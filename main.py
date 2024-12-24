import datetime
import requests
from bs4 import BeautifulSoup

URL = "https://www.zdf.de/filme/spielfilm-highlights"

def download(url):
    '''Download the content of a webpage.'''
    web = requests.get(url)
    return web

def dump(code):
    '''Dump the content of a webpage to a file.'''
    with open("dump.html", "w", encoding="utf-8") as f:
        f.write(code)

def generate_entry(url, title, laufzeit, vdate):
    '''Generate a wiki entry for a movie.'''
    return f"""\n;[[{title}]]\n<pre>* {{{{Mediathek\n  |url={url}\n  |titel={title}\n  |sender=[[ZDF]]\n  |laufzeit={laufzeit}\n  |vdatum={vdate}\n  }}}}</pre>"""

def scrape_availability(soup):
    '''Scrape the availability of a movie, returns a datetime.date object.'''
    availability = soup.find("dd", attrs={"class": "desc-text"})
    day, month, year = availability.text.split(",")[0].split(" bis ")[1].split(".")
    return datetime.date(int(year), int(month), int(day))

def scrape_runtime(soup):
    '''Scrape the runtime of a movie.'''
    runtime = soup.find("dd", attrs={"class": "teaser-info"})
    return runtime.text.split(" min")[0]

def scrape_title(soup):
    '''Scrape the title of a movie.'''
    title = soup.find("h1", attrs={"class": "big-headline"})
    return title.text.strip("\n ")

def main():
    '''Main function.'''
    # Get the content of the webpage with the movie links
    web = download(URL)
    dump(web.text)

    # Get the movie urls
    soup = BeautifulSoup(web.text, "html5lib")
    movie_links = list(set(["https://www.zdf.de" + item["href"].split("#")[0] for item in soup.find_all("a") if "/spielfilm" in item["href"]]))
    movie_links.remove("https://www.zdf.de/filme/spielfilm-highlights")
    print("\n" + str(len(movie_links)) + " links to movies found.")
    movie_links.sort()

    # scrape the movie information and generate the wiki entries
    for movie_link in movie_links:
        web = download(movie_link)
        dump(web.text)
        soup = BeautifulSoup(web.text, "html5lib")
        title = scrape_title(soup)
        runtime = scrape_runtime(soup)
        try:
            availability_date = scrape_availability(soup)
            print(generate_entry(movie_link, title, runtime, availability_date))
        except IndexError:
            pass

if  __name__ == "__main__":
    main()