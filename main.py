import sys
from book import Book
import json


def main():
    book = Book(sys.argv[1])
    book.download_chapters_list()
    book.download_chapters_content()
    #book.save_chapters()
    print("Finished")


main()
