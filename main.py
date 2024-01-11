from datetime import datetime
import json
import re
import requests
import pandas as pd

url = "https://www.elabastecedor.com.ar/"
routes_pattern = "<a href='([^']+)'><b>([^<]+)</b></a>"
products_pattern = "<form data-codigo='([^']+)' data-marca='([^']+)' data-nombre='([^']+)' data-id='([^']+)' data-precio='([^']+)' class='produItem' name='form1' method='post'>"
pagination_pattern = "class=\"active\"> \d+ </a></li><li> <a href=\"([^\"]+)\"> \d+ </a>"

def get_routes(filename):
    with requests.get(url) as response:
        response.raise_for_status()
        content = response.text
        cookie = response.headers["Set-Cookie"]
    
    routes_results = re.findall(routes_pattern, content)
    
    urls = {}
    for route_url, route_name in routes_results:
        urls[route_name.strip()] = url + route_url

    routes = dict(
        headers=dict(response.headers),
        urls=urls,
    )
    save_json(filename, routes)
    return cookie, urls

def save_json(filename, obj):
    with open(filename, "w") as file:
        json.dump(obj, file)
    
def get_products(cookie, urls):
    headers = {
        "Cookie": cookie,
        "Upgrade-Insecure-Requests": "1"
    }
    
    def _get_products(route_name, route_url):
        products = []
    
        print(route_url)
        with requests.get(url + route_url, headers=headers) as response:
            response.raise_for_status()
            content = response.text
    
        results = re.findall(products_pattern, content)
        for codigo, marca, nombre, id, precio in results:
            products.append(dict(
                id=id,
                codigo=codigo,
                marca=marca,
                nombre=nombre,
                precio=float(precio.replace(",", "")),
                categoria=route_name,
            ))
        
        pages = re.findall(pagination_pattern, content)
        if any(pages):
            products.extend(_get_products(route_name, pages[0]))
    
        return products
    
    products = []
    for route_name, route_url in urls.items():
        products.extend(_get_products(route_name, route_url))

    return products

def export_products(filename, products):
    df = pd.DataFrame(products)
    df.drop_duplicates(inplace=True)
    df.to_csv(filename, header=True, index=False)

def main():
    start_time = datetime.now()
    date = f"{start_time:%Y%m%d}"
    cookie, urls = get_routes(f"data/{date}_routes.json")
    products = get_products(cookie, urls)
    export_products(f"data/{date}_products.csv", products)

if __name__ == "__main__":
    main()
