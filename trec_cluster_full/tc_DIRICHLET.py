import math


class DIRICHLET:

    def __init__(self, query_structure, document_structure, tuning_parameter):
        self.queries = query_structure
        self.documents = document_structure
        self.frequency_of_all_words_in_a_collection = self.freq_of_all_words()
        self.no_of_words_in_the_collection = self.no_of_words_in_collection()
        self.u = tuning_parameter

    def no_of_words_in_collection(self):
        summ = 0
        for para_id, ranked_words_dict in self.documents.items():
            summ += sum(ranked_words_dict.values())
        return summ

    def freq_of_all_words(self):
        """
        
        :return: 
        """
        freq_dict = dict()
        for para_id, ranked_words_dict in self.documents.items():
            for word, frequency in ranked_words_dict.items():
                if word in freq_dict:
                    freq_dict[word] += frequency
                else:
                    freq_dict[word] = frequency
        return freq_dict

    def word_frequency_of_word_in_document(self, word, document_id):
        """
        Returns the frequency of word in the document
        :param word: query term
        :param document_id: document id
        :return: frequency of the word in the document
        """
        ranked_words_dict = self.documents[document_id]
        if word in ranked_words_dict:
            return ranked_words_dict[word]
        else:
            return 0

    def document_score(self, query, document_id):
        """
        Returns the score given a query and a document
        :param query: query tup structure
        :param document_id: document id 
        :return: tup (query, document_id and score)
        """
        score = 0
        document_length = sum(self.documents[document_id].values())
        query_length = sum(query[2].values())
        part_one_calc = query_length * math.log(self.u / (document_length + self.u))
        for key, value in query[2].items():
            w = self.word_frequency_of_word_in_document(key, document_id)
            if key in self.frequency_of_all_words_in_a_collection:
                occurence_in_collection = self.frequency_of_all_words_in_a_collection[key]
            else:
                occurence_in_collection = 1.0
            inner_calc = ((w / self.u) * (self.no_of_words_in_the_collection / occurence_in_collection)) + 1.0
            score += query[2][key] * math.log(inner_calc)
        score += part_one_calc
        tup = (query[1], document_id, score)
        return tup
