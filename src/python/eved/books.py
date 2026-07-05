#!/usr/bin/env python3
"""Bible books reference map for the eved project.

This module provides the ``Books`` class, which wraps the ``data/books/map.py``
literal.  Each key is an English book name (e.g. ``'Genesis'``, ``'1 Kings'``)
and each value is a dict containing the Hebrew name, pronunciation, and
related metadata.

Typical usage::

    from books import Books

    print(Books.book_list())
    # ['Genesis', 'Exodus', ..., 'John', ...]

    entry = Books.get_book('Genesis')
    print(entry['hebrew'])
    print(entry['hebrew_say'])
"""

from filepath import FilePath
from filepath import eval_file


class Books(dict):
    """Dict subclass loaded from the Bible books map file.

    The map covers all Old Testament books and the beginning of the New
    Testament.  Keys are the English book names used throughout the category
    verse data (e.g. ``'1 Kings'``, ``'Psalms'``) so that lookups are
    consistent across the whole project.

    Example:
        >>> from books import Books
        >>> 'Genesis' in Books.book_list()
        True
        >>> Books.get_book('Exodus')['hebrew_say']
        'Shemot'
    """

    def __init__(self, *arg, **kw):
        """Initialise and immediately load the books map from disk.

        Args:
            *arg: Passed through to ``dict.__init__``.
            **kw: Passed through to ``dict.__init__``.
        """
        super(Books, self).__init__(*arg, **kw)
        self.file = self.get_books_path
        self.update(eval_file(self.file))

    @property
    def get_books_path(self):
        """Return the absolute path to the Bible books map file.

        Returns:
            str: Absolute path to ``eved/data/books/map.py``.

        Example:
            >>> from books import Books
            >>> Books().get_books_path.endswith('map.py')
            True
        """
        return FilePath().get_books

    @classmethod
    def get_book(cls, book):
        """Return the map entry for a single Bible book by its English name.

        Args:
            book (str): English book name, e.g. ``'Genesis'`` or ``'1 Kings'``.

        Returns:
            dict: Entry with at minimum the keys ``hebrew`` and ``hebrew_say``.

        Raises:
            NameError: If ``book`` is not a recognised key in the map.

        Example:
            >>> from books import Books
            >>> entry = Books.get_book('Numbers')
            >>> entry['hebrew_say']
            'Bamidbar'
            >>> Books.get_book('FakeBook')
            Traceback (most recent call last):
                ...
            NameError: Book name(FakeBook) not found, ...
        """
        if book not in cls().book_list():
            raise NameError(f'Book name({book}) not found, allowed books: {Books.book_list()}')
        return cls()[book]

    @classmethod
    def book_list(cls):
        """Return the list of all supported English book names.

        Returns:
            list[str]: All keys from the books map in insertion order.

        Example:
            >>> from books import Books
            >>> names = Books.book_list()
            >>> names[0]
            'Genesis'
            >>> isinstance(names, list)
            True
        """
        return list(cls().keys())
