"""Wstawia (zaktualizowane) instrukcje z powrotem do instrukcje_gier.html.

Użycie (z katalogu głównego repozytorium):
    python narzedzia/zbuduj.py              # czyta pliki z folderu zrodla/
    python narzedzia/zbuduj.py inny_folder

Brakujące pliki źródłowe są pomijane – w instrukcje_gier.html zostaje wtedy
dotychczasowa wersja danej gry.
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
    "ttr": "wsiasc_do_pociagu_europa_instrukcja.html",
    "munchkin": "munchkin_instrukcja.html",
}


def main() -> None:
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "zrodla"
    text = MAIN.read_bytes().decode("utf-8")
    for key, name in NAMES.items():
        f = src / name
        if not f.exists():
            print(f"{key:12} pominięto (brak {f})")
            continue
        data = base64.b64encode(f.read_bytes()).decode("ascii")
        text, n = re.subn(key + r':"[A-Za-z0-9+/=]+"', lambda _: f'{key}:"{data}"', text, count=1)
        if n != 1:
            sys.exit(f"Nie znaleziono miejsca na '{key}' w {MAIN.name}")
        print(f"{key:12} <- {f}")
    MAIN.write_bytes(text.encode("utf-8"))
    print(f"Zapisano {MAIN}")


if __name__ == "__main__":
    main()
