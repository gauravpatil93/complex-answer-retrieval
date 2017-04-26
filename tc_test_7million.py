from tc_modified_ranking_7million import PartialRanking

ranking_object = PartialRanking("all.test200.cbor.outlines", "all.test200.cbor.paragraphs", 1000)

ranking_object.gather_queries()
ranking_object.gather_paragraphs()

