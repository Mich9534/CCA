# This is our first Google-Scholar web scraping project.

_CCA_scraper-py_ is the main file to use. The other three are older version which are used for testing purposes only.

CCA_scraper is respondibles of three main tasks:

- **CCA affiliates Finder:** it goes on Google Scholar and finds all the CCA affiliates whose are registered on the site;
- **Paper Scraper:** for each affilate it searches all the paper with at lest one citation or for which exists a publication date;
- **Paper Saver:** saves all the _good_ paper for each affilate;

## Further Developments: 
we could adapt the code to more sophisticated librarires. Selenium is the current library, but other libraries exisist such as PyScraper and BeautifulSoup.
One idea might be to make it more scalable to be applied to different type of data. Otherwise we might also push further this project, extracting for each
afiliates its co-author (internal to CCA or also external) and trying to represents all the publications as a network. We could then perform some network analyses as
community detection (here I could also use the sampler implemented for my M.Sc. thesis).
