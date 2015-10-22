# WikiCrawler
Python program to map out connections between Wikipedia pages.

Upon running `wikicrawler3.py`, it will choose a random page on wikipedia and start there. If you specify a page title as the first command-line argument (i.e. `python wikicrawler3.py Tristen_da_Cunha`), the crawler will start there. It then parses the page and attempts to scrape all the hyperlinks to other wikipedia pages within the body of the page. It will select the first hyperlink as the next page to load, and repeats the process until the program is killed (<kbd>ctrl</kbd>-<kbd>c</kbd> usually works). If it encounters a page it has already visited, or reaches Philosophy, it chooses a new random page and continues the loop.

All data is saved in SQLite3 format in `wiki.db`, which is designed to be parsed by `WikiToFlowchart.py`. Running this program requires the [Graph-Tool](https://graph-tool.skewed.de/) library to generate an image of a flowchart showing how each article is connected. It removes all pages not connected to Philosophy due to limitations in the library. This image is then saved as `output.png`, an example is included in this repository.

A few problems exist. Notably, if unicode is present in the article title, the program crashes, but no data is lost. Additionally, since some articles list the etymology of a certain word, or have some valid link in the sidebar, the parser cannot differentiate between these links and sometimes chooses an unintended path.
