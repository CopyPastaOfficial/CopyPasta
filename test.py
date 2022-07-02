from requests import get
from json import loads
from bs4 import BeautifulSoup

#isbn = "3302740068027"
#isbn = "978209157545"
isbn = "3270220060949"

def identify_product(isbn:str):
    
    
    
    # edible product ?
    r = get(f"http://world.openfoodfacts.org/api/v0/product/{isbn}")
    r = loads(r.text)
    if "product" in r.keys():
        r = r["product"]
        
        return {"name":r["product_name"]+ " - "+r["brands"] if "brands" in r.keys() else r["product_name"] ,"url":f"https://world.openfoodfacts.org/product/{isbn}"}
    
    
    # book ?
    r = get(f"https://www.isbnsearcher.com/books/{isbn}",headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"})
    
    if r.status_code == 200:
        r = BeautifulSoup(r.text,"html.parser")
        
        return {"name":r.find("h1").get_text(),"url":f"https://www.isbnsearcher.com/books/{isbn}"}
    
    else:
        return {"name":isbn,"url":f"https://www.google.com/search?q={isbn}"}
    
#print(identify_product(isbn))
# amazon lookup
r = get("https://www.amazon.fr/s?k=9782091575452",headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"},allow_redirects=True)
