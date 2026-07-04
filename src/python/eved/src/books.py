#!/usr/bin/env python3
"""
Main numbers map
"""
from filepath import FilePath
from filepath import eval_file


class Books(dict):

    def __init__(self, *arg, **kw):
        super(Books, self).__init__(*arg, **kw)
        self.file = self.get_books_path
        self.update(eval_file(self.file))

    @property
    def get_books_path(self):
        return FilePath().get_books

    @classmethod
    def get_book(cls, book):
        if book not in cls().book_list():
            raise NameError(f'Book name({book}) not found, allowed books: {Books.book_list()}')
        return cls()[book]

    @classmethod
    def book_list(cls):
        return list(cls().keys())


print(Books.get_book('1 Samuel'))
print(Books.book_list())
print(Books())
print(Books()['Numbers'])
print(Books.get_book('7 Samuel'))
