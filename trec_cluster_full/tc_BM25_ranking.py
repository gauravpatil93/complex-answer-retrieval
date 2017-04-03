import math


class BM25:

    def __init__(self, query_structure, document_structure):
        """
        Constructor takes the query structure and the document structure
        :param query_structure: tuple (query_id_plain, query_id_formatted, Ranked dict of words))
        :param document_structure: dictionary  consisting of document id mapping to the ranked dict of words
        """
        self.queries = query_structure
        self.documents = document_structure
        self.no_of_documents = len(self.documents.keys())
        self.average_length_of_all_documents = self.average_length_of_documents()
        self.k = 1.2
        self.b = 0.75
        self.k_plus_one = self.k + 1

    def average_length_of_documents(self):
        """
        Calculates the the average length of documents
        :return: average length of documents
        """
        summ = 0
        for key, value in self.documents.items():
            for k, v in value.items():
                summ += v
        return summ/float(self.no_of_documents)

    def inverse_document_frequency(self, query_word):
        no_qi = self.no_of_documents_containing_a_word(query_word)
        return float(math.log(self.no_of_documents / (no_qi + 1.0)))

    def no_of_documents_containing_a_word(self, query_word):
        count = 0
        for key, value in self.documents.items():
            if query_word in value:
                count += 1
        return float(count)

    def word_frequency_of_word_in_document(self, word, document_id):
        if word in self.documents[document_id]:
            return self.documents[document_id][word]
        else:
            return 0

    def bm25_score(self, query, document_id):
        score = 0
        document_length = 0
        for k, v in self.documents[document_id].items():
            document_length += v
        for key, value in query[2].items():
            term_freq = self.word_frequency_of_word_in_document(key, document_id)
            score += self.inverse_document_frequency(key) * (self.k_plus_one * term_freq) / \
                     (self.k * (1.0 - self.b + self.b * (document_length/ self.average_length_of_all_documents))
                      + term_freq )
        tup = (query[1], document_id, score)
        return tup