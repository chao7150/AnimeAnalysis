from SPARQLWrapper import SPARQLWrapper

sparql = SPARQLWrapper(endpoint='http://ja.dbpedia.org/sparql', returnFormat='json')
sparql.setQuery("""                                                                                                                                                                      
    PREFIX dbpedia-owl:  <http://dbpedia.org/ontology/>                                                                                                                                  
    SELECT ?pref WHERE {                                                                                                                                                                 
    ?pref dbpedia-owl:wikiPageWikiLink category-ja:日本の都道府県.  }                                                                                                                    
""")
results = sparql.query().convert()
print(results)