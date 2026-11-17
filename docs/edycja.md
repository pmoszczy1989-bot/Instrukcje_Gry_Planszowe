# Edycja i rozwój

[← README](../README.md)

Instrukcje są zapisane wewnątrz `instrukcje_gier.html` w postaci base64, więc nie da się ich wygodnie edytować bezpośrednio. Do edycji służą dwa skrypty w katalogu `narzedzia/` (wymagają **Python 3.8+**, bez dodatkowych pakietów).

## Krok po kroku

```powershell
# 1. Wypakuj instrukcje do folderu zrodla/
python narzedzia/rozpakuj.py

# 2. Edytuj pliki:
#    zrodla/level8_instrukcja.html
#    zrodla/sabotazysta_instrukcja.html
#    zrodla/kroniki_zamku_avel_instrukcja.html
#    zrodla/wsiasc_do_pociagu_europa_instrukcja.html
#    zrodla/munchkin_instrukcja.html
#    (każdy można otworzyć bezpośrednio w przeglądarce)

# 3. Wstaw zmiany z powrotem do instrukcje_gier.html
python narzedzia/zbuduj.py

# 4. Sprawdź wynik w przeglądarce i zatwierdź
git add instrukcje_gier.html
git commit -m "Opis zmiany"
git push
```

Folder `zrodla/` jest w `.gitignore`. W repozytorium trzymany jest tylko gotowy plik `instrukcje_gier.html`.

Obu skryptom można podać inny folder jako argument, np. `python narzedzia/rozpakuj.py C:\tmp\gry`. Jeśli w folderze brakuje któregoś pliku, `zbuduj.py` zostawia dotychczasową wersję tej gry.

## Typowe zmiany

| Co zmienić | Gdzie szukać w pliku źródłowym |
|---|---|
| Treść rozdziału zasad | odpowiednia `<section>` w HTML |
| Komentarze w partii na 4 graczy | tablica `STEPS` (pole z tekstem kroku) |
| Przebieg partii generowanej | funkcja generatora (`genL8`, `genAvel`, generator Sabotażysty) |
| Inna partia dla danej liczby graczy | stała `SEEDS`: zmień ziarno i sprawdź, czy partia ma sensowną długość i zakończenie |
| Wygląd kart lub planszy | sekcja `<style>` |
| Ściąga | ostatnia `<section>` z tabelą |

## Dodanie nowej gry

1. Przygotuj samodzielny plik HTML z instrukcją (najlepiej na wzór istniejących).
2. W `instrukcje_gier.html`:
   - dodaj `<option value="klucz">🎯 Nazwa gry</option>` do listy `#game`;
   - dodaj wpis `klucz:"<base64>"` do obiektu `DATA`.
3. Dopisz grę do słownika `NAMES` w obu skryptach w `narzedzia/`.
4. Uzupełnij `README.md` i dodaj stronę gry w `docs/`.

## Zasady przy zmianach

- Teksty są **po polsku**. Pliki mają kodowanie **UTF-8**.
- Generatory muszą pozostać **deterministyczne** (patrz [Budowa techniczna](budowa-techniczna.md#liczba-graczy-i-generatory)).
- Po zmianie sprawdź każdą liczbę graczy danej gry aż do ostatniego kroku i upewnij się, że konsola nie pokazuje błędów.
