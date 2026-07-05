# eved

> *Eved* (עֶבֶד) is Hebrew for slave or servant. It is what they want us to be. We can do better.

A Python data project cataloguing the negative character traits of the God of the Old Testament, as described in Dan Barker's book *"God: The Most Unpleasant Character in All Fiction"* — itself inspired by the famous passage from Richard Dawkins' *The God Delusion*:

> "The God of the Old Testament is arguably the most unpleasant character in all fiction: jealous and proud of it; and petty, unjust, unforgiving control-freak; a vindictive, bloodthirsty ethnic cleanser; a misogynistic, homophobic, racist, infanticidal, genocidal, filicidal, pestilential, megalomaniacal, sadomasochistic, capriciously malevolent bully."

The project maps each trait to specific Bible verses, cross-referenced with 19 Bible translations, and provides Hebrew names and numerals for chapter/verse rendering.

---

## Project Structure

```
eved/
├── src/
│   └── python/
│       └── eved/
│           ├── src/
│           │   ├── filepath.py      # FilePath class + eval_file() loader
│           │   ├── books.py         # Books class — Bible book lookup
│           │   ├── numbers.py       # Numbers class — Hebrew numeral map
│           │   └── categories.py    # Category class — trait loader + JSON export
│           └── data/
│               ├── categories/
│               │   ├── python/      # Category definitions (source of truth)
│               │   └── json/        # Auto-generated JSON mirrors
│               ├── books/
│               │   └── map.py       # English book name → Hebrew name + pronunciation
│               ├── numbers/
│               │   └── map.py       # Integer 1–100 → Hebrew numeral (gematria)
│               └── bible/
│                   ├── *.json       # 19 Bible translations
│                   ├── godBook.01.pdf
│                   └── 1454918322G.epub
└── src/tests/
```

---

## Categories

Each category is a Python dict file under `data/categories/python/` and a mirrored JSON under `data/categories/json/`. Each entry in a category maps a numbered verse reference to a note, book, chapter, verse list, and search tags for the UI.

### Currently implemented

| File | Trait |
|------|-------|
| `jealous.py` | Jealous |
| `unjust.py` | Unjust |
| `unforgiving.py` | Unforgiving |
| `control_freak.py` | Control Freak |
| `bloodthirsty.py` | Bloodthirsty |
| `ethnic_cleanser.py` | Ethnic Cleanser |
| `homophobic.py` | Homophobic |

### From the book — to be implemented

Petty, Vindictive, Misogynistic, Racist, Infanticidal, Genocidal, Filicidal, Pestilential, Megalomaniacal, Sadomasochistic, Capriciously Malevolent, Bully, Pyromaniacal, Angry, Merciless, Curse Hurling, Vaccicidal, Aborticidal, Cannibalistic, Slavemonger

### Category data format

```python
{
    'name': 'jealous',
    'nice_name': 'Jealous',
    'dictionary': '...',
    'verses': {
        1: {
            'notes': 'Avenging and wrathful',
            'book': 'Nahum',
            'chapter': 1,
            'verse': [2],
            'search': ['why would god be jealous if He created everything'],
        },
        ...
    }
}
```

---

## Bible Translations

19 translations are included as JSON under `data/bible/`:

| File | Language / Translation |
|------|----------------------|
| `ar_svd.json` | Arabic |
| `de_schlachter.json` | German (Schlachter) |
| `el_greek.json` | Greek |
| `en_bbe.json` | English (BBE) |
| `en_kjv.json` | English (KJV) |
| `eo_esperanto.json` | Esperanto |
| `es_rvr.json` | Spanish (RVR) |
| `fi_finnish.json` | Finnish |
| `fi_pr.json` | Finnish (PR) |
| `fr_apee.json` | French (APEE) |
| `ko_ko.json` | Korean |
| `pt_aa.json` | Portuguese (AA) |
| `pt_acf.json` | Portuguese (ACF) |
| `pt_nvi.json` | Portuguese (NVI) |
| `ro_cornilescu.json` | Romanian (Cornilescu) |
| `ru_synodal.json` | Russian (Synodal) |
| `vi_vietnamese.json` | Vietnamese |
| `zh_cuv.json` | Chinese (CUV) |
| `zh_ncv.json` | Chinese (NCV) |

---

## Hebrew Numbers Map

`data/numbers/map.py` maps integers **1–100** to their Hebrew numeral representation using the traditional gematria/alphabetic numeral system, with Unicode code points and HTML entities for each letter.

Notable: 15 is written **טו** (Tet + Vav) and 16 as **טז** (Tet + Zayin) — not יה / יו — to avoid spelling one of God's names.

---

## Hebrew Books Map

`data/books/map.py` maps English Bible book names to their Hebrew name and transliterated pronunciation, covering the full Old Testament and the beginning of the New Testament.

---

## Source / Reference

- *God: The Most Unpleasant Character in All Fiction* — Dan Barker (2016)
- *The God Delusion* — Richard Dawkins (2006)
