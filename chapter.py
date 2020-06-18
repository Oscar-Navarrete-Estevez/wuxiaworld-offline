from utils import sanitize_string
import re
import logging
import os
import io


class Chapter:
    def __init__(self, title_html, link_prefix):
        self.raw_title = title_html
        self.raw_content = ""

        self.link = link_prefix
        self.number = ""
        self.title = ""
        self.chapter_content = ""
        logging.basicConfig(filename='chapters.log', level=logging.DEBUG)

    def process_raw_title(self):
        search = re.search(r'<a style="" href="(.*?)">(.*)<\/a>', self.raw_title)
        if search:
            self.link += search.group(1)
            self.title = sanitize_string(search.group(2))
            return search
        logging.warning(f'Failed to extract {self.raw_title} title!')
        return search

    # TODO unify extract and clean chapter in process_raw_chapter
    def extract_chapter(self):
        search = re.search(r'<div\sid="chaptercontent".*\n((.*\n)+)<amp-auto-ads', self.raw_content)
        if search:
            content = search.group(1)
            self.raw_content = content
            return content
        logging.warning(f'Chapter {self.title} is empty!')
        return search

    def clean_chapter(self):
        clean_chap = ""
        for line in self.raw_content.splitlines():
            if not line.startswith('<') and not line.startswith(' ') and not line.startswith('('):
                clean_chap = clean_chap + line
            elif line.startswith("<br/>"):
                clean_chap = clean_chap + '\n\n'
            self.chapter_content = clean_chap
            clean_chap = re.sub("<br\/>", "\n", self.chapter_content)
            self.chapter_content = clean_chap
        if not clean_chap:
            logging.warning(f'Failed to clean {self.title} content!')

    def save_chapter(self, abs_path):
        save_to = f"{abs_path}\\{self.title}.txt"
        #f = open(save_to, "w")
        #f.write(self.title + "\n\n")
        #for line in self.chapter_content.splitlines():
        #    f.write(line + "\n")
        #f.close()
        with io.open(save_to, "w", encoding="utf-8") as f:
            f.write(self.title)
            f.write("\n\n")
            f.write(self.chapter_content)

