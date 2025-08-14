import lxml  # noqa: F401
from bs4 import BeautifulSoup
from httpx import get
from os import makedirs
from textstat import flesch_kincaid_grade

def main():
    site_map_resp = get("https://pybit.es/post-sitemap1.xml")
    xsoup = BeautifulSoup(site_map_resp.content, 'xml')
    articles = [ loc_tag.get_text() for loc_tag in xsoup.find_all('loc') ]
    makedirs("pybites-articles", exist_ok=True)

    for article in articles[1:]:
        title_url_chunk = article.split('/')[4]
        if"https://pybit.es/wp-content/uploads" in article:
           continue 
        article_resp = get(article)
        hsoup = BeautifulSoup(article_resp.content, 'html.parser')
        article_filename = f"pybites-articles/{title_url_chunk}"
        rounded_flesch_kincaid_grade_level = round(flesch_kincaid_grade("".join(hsoup.stripped_strings)))
        print(f"According to the Flesch/Kincaid Grade, Pybites article {article_filename} is readable by a {rounded_flesch_kincaid_grade_level} grader.")




if __name__ == "__main__":
    main()
