import lxml  # noqa: F401
from bs4 import BeautifulSoup
from httpx import get
from os import makedirs

def main():
    site_map_resp = get("https://pybit.es/post-sitemap1.xml")
    soup = BeautifulSoup(site_map_resp.content, 'xml')
    articles = [ loc_tag.get_text() for loc_tag in soup.find_all('loc') ]
    makedirs("pybites-articles", exist_ok=True)

    for article in articles[1:]:
        title_url_chunk = article.split('/')[4]
        if"https://pybit.es/wp-content/uploads" in article:
           continue 
        article_resp = get(article)
        print(f"Downloading article: {title_url_chunk}")
        article_filename = f"pybites-articles/{title_url_chunk}"
        with open(article_filename, "w") as fp:
            fp.write(article_resp.text)




if __name__ == "__main__":
    main()
