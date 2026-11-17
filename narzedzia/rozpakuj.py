"""Wypakowuje trzy instrukcje z instrukcje_gier.html do osobnych plików HTML.

Użycie (z katalogu głównego repozytorium):
    python narzedzia/rozpakuj.py            # zapisuje do folderu zrodla/
    python narzedzia/rozpakuj.py inny_folder
"""
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAIN = ROOT / "instrukcje_gier.html"
NAMES = {
    "level8": "level8_instrukcja.html",
    "sabotazysta": "sabotazysta_instrukcja.html",
    "avel": "kroniki_zamku_avel_instrukcja.html",
}


def main() -> None:
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "zrodla"
    out.mkdir(parents=True, exist_ok=True)
    text = MAIN.read_text(encoding="utf-8")
    for key, name in NAMES.items():
        m = re.search(key + r':"([A-Za-z0-9+/=]+)"', text)
        if not m:
            sys.exit(f"Nie znaleziono danych dla '{key}' w {MAIN.name}")
        (out / name).write_bytes(base64.b64decode(m.group(1)))
        print(f"{key:12} -> {out / name}")


if __name__ == "__main__":
    main()
