#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime

prefix = f"data/{datetime.now():%Y%m%d}"
print(prefix)


# In[ ]:


import requests

url = "https://www.elabastecedor.com.ar/"

with requests.get(url) as response:
    response.raise_for_status()
    content = response.text
    cookie = response.headers["Set-Cookie"]


# In[ ]:


import re

routes_results = re.findall("<a href='([^']+)'><b>([^<]+)</b></a>", content)


# In[ ]:


routes = {}
for route_url, route_name in routes_results:
    routes[route_name.strip()] = route_url


# In[ ]:


headers = {
    "Cookie": cookie,
    "Upgrade-Insecure-Requests": "1"
}


# In[ ]:


def get_products(route_name, route_url):
    products = []

    print(route_url)
    with requests.get(url + route_url, headers=headers) as response:
        response.raise_for_status()
        content = response.text
        
    products_pattern = "<form data-codigo='([^']+)' data-marca='([^']+)' data-nombre='([^']+)' data-id='([^']+)' data-precio='([^']+)' class='produItem' name='form1' method='post'>"
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
        
    pagination_pattern = "class=\"active\"> \d+ </a></li><li> <a href=\"([^\"]+)\"> \d+ </a>"
    pages = re.findall(pagination_pattern, content)
    if any(pages):
        products.extend(get_products(route_name, pages[0]))

    return products

products = []
for route_name, route_url in routes.items():
    products.extend(get_products(route_name, route_url))


# In[ ]:


import pandas as pd

df = pd.DataFrame(products)
df.drop_duplicates(inplace=True)
df.to_csv(f"{prefix}_products.csv", header=True, index=False)

