"""Translate LaTeX CV context using NLLB (No Language Left Behind)."""
from __future__ import annotations

import os
import copy
from typing import Any, List, Dict

import torch
from transformers import AutoModelForSeq2SeqLM, NllbTokenizerFast

from src.resume import logger

# --- EXPORTED CONSTANTS ---
NLLB_EN = "eng_Latn"
NLLB_FR = "fra_Latn"
NLLB_PT = "por_Latn"

TARGET_LANGUAGES = (NLLB_EN, NLLB_FR, NLLB_PT)
LANG_SUFFIX = {NLLB_EN: "_en", NLLB_FR: "_fr", NLLB_PT: "_pt"}

_MODEL_ID = "facebook/nllb-200-distilled-600M"

# Use cache only by default to avoid Hugging Face API timeouts (e.g. safetensors conversion check).
# Set RESUME_NLLB_DOWNLOAD=1 when you need to download the model for the first time.
_LOCAL_FILES_ONLY = os.environ.get("RESUME_NLLB_DOWNLOAD") != "1"


def _load_nllb():
    """Load tokenizer and model; prefer cache to avoid hub API timeouts."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Loading NLLB model ({_MODEL_ID}) on {device}...")
    try:
        tokenizer = NllbTokenizerFast.from_pretrained(_MODEL_ID, local_files_only=_LOCAL_FILES_ONLY)
        model = AutoModelForSeq2SeqLM.from_pretrained(_MODEL_ID, local_files_only=_LOCAL_FILES_ONLY).to(device)
    except OSError as e:
        if _LOCAL_FILES_ONLY and ("not found" in str(e).lower() or "cache" in str(e).lower()):
            logger.warning("Model not in cache. Run once with RESUME_NLLB_DOWNLOAD=1 python main.py to download.")
            raise RuntimeError(
                "NLLB model not in cache. Download first with: RESUME_NLLB_DOWNLOAD=1 python main.py"
            ) from e
        raise
    logger.info("NLLB model loaded.")
    return tokenizer, model, device


class NLLBTranslator:
    """Singleton that holds the NLLB model in memory."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            tok, model, device = _load_nllb()
            cls._instance.tokenizer = tok
            cls._instance.model = model
            cls._instance.device = device
        return cls._instance

    def translate_batch(self, texts: List[str], src_lang: str, tgt_lang: str) -> List[str]:
        """Translate a batch of strings efficiently."""
        if not texts:
            return []

        # Filter empty strings
        valid_indices = [i for i, t in enumerate(texts) if t and t.strip()]
        valid_texts = [texts[i].strip() for i in valid_indices]

        if not valid_texts:
            return texts

        self.tokenizer.src_lang = src_lang

        inputs = self.tokenizer(
            valid_texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.device)

        forced_bos_id = self.tokenizer.convert_tokens_to_ids(tgt_lang)

        with torch.no_grad():
            generated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_id,
                max_length=512,
            )

        translated_valid = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

        result = list(texts)
        for i, trans in zip(valid_indices, translated_valid):
            result[i] = trans

        return result

def translate_context(context: dict, src_lang: str, tgt_lang: str) -> dict:
    if src_lang == tgt_lang:
        return copy.deepcopy(context)

    logger.info(f"Translating CV context from {src_lang} to {tgt_lang}")
    translator = NLLBTranslator()

    pointers = []
    texts_to_translate = []

    def collect(d: Dict, key: str):
        if d.get(key):
            pointers.append((d, key))
            texts_to_translate.append(str(d[key])) # Ensure string conversion

    ctx = copy.deepcopy(context)

    # Single fields
    for k in ["headline_text", "tagline", "footer_title", "title", "role", "summary", "description"]:
        if k in ctx: collect(ctx, k)

    for k in ctx.keys():
        if k.endswith("_section_title"):
            collect(ctx, k)

    # Nested Lists
    for entry in ctx.get("competence_entries", []):
        collect(entry, "category")
        collect(entry, "text")

    for entry in ctx.get("experience_entries", []):
        for k in ["title", "company", "location", "description", "tags", "date_from", "date_to"]:
            collect(entry, k)

    for entry in ctx.get("education_entries", []):
        collect(entry, "description")
        collect(entry, "period")
        collect(entry, "degree")

    for entry in ctx.get("project_entries", []):
        collect(entry, "description")
        collect(entry, "title")
        collect(entry, "subtitle")

    if not texts_to_translate:
        return ctx

    logger.info(f"Batch translating {len(texts_to_translate)} fields...")
    translated_texts = translator.translate_batch(texts_to_translate, src_lang, tgt_lang)

    for (d, key), trans_text in zip(pointers, translated_texts):
        d[key] = trans_text

    return ctx