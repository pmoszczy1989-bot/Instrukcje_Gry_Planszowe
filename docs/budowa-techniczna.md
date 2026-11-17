# Budowa techniczna

[← README](../README.md)

## Jeden plik, pięć instrukcji

`instrukcje_gier.html` to samodzielna strona bez zewnętrznych zależności. Zawiera:

- **pasek górny** (`#bar`) z listą wyboru gry (`<select id="game">`);
- kontener `#frames`, w którym pojawiają się ramki (`<iframe>`) z instrukcjami;
- obiekt danych z trzema pełnymi instrukcjami HTML zakodowanymi w **base64**:

```js
const DATA = { level8: "…", sabotazysta: "…", avel: "…", ttr: "…", munchkin: "…" };
```

Funkcja `show(klucz)`:

1. przy pierwszym użyciu dekoduje base64 (UTF-8), tworzy z niego `Blob` i adres `URL.createObjectURL`, a potem ramkę `iframe` z tym adresem (**leniwe ładowanie**);
2. ukrywa pozostałe ramki i pokazuje wybraną (klasa `.on`); dzięki temu stan każdej gry jest zachowany;
3. ustawia wartość listy i kotwicę w adresie (`history.replaceState`, np. `#avel`).

Każda instrukcja działa w osobnej ramce, więc ich style, skrypty i skróty klawiszowe nie kolidują ze sobą.

## Budowa pojedynczej instrukcji

Każda z instrukcji to osobny dokument HTML z wbudowanym CSS i JS:

- **rozdziały** (`<section>`) z animacjami CSS; pojawiają się przy przewijaniu dzięki `IntersectionObserver`;
- **symulacja rozgrywki**, czyli silnik krokowy opisany niżej;
- **ściąga** w formie tabeli.

Grafiki to wyłącznie emoji, gradienty CSS i elementy HTML, bez plików graficznych.

### Silnik krokowy

```text
STEPS[]  ──computeStates()──►  STATES[]  ──render(i)──►  DOM (plansza, ręce, komentarz)
```

- **`STEPS`**: lista kroków partii. Każdy krok ma tekst komentarza i funkcję `f(s)`, która zmienia stan gry (przenosi karty, zmienia poziomy, rany, pozycje itp.).
- **`computeStates()`**: zaczyna od stanu początkowego, kolejno stosuje `f` na głębokich kopiach i zapisuje wynik każdego kroku w `STATES`. Dzięki temu przewijanie wstecz i skoki suwakiem działają od razu.
- **`render(i)`**: rysuje stan `i`. Elementy mają stałe `data-id`, więc przy zmianie kroku animacja FLIP przesuwa je płynnie ze starej pozycji do nowej, a zmienione elementy są podświetlane.
- **`go(i)`, `play()`, `pause()`**: nawigacja i automatyczne odtwarzanie z ustawionym tempem.
- **`buildMarks()`**: tworzy przyciski skoku do rund z kroków oznaczonych jako początek rundy.

### Liczba graczy i generatory

- Partia na **4 graczy** w Level 8, Sabotażyście i Kronikach Zamku Avel jest opisana ręcznie jako stała lista kroków. W Wsiąść do Pociągu i Munchkinie wszystkie partie tworzy generator.
- Dla pozostałych liczb `build(n)` wywołuje **generator**, który rozgrywa partię według zasad i tworzy z niej `STEPS`:
  - `genL8`: Level 8;
  - generator Sabotażysty;
  - `genAvel`: Kroniki Zamku Avel (uproszczona sztuczna inteligencja drużyny).
- Generatory używają deterministycznego PRNG **mulberry32** ze **stałym ziarnem** dla każdej liczby graczy. Dzięki temu partie są zawsze takie same, a ziarna zostały dobrane tak, żeby partie były ciekawe i miały rozsądną długość.

| Gra | Ziarna (`liczba graczy: ziarno`) |
|---|---|
| Level 8 | `2:43, 3:22, 5:8, 6:99` |
| Sabotażysta | `3:59, 5:48, 6:12, 7:14, 8:12, 9:12, 10:1` |
| Kroniki Zamku Avel | `1:502, 2:1504, 3:681` |
| Wsiąść do Pociągu: Europa | `2:288, 3:169, 4:205, 5:147` (wszystkie partie generowane) |
| Munchkin | `3:3450571044, 4:134586765, 5:4246706327, 6:3084875576`, modyfikowane maską dodatków: `(ZIARNO ^ Math.imul(maska, 7919)) >>> 0` |

> **Uwaga o determinizmie:** w generatorach nie wolno tasować przez `array.sort(() => rnd() - 0.5)`. Wynik takiego sortowania zależy od algorytmu sortowania w przeglądarce, więc ta sama partia wyglądałaby inaczej np. w Edge i Firefoksie. Zamiast tego jest tasowanie Fishera–Yatesa i sortowanie po stałym kluczu.

## Testowanie

- Najprościej otworzyć plik w przeglądarce i przejrzeć każdą grę dla każdej liczby graczy (lista **👥 Gracze**), przewijając suwakiem do końca. Konsola deweloperska (F12) nie powinna pokazywać błędów.
- Zrzuty w `docs/img/` zrobiono w trybie headless Edge:

```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu `
  --window-size=1400,900 --screenshot=zrzut.png "file:///C:/sciezka/instrukcje_gier.html#level8"
```

  Rozdziały pojawiają się dopiero przy przewijaniu, więc do zrzutów warto wstrzyknąć CSS `section{opacity:1!important;transform:none!important}`.
