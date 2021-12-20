import urllib.request
import re

def search_youtube(keyword):
    pattern = r"/watch\?v=(\S{11})"
    url = f"https://www.youtube.com/results?search_query={keyword}"

    html = urllib.request.urlopen(url)
    html = html.read().decode()
    ids = re.findall(pattern, html)

    results = [f"https://www.youtube.com/watch?v={id}" for id in ids]
    embeded = [f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>' for id in ids]

    return results, embeded

