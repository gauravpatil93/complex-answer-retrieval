import itertools
from trec_car.format_runs import *
from trec_car.read_data import *
from pprint import pprint
from nltk.corpus import stopwords
import re
from stemming.porter2 import stem


class Ranking:

    stop_words = stopwords.words('english')

    def __init__(self, outline_file: str, paragraph_file: str, output_file: str):
        self.outline_file = outline_file
        self.paragraph_file = paragraph_file
        self.output_file = output_file
        self.pages = self.get_pages()
        self.queries = self.get_queries()
        self.paragraphs = self.get_paragraphs()

    def get_pages(self):
        with open(self.outline_file, 'rb') as f:
            pages = [p for p in itertools.islice(iter_annotations(f), 0, 1000)]
        return pages

    def get_paragraphs(self):
        id_to_text_dict = dict()
        with open(self.paragraph_file, 'rb') as f:
            for p in itertools.islice(iter_paragraphs(f), 0, 500):
                id_to_text_dict[p.para_id] = Ranking.process_text(p.get_text())
        pprint(id_to_text_dict)
        return id_to_text_dict

    @staticmethod
    def process_text(input_text: str):
        # Convert characters to lower case
        input_text_to_lower = input_text.lower()
        # Remove special characters from the string
        input_text_to_lower = re.sub('[^a-zA-Z0-9 \n]', '', input_text_to_lower)
        # Remove common words using list of stop words
        filtered_words_list = [word for word in input_text_to_lower.split() if word not in Ranking.stop_words]
        # Stem the list of words
        filtered_words_list = [stem(word) for word in filtered_words_list]
        # Word ranking
        ranked_dict = dict()
        for word in filtered_words_list:
            if word in ranked_dict:
                ranked_dict[word] += 1
            else:
                ranked_dict[word] = 1
        return ranked_dict

    def get_queries(self):
        for page in self.pages:
            for section_path in page.flat_headings_list():
                query_id_plain = " ".join([page.page_name] + [section.heading for section in section_path])








#pprint(Ranking.process_text("According to the OECD NEA report on Chernobyl (ten years on), the following proportions of the core inventory were released."))
obj =  Ranking("spritzer.cbor.outlines", "spritzer.cbor.paragraphs", "output.run")
#print(Ranking.process_text("According to the OECD NEA report on Chernobyl (ten years on), the following proportions of the core inventory were released.").split())