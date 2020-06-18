from chapter import Chapter
from utils import download_content, sanitize_string
import re
import time
import random
import logging
from pathlib import Path
import os


class Book:
    def __init__(self, title_html):
        self.index_iri = title_html
        self.chapter_list = []
        self.title = sanitize_string(re.search(r'https://m.wuxiaworld.co/(.*)/all.html', title_html).group(1))
        logging.basicConfig(filename='book.log', level=logging.DEBUG)

    def download_chapters_list(self):
        html = download_content(self.index_iri)
        page_prefix = self.index_iri.replace("all.html", "")
        search = re.findall(r'<a style="" href=".*?<\/a>', html)
        if search:
            for title_html in search:
                self.chapter_list.append(Chapter(title_html, page_prefix))
        else:
            logging.error(f'Failed to fetch this books chapter list from {self.index_iri}')
        # TODO delete this line
        self.chapter_list = self.chapter_list[2088:]
        return search

    def download_chapters_content(self):
        # To avoid being detected as a script(?)
        random.seed()
        #Create directory where to save chapters
        Path(f"{self.title}").mkdir(parents=True, exist_ok=True)
        abs_file_path = os.path.abspath(f'.\\{self.title}')
        for chapter in self.chapter_list:
            chapter.process_raw_title()
            logging.info(f'Downloading {chapter.title}')
            print(f'Downloading {chapter.title}')
            chapter.raw_content = download_content(chapter.link)
            chapter.extract_chapter()
            chapter.clean_chapter()
            chapter.save_chapter(abs_file_path)
            time.sleep(random.randrange(5))


    def save_chapters(self):
        for chapter in self.chapter_list:
            logging.debug(f'Saving {chapter.title}')
            chapter.save_chapter(self.title)
