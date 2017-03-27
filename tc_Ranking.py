from trec_car.read_data import *
from nltk.corpus import stopwords
import re
from stemming.porter2 import stem


class Ranking:

    stop_words = stopwords.words('english')

    def __init__(self, outline_file, paragraph_file, output_file):
        self.outline_file = outline_file
        self.paragraph_file = paragraph_file
        self.output_file = output_file
        self.pages = self.gather_pages()
        self.queries = self.gather_queries()
        self.paragraphs = self.gather_paragraphs()

    def gather_pages(self):
        with open(self.outline_file, 'rb') as f:
            pages = [p for p in itertools.islice(iter_annotations(f), 0, 1000)]
        return pages

    def gather_paragraphs(self):
        id_to_text_dict = dict()
        with open(self.paragraph_file, 'rb') as f:
            for p in itertools.islice(iter_paragraphs(f), 0, 1000):
                id_to_text_dict[p.para_id] = Ranking.process_text(p.get_text())
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

    def gather_queries(self):
        query_tup_list = []
        for page in self.pages:
            for section_path in page.flat_headings_list():
                query_id_plain = " ".join([page.page_name] + [section.heading for section in section_path])
                query_id_formatted = "/".join([page.page_id] + [section.headingId for section in section_path])
                tup = (query_id_plain, query_id_formatted, Ranking.process_text(query_id_plain))
                query_tup_list.append(tup)
        return query_tup_list

    def get_queries(self):
        return self.queries

    def get_paragraphs(self):
        return self.paragraphs
