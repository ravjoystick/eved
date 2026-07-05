#!/usr/bin/env python3
"""Filesystem path resolution and JSON generation utilities for the eved project.

This module provides the FilePath class, which resolves absolute paths to
every data directory and file the project uses, along with helper functions for
loading Python dict files via eval and for generating the JSON mirrors of
the category data.

Typical usage::

    from filepath import FilePath, create_all_jsons, eval_file

    fp = FilePath()
    print(fp.get_data)            # PosixPath('.../eved/data')
    print(fp.get_categories_json) # PosixPath('.../eved/data/categories/json')

    create_all_jsons()            # regenerate all 27 category JSON files
"""

import json
from pathlib import Path

# Root of the eved package — the directory that contains this file.
# filepath.py lives at  src/python/eved/filepath.py
# APP_ROOT resolves to  src/python/eved/
APP_ROOT = Path(__file__).resolve().parent

DATA_FOLDER = 'data'
TESTS_FOLDER = 'tests'
CATEGORIES_FOLDER = 'categories'
CATEGORIES_TYPE_PYTHON = 'python'
CATEGORIES_TYPE_JSON = 'json'
NUMBERS_FOLDER = 'numbers'
BOOKS_FOLDER = 'books'


def eval_file(filepath):
    """Read a .py file that contains a bare Python literal and return it.

    The category and map data files are stored as plain Python dicts (no
    assignment, just a literal).  This function reads those files and
    evaluates them with the built-in eval.

    Args:
        filepath (str | Path): Path to the Python literal file.

    Returns:
        Any: The Python object described in the file — typically a dict.

    Raises:
        FileNotFoundError: If filepath does not exist.
        SyntaxError: If the file content is not valid Python.

    Example:
        >>> from filepath import eval_file, FilePath
        >>> data = eval_file(FilePath().get_numbers)
        >>> data[1]['hebrew_say']
        'Alef'
    """
    return eval(Path(filepath).read_text(encoding='utf-8'))


def create_all_jsons():
    """Generate a JSON mirror for every category .py file.

    Reads every .py file under data/categories/python/, evaluates it
    as a Python dict, and writes the result as a formatted JSON file into
    data/categories/json/.  Existing JSON files are overwritten.

    Returns:
        list[Path]: Paths of every JSON file that was written.

    Raises:
        IOError: If the python categories folder does not exist.

    Example:
        >>> from filepath import create_all_jsons
        >>> written = create_all_jsons()
        >>> len(written) >= 27
        True
        >>> written[0].suffix
        '.json'
    """
    python_root = FilePath().get_categories_python
    if not python_root.exists():
        raise IOError('Python categories folder not found!')

    written = []
    for py_file in sorted(python_root.glob('*.py')):
        data = eval_file(py_file)
        written.append(_create_json(py_file, data))
    return written


def _create_json(filepath, data):
    """Write data to a JSON file named after the stem of filepath.

    The output file is placed in data/categories/json/ regardless of where
    filepath lives.  The filename is derived from filepath's stem.

    Args:
        filepath (str | Path): Path to the source .py file — used only to
            derive the output filename.
        data (dict): The Python dict to serialise as JSON.

    Returns:
        Path: Path of the JSON file that was written.

    Raises:
        IOError: If the JSON categories folder does not exist.

    Example:
        >>> from filepath import _create_json, FilePath
        >>> sample = {'name': 'test', 'verses': {}}
        >>> fake_py = FilePath().get_categories_python / 'jealous.py'
        >>> path = _create_json(fake_py, sample)
        >>> path.name
        'jealous.json'
    """
    json_root = FilePath().get_categories_json
    if not json_root.exists():
        raise IOError('JSON categories folder not found!')

    json_file = json_root / (Path(filepath).stem + '.json')
    json_file.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding='utf-8',
    )
    return json_file


class FilePath:
    """Resolves absolute paths to every data directory and file in the project.

    All paths are derived from the location of this module, so the project
    can be moved freely on disk without any hardcoded paths.  All properties
    return pathlib.Path objects.

    Attributes:
        root (Path): Absolute path to the eved package root directory
            (the folder that contains data/).

    Example:
        >>> from filepath import FilePath
        >>> fp = FilePath()
        >>> fp.get_data.name
        'data'
        >>> fp.get_categories_python.name
        'python'
    """

    def __init__(self):
        """Initialise FilePath with the package root resolved from this file."""
        self.root = APP_ROOT

    @property
    def get_root(self):
        """Return the absolute path to the eved package root.

        Returns:
            Path: Absolute path, e.g. Path('/path/to/src/python/eved').

        Example:
            >>> from pathlib import Path
            >>> from filepath import FilePath
            >>> isinstance(FilePath().get_root, Path)
            True
        """
        return self.root

    @property
    def get_data(self):
        """Return the absolute path to the data/ directory.

        Returns:
            Path: Absolute path to eved/data.

        Raises:
            ValueError: If the data/ directory does not exist.

        Example:
            >>> from filepath import FilePath
            >>> FilePath().get_data.is_dir()
            True
        """
        data = self.root / DATA_FOLDER
        if data.exists():
            return data
        raise ValueError('Missing data folder!')

    @property
    def get_tests(self):
        """Return the absolute path to the tests/ directory.

        Returns:
            Path: Absolute path to the tests directory.

        Raises:
            ValueError: If the tests/ directory does not exist.

        Example:
            >>> from filepath import FilePath
            >>> FilePath().get_tests.name
            'tests'
        """
        tests = self.root / TESTS_FOLDER
        if tests.exists():
            return tests
        raise ValueError('Missing tests folder!')

    @property
    def get_caterogies(self):
        """Return the absolute path to the data/categories/ directory.

        Returns:
            Path: Absolute path to eved/data/categories.

        Example:
            >>> from filepath import FilePath
            >>> FilePath().get_caterogies.name
            'categories'
        """
        return self.get_data / CATEGORIES_FOLDER

    @property
    def get_categories_python(self):
        """Return the absolute path to data/categories/python/.

        This is the directory that contains the authoritative Python dict
        files for every category.

        Returns:
            Path: Absolute path to eved/data/categories/python.

        Example:
            >>> from filepath import FilePath
            >>> FilePath().get_categories_python.name
            'python'
        """
        return self.get_caterogies / CATEGORIES_TYPE_PYTHON

    @property
    def get_categories_json(self):
        """Return the absolute path to data/categories/json/.

        This is the directory that contains the generated JSON mirrors of
        the category data files.

        Returns:
            Path: Absolute path to eved/data/categories/json.

        Example:
            >>> from filepath import FilePath
            >>> FilePath().get_categories_json.name
            'json'
        """
        return self.get_caterogies / CATEGORIES_TYPE_JSON

    @property
    def get_books(self):
        """Return the absolute path to the Bible books map file.

        Returns:
            Path: Absolute path to eved/data/books/map.py.

        Example:
            >>> from filepath import FilePath
            >>> FilePath().get_books.is_file()
            True
        """
        return self.get_data / BOOKS_FOLDER / 'map.py'

    @property
    def get_numbers(self):
        """Return the absolute path to the Hebrew numbers map file.

        Returns:
            Path: Absolute path to eved/data/numbers/map.py.

        Example:
            >>> from filepath import FilePath
            >>> FilePath().get_numbers.is_file()
            True
        """
        return self.get_data / NUMBERS_FOLDER / 'map.py'
