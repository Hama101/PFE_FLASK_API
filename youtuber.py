import urllib.request
import re

def search_youtube(keyword):
    keyword += " recipes"
    keyword = keyword.replace(' ', '+')
    pattern = r"/watch\?v=(\S{11})"
    url = f"https://www.youtube.com/results?search_query={keyword}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    html = urllib.request.urlopen(req)
    html = html.read().decode()
    ids = list(re.findall(pattern, html))
    #reversed the list 
    ids = ids[:-1]
    # results = [f"https://www.youtube.com/watch?v={id}" for id in ids]
    embeded = [f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>' for id in ids]

    #return results[:3], embeded[:3]
    return embeded[:6]
