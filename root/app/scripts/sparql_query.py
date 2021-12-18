from typing import List
from SPARQLWrapper import SPARQLWrapper, JSON, XML
import re
import geopy.distance

# Query Linked Data(LinkedGeoData, DBpedia) SPARQL endpoints
def restaurant_query(city: str, radius: str) -> List:
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
    select ?lat ?long { <http://dbpedia.org/resource/"""+ city + """> geo:lat ?lat ; geo:long ?long }
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    latitude = results["results"]["bindings"][0]["lat"]["value"]
    longitude = results["results"]["bindings"][0]["long"]["value"]
    city_point = tuple([longitude, latitude])

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
                        LIMIT 30
          """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    restaurants = []
    for result in results["results"]["bindings"]:
        point = result['g']['value']
        match = tuple(re.findall(r'\d{2}.\d+', point))
        restaurants.append((result["l"]["value"], calculate_distance(city_point, match)))
        restaurants = sorted(restaurants, key = lambda l: l[1])
    return restaurants

#Calculate the distance between two geo points
def calculate_distance(point1: tuple, point2: tuple) -> float:
    distance = f'{geopy.distance.distance(point1, point2).m:.2f}'
    return float(distance)


if __name__ == "__main__":
  print(restaurant_query('Athens','1'))
