#!/usr/bin/env python3
"""Hebrew gematria (alphabetic numeral) map for integers 1–100.

This module provides the ``Numbers`` class, which wraps the ``data/numbers/map.py``
literal.  Each key is an integer (1–100) and each value is a dict containing the
Hebrew letter(s), their Unicode code points, HTML entities, and the standard
transliterated pronunciation.

Typical usage::

    from numbers import Numbers

    all_nums = Numbers.get_numbers_map()
    entry = all_nums[15]           # {'hebrew': 'טו', 'unicode': [...], ...}
    print(entry['hebrew_say'])     # 'Tet Vav'
"""

from filepath import FilePath
from filepath import eval_file


class Numbers(dict):
    """Dict subclass that wraps the Hebrew gematria map.

    The map covers integers 1–100.  Entries 15 and 16 intentionally use
    Tet+Vav (טו) and Tet+Zayin (טז) instead of the arithmetically expected
    Yod+He and Yod+Vav, so that no entry accidentally spells a divine name.

    Example:
        >>> from numbers import Numbers
        >>> n = Numbers.get_numbers_map()
        >>> n[1]['hebrew_say']
        'Alef'
        >>> n[15]['hebrew']
        'טו'
        >>> n[100]['hebrew_say']
        'Kof'
    """

    def __init__(self, *arg, **kw):
        """Initialise as an empty dict; data is loaded via ``get_numbers_map``."""
        super(Numbers, self).__init__(*arg, **kw)

    @property
    def get_numbers_path(self):
        """Return the absolute path to the Hebrew numbers map file.

        Returns:
            str: Absolute path to ``eved/data/numbers/map.py``.

        Example:
            >>> from numbers import Numbers
            >>> Numbers().get_numbers_path.endswith('map.py')
            True
        """
        return FilePath().get_numbers

    @classmethod
    def get_numbers_map(cls):
        """Load and return the full Hebrew gematria map.

        Reads ``data/numbers/map.py`` via ``eval_file`` and returns the bare
        Python dict it contains.  Keys are integers 1–100; values are dicts
        with the keys ``hebrew``, ``unicode``, ``html``, and ``hebrew_say``.

        Returns:
            dict[int, dict]: Mapping of integer → Hebrew numeral entry.

        Raises:
            FileNotFoundError: If ``data/numbers/map.py`` is missing.

        Example:
            >>> from numbers import Numbers
            >>> data = Numbers.get_numbers_map()
            >>> len(data)
            100
            >>> data[10]['hebrew']
            'י'
            >>> data[10]['hebrew_say']
            'Yod'
        """
        number_file = cls().get_numbers_path
        return eval_file(number_file)
