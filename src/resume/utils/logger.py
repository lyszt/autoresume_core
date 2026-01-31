from __future__ import annotations
import threading
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Final, Dict, Any
from rich.console import Console


class Logger:
    """Thread-safe logger using rich markup for vivid console output."""

    LEVELS: Final[Dict[str, int]] = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40}
    COLORS: Final[Dict[str, str]] = {
        "DEBUG": "bright_black", "INFO": "bold cyan",
        "WARNING": "bold yellow", "ERROR": "bold red",
        "TIME": "green", "NAME": "bold magenta", "MSG": "white"
    }

    def __init__(self, name: str = "resume", file_path: Optional[str] = None, level: str = "INFO",
                 console: bool = True) -> None:
        self.name: str = name
        self.level_val: int = self.LEVELS.get(level.upper(), 20)
        self.rich: Optional[Console] = Console() if console else None
        self.path: Path = Path(file_path or f"logs/{name}.log").resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock: threading.Lock = threading.Lock()

    def log(self, level: str, message: str) -> None:
        lvl: str = level.upper()
        if self.LEVELS.get(lvl, 0) < self.level_val: return

        now: datetime = datetime.now(timezone.utc)
        ts_short: str = now.strftime('%H:%M:%S')

        if self.rich:
            color: str = self.COLORS.get(lvl, "white")
            # Multi-colored console output using Rich tags
            self.rich.print(
                f"[{self.COLORS['TIME']}]{ts_short}[/] "
                f"| [{color}]{lvl:^7}[/] | "
                f"[{self.COLORS['NAME']}]{self.name}[/] : "
                f"[{self.COLORS['MSG']}]{message}[/]"
            )

        with self._lock, self.path.open("a", encoding="utf-8") as f:
            f.write(f"{now.isoformat()} [{lvl}] {self.name}: {message}\n")

    def debug(self, msg: str) -> None:
        self.log("DEBUG", msg)

    def info(self, msg: str) -> None:
        self.log("INFO", msg)

    def warning(self, msg: str) -> None:
        self.log("WARNING", msg)

    def error(self, msg: str) -> None:
        self.log("ERROR", msg)


_default: Optional[Logger] = None


def get_logger(**kwargs: Any) -> Logger:
    global _default
    if _default is None: _default = Logger(**kwargs)
    return _default