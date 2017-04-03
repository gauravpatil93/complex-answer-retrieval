import math

class TDELTAIDF:

    def __init__(self, query_structure, document_structure):
        self.queries = query_structure
        self.documents = document_structure
        self.no_of_documents = len(self.documents)
        self.average_length_of_all_documents = self.average_document_length()
        self.k = 1.2
        self.b = 0.75
        self.delta = 1.0
        self.k_plus_one = self.k + 1
        self.cache = dict()

    def average_document_length(self):
        summ = 0
        for para_id, ranked_words_dict in self.documents.items():
            summ += sum(ranked_words_dict.values())
        return summ/float(self.no_of_documents)

    def modified_idf_calculation(self, query_word):
        result = math.log((self.no_of_documents + 1) / (self.no_of_documents_containing_a_word(query_word) + 0.5))
        return result

    def no_of_documents_containing_a_word(self, query_word):
        if query_word in self.cache:
            return self.cache[query_word]
        else:
            no_of_documents_having_the_word = 0
            for para_id, ranked_word_dict in self.documents.items():
                if query_word in ranked_word_dict:
                    no_of_documents_having_the_word += 1
            self.cache[query_word] = no_of_documents_having_the_word
            return float(no_of_documents_having_the_word)

    def word_frequency_of_word_in_document(self, word, document_id):
        ranked_words_dict = self.documents[document_id]
        if word in ranked_words_dict:
            return ranked_words_dict[word]
        else:
            return 0

    def t_delta_score(self, query, document_id):
        score = 0
        document_length = sum(self.documents[document_id].values())
        for key, value in query[2].items():
            w = self.word_frequency_of_word_in_document(key, document_id)
            d = 1 - self.b + self.b * (document_length / self.average_length_of_all_documents)
            w_by_plus_delta_ln = 1.0 + math.log((w / d) + self.delta)
            outer_ln = 1.0 + math.log(w_by_plus_delta_ln)
            score += self.modified_idf_calculation(key) * outer_ln
        tup = (query[1], document_id, score)
        return tup
