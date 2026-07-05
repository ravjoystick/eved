#!/usr/bin/env python3
"""Filesystem path resolution and JSON generation utilities for the eved project.

This module provides the ``FilePath`` class, which resolves absolute paths to
every data directory and file the project uses, along with helper functions for
loading Python dict files via ``eval`` and for generating the JSON mirrors of
the category data.

Typical usage::

    from filepath import FilePath, create_all_jsons, eval_file

    fp = FilePath()
    print(fp.get_data)            # .../eved/data
    print(fp.get_categories_json) # .../eved/data/categories/json

    create_all_jsons()            # regenerate all 27 category JSON files
"""

import json
import os

# Root of the eved package — one dirname up from this file's location.
# filepath.py lives at  src/python/eved/filepath.py
# APP_ROOT_FOLDER resolves to  src/python/eved/
APP_ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))

DATA_FOLDER = 'data'
TESTS_FOLDER = 'tests'
CATEGORIES_FOLDER = 'categories'
CATEGORIES_TYPE_PYTHON = 'python'
CATEGORIES_TYPE_JSON = 'json'
NUMBERS_FOLDER = 'numbers'
BOOKS_FOLDER = 'books'


def eval_file(filepath):
    """Read a ``.py`` file that contains a bare Python literal and return it.

    The category and map data files are stored as plain Python dicts (no
    assignment, just a literal).  This function reads those files and
    evaluates them with the built-in ``eval``.

    Args:
        filepath (str): Absolute path to the Python literal file.

    Returns:
        Any: The Python object described in the file — typically a ``dict``.

    Raises:
        FileNotFoundError: If ``filepath`` does not exist.
        SyntaxError: If the file content is not valid Python.

    Example:
        >>> from filepath import eval_file, FilePath
        >>> data = eval_file(FilePath().get_numbers)
        >>> data[1]['hebrew_say']
        'Alef'
    """
    with open(filepath, 'r', encoding='utf-8') as fh:
        return eval(fh.read())


def create_all_jsons():
    """Generate a JSON mirror for every category ``.py`` file.

    Reads every ``.py`` file under ``data/categories/python/``, evaluates it
    as a Python dict, and writes the result as a formatted JSON file into
    ``data/categories/json/``.  Existing JSON files are overwritten.

    Returns:
        list[str]: Absolute paths of every JSON file that was written.

    Raises:
        IOError: If the python categories folder does not exist.

    Example:
        >>> from filepath import create_all_jsons
        >>> written = create_all_jsons()
        >>> len(written) >= 27
        True
        >>> written[0].endswith('.json')
        True
    """
    python_root = FilePath().get_categories_python
    if not os.path.exists(python_root):
        raise IOError('Python categories folder not found!')

    written = []
    for filename in os.listdir(python_root):
        if not filename.endswith('.py'):
            continue
        data = eval_file(os.path.join(python_root, filename))
        written.append(_create_json(os.path.join(python_root, filename), data))
    return written


def _create_json(filepath, data):
    """Write ``data`` to a JSON file named after the stem of ``filepath``.

    The output file is placed in ``data/categories/json/`` regardless of where
    ``filepath`` lives.  The filename is derived by stripping the directory and
    extension from ``filepath``.

    Args:
        filepath (str): Path to the source ``.py`` file — used only to derive
            the output filename.
        data (dict): The Python dict to serialise as JSON.

    Returns:
        str: Absolute path of the JSON file that was written.

    Raises:
        IOError: If the JSON categories folder does not exist.

    Example:
        >>> import os, tempfile
        >>> from filepath import _create_json, FilePath
        >>> sample = {'name': 'test', 'verses': {}}
        >>> fake_py = os.path.join(FilePath().get_categories_python, 'jealous.py')
        >>> path = _create_json(fake_py, sample)
        >>> os.path.basename(path)
        'jealous.json'
    """
    json_root = FilePath().get_categories_json
    if not os.path.exists(json_root):
        raise IOError('JSON categories folder not found!')

    stem = os.path.basename(filepath).rsplit('.', 1)[0]
    json_file = os.path.join(json_root, f'{stem}.json')
    with open(json_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
    return json_file


class FilePath:
    """Resolves absolute paths to every data directory and file in the project.

    All paths are derived from the location of this module, so the project
    can be moved freely on disk without any hardcoded paths.

    Attributes:
        root (str): Absolute path to the ``eved`` package root directory
            (the folder that contains ``data/``).

    Example:
        >>> from filepath import FilePath
        >>> fp = FilePath()
        >>> fp.get_data.endswith('data')
        True
        >>> fp.get_categories_python.endswith('python')
        True
    """

    def __init__(self):
        """Initialise FilePath with the package root resolved from this file."""
        self.root = APP_ROOT_FOLDER

    @property
    def get_root(self):
        """Return the absolute path to the eved package root.

        Returns:
            str: Absolute path, e.g. ``/path/to/src/python/eved``.

        Example:
            >>> from filepath import FilePath
            >>> isinstance(FilePath().get_root, str)
            True
        """
        return self.root

    @property
    def get_data(self):
        """Return the absolute path to the ``data/`` directory.

        Returns:
            str: Absolute path to ``eved/data``.

        Raises:
            ValueError: If the ``data/`` directory does not exist.

        Example:
            >>> import os
            >>> from filepath import FilePath
            >>> os.path.isdir(FilePath().get_data)
            True
        """
        data = os.path.join(self.root, DATA_FOLDER)
        if os.path.exists(data):
            return data
        raise ValueError('Missing data folder!')

    @property
    def get_tests(self):
        """Return the absolute path to the ``tests/`` directory.

        Returns:
            str: Absolute path to the tests directory.

        Raises:
            ValueError: If the ``tests/`` directory does not exist.

        Example:
            >>> from filepath import FilePath
            >>> isinstance(FilePath().get_tests, str)
            True
        """
        tests = os.path.join(self.root, TESTS_FOLDER)
        if os.path.exists(tests):
            return tests
        raise ValueError('Missing tests folder!')

    @property
    def get_caterogies(self):
        """Return the absolute path to the ``data/categories/`` directory.

        Returns:
            str: Absolute path to ``eved/data/categories``.

        Example:
            >>> from filepath import FilePath
            >>> FilePath().get_caterogies.endswith('categories')
            True
        """
        return os.path.join(self.get_data, CATEGORIES_FOLDER)

    @property
    def get_categories_python(self):
        """Return the absolute path to ``data/categories/python/``.

        This is the directory that contains the authoritative Python dict
        files for every category.

        Returns:
            str: Absolute path to ``eved/data/categories/python``.

        Example:
            >>> from filepath import FilePath
            >>> FilePath().get_categories_python.endswith('python')
            True
        """
        return os.path.join(self.get_caterogies, CATEGORIES_TYPE_PYTHON)

    @property
    def get_categories_json(self):
        """Return the absolute path to ``data/categories/json/``.

        This is the directory that contains the generated JSON mirrors of
        the category data files.

        Returns:
            str: Absolute path to ``eved/data/categories/json``.

        Example:
            >>> from filepath import FilePath
            >>> FilePath().get_categories_json.endswith('json')
            True
        """
        return os.path.join(self.get_caterogies, CATEGORIES_TYPE_JSON)

    @property
    def get_books(self):
        """Return the absolute path to the Bible books map file.

        Returns:
            str: Absolute path to ``eved/data/books/map.py``.

        Example:
            >>> import os
            >>> from filepath import FilePath
            >>> os.path.isfile(FilePath().get_books)
            True
        """
        return os.path.join(self.get_data, BOOKS_FOLDER, 'map.py')

    @property
    def get_numbers(self):
        """Return the absolute path to the Hebrew numbers map file.

        Returns:
            str: Absolute path to ``eved/data/numbers/map.py``.

        Example:
            >>> import os
            >>> from filepath import FilePath
            >>> os.path.isfile(FilePath().get_numbers)
            True
        """
        return os.path.join(self.get_data, NUMBERS_FOLDER, 'map.py')
