from bs4 import BeautifulSoup
from preprocessing.scrapers import lolesports

def main():
    lolesports.scrape()
        
if __name__ == "__main__":
    main();