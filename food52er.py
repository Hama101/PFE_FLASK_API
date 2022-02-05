import urllib.request
import re

def search_food52(keyword):
    keyword = keyword.replace(' ', '+')
    pattern = r'/recipes/([0-9]{3,5})-'
    url = f"https://food52.com/recipes/search?q={keyword}"
   
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req)
    html = html.read().decode()
    ids = list(re.findall(pattern, html))
    
    links = [f"https://food52.com/recipes/{id}" for id in ids[:-1]]
    return links[:15]
