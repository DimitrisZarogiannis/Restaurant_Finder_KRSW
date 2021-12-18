# Application execution window 
# User inputs functionality

from re import findall
from scripts.sparql_query import restaurant_query


def inputs():
    user_input_City = input("Enter the City you want to search for:")
    user_input_radius = input("Enter the radius you want to search for (in km):")
    output = restaurant_query(user_input_City, user_input_radius)
    print(f"Restaurants in {user_input_radius} km radius from {user_input_City} centre: ")
    return output

def printer(out):
    for x in out:
        print(x[0],f' | {x[1]} meters from the city centre |')

if __name__== "__main__":
    out = inputs()
    printer(out)