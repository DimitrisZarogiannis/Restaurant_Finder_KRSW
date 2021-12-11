from typing import List
from SPARQLWrapper import SPARQLWrapper, JSON, XML

def restaurant_query(city: str, radius: str) -> List:
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
    select ?lat ?long { <http://dbpedia.org/resource/"""+ city + """> geo:lat ?lat ; geo:long ?long }
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    latitude = results["results"]["bindings"][0]["lat"]["value"]
    longitude = results["results"]["bindings"][0]["long"]["value"]


    sparql = SPARQLWrapper("http://linkedgeodata.org/sparql")
    sparql.setQuery("""
        Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        Prefix ogc: <http://www.opengis.net/ont/geosparql#>
        Prefix geom: <http://geovocab.org/geometry#>
        Prefix lgdo: <http://linkedgeodata.org/ontology/>

        Select *
        From <http://linkedgeodata.org> {
                      ?s
                      a lgdo:Restaurant ;
                      rdfs:label ?l ;    
                      geom:geometry [
                      ogc:asWKT ?g
                      ] .

                      Filter(bif:st_intersects (?g, bif:st_point (""" + longitude + ""","""+latitude+""" ), """+radius+""")) .
                        }
                        LIMIT 50
          """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    restaurants = []
    for result in results["results"]["bindings"]:
        restaurants.append(result["l"]["value"])
    return restaurants


if __name__ == "__main__":
  print(restaurant_query('Athens','1'))
