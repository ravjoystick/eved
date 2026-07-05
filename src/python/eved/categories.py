#!/usr/bin/env python3
"""Category objects and helpers for the eved project.

Each *category* represents one attribute of God documented by Richard Dawkins
in *The God Delusion* (Chapter 2).  The authoritative data lives in
``data/categories/python/`` as bare Python dict literals; this module
dynamically loads all of them at import time into ``__all__`` and exposes
convenience wrappers for iteration, lookup, and JSON export.

Typical usage::

    from categories import Category, category_names, get_all_categories

    print(category_names())
    # ['angry', 'bloodthirsty', 'bully', ...]

    cat = Category('jealous')
    print(cat)            # Jealous
    print(cat['verses'])  # {1: {...}, 2: {...}, ...}

    cat.to_json()         # writes/updates data/categories/json/jealous.json
"""

import os

from filepath import FilePath
from filepath import eval_file

# Load every .py file from data/categories/python/ into __all__ at import time.
_python_root = FilePath().get_categories_python
__all__ = [
    eval_file(os.path.join(_python_root, f))
    for f in sorted(os.listdir(_python_root))
    if f.endswith('.py')
]


def get_all_categories():
    """Return a ``Category`` object for every loaded category.

    Returns:
        list[Category]: One ``Category`` per file in ``data/categories/python/``,
        sorted by filename (alphabetical).

    Example:
        >>> from categories import get_all_categories
        >>> cats = get_all_categories()
        >>> isinstance(cats[0], Category)
        True
        >>> len(cats) >= 27
        True
    """
    return [Category(c['name']) for c in __all__]


def category_names():
    """Return the ``name`` string for every loaded category.

    Returns:
        list[str]: Category name strings sorted alphabetically by filename.

    Example:
        >>> from categories import category_names
        >>> names = category_names()
        >>> 'jealous' in names
        True
        >>> 'homophobic' in names
        True
    """
    return [c['name'] for c in __all__]


class Category(dict):
    """A single God-character category, backed by its Python dict literal.

    ``Category`` extends ``dict``, so all verse data is accessible via normal
    dict operations.  On construction the matching entry is located in
    ``__all__`` by ``name`` and the instance is populated with its data.

    Attributes:
        category (str): The internal snake_case name of this category.
        is_true (bool): Whether this category has been confirmed true
            (application-level flag; not persisted).

    Example:
        >>> from categories import Category
        >>> cat = Category('jealous')
        >>> str(cat)
        'Jealous'
        >>> repr(cat)
        'Category(jealous)'
        >>> cat['name']
        'jealous'
        >>> cat['nice_name']
        'Jealous'
    """

    TYPE = None

    def __init__(self, category, is_true=False):
        """Initialise the Category by looking up ``category`` in ``__all__``.

        Args:
            category (str): The snake_case name of the category, e.g.
                ``'jealous'`` or ``'ethnic_cleanser'``.
            is_true (bool): Optional initial value for the ``true`` flag.
                Defaults to ``False``.

        Raises:
            ValueError: If no entry with ``name == category`` exists in
                ``__all__``.

        Example:
            >>> from categories import Category
            >>> Category('bloodthirsty')['nice_name']
            'Bloodthirsty'
            >>> Category('nonexistent')
            Traceback (most recent call last):
                ...
            ValueError: Could not find category: 'nonexistent'. ...
        """
        self.category = None
        self.is_true = is_true
        for _category in __all__:
            if _category['name'] == category:
                super(Category, self).__init__(_category)
                self.category = category
        if not self.category:
            raise ValueError(
                f'Could not find category: {category!r}. '
                f'Available: {category_names()}'
            )

    def __repr__(self):
        """Return an unambiguous string representation.

        Returns:
            str: ``'Category(<name>)'``.

        Example:
            >>> from categories import Category
            >>> repr(Category('jealous'))
            'Category(jealous)'
        """
        return f'{self.__class__.__name__}({self.category})'

    def __str__(self):
        """Return the human-readable display name.

        Returns:
            str: The ``nice_name`` value for this category.

        Example:
            >>> from categories import Category
            >>> str(Category('ethnic_cleanser'))
            'Ethnic Cleanser'
        """
        return self['nice_name']

    @property
    def true(self):
        """Whether this category has been marked as confirmed.

        Returns:
            bool: Current value of the confirmation flag.

        Example:
            >>> from categories import Category
            >>> cat = Category('jealous')
            >>> cat.true
            False
            >>> cat.true = True
            >>> cat.true
            True
        """
        return self.is_true

    @true.setter
    def true(self, true):
        """Set the confirmation flag.

        Args:
            true (bool): New value for the confirmation flag.
        """
        self.is_true = true

    @classmethod
    def create(cls, category):
        """Factory method that creates a ``Category`` by name.

        Equivalent to calling ``Category(category)`` directly; provided as a
        named constructor for readability.

        Args:
            category (str): Snake_case category name.

        Returns:
            Category: The matching category instance.

        Example:
            >>> from categories import Category
            >>> cat = Category.create('bully')
            >>> cat['name']
            'bully'
        """
        return cls(category)

    def to_json(self):
        """Write this category's data to its JSON file and return the path.

        The output file is placed in ``data/categories/json/`` with the same
        stem as the source ``.py`` file.  Any existing JSON file is overwritten.

        Returns:
            str: Absolute path of the JSON file that was written.

        Example:
            >>> import os
            >>> from categories import Category
            >>> path = Category('jealous').to_json()
            >>> os.path.basename(path)
            'jealous.json'
        """
        from filepath import _create_json
        py_file = os.path.join(FilePath().get_categories_python, f'{self.category}.py')
        return _create_json(py_file, dict(self))
