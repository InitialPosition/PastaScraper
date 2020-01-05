# PastaScraper
A script to scrape all the magic pastebin has to offer

### Usage
1. Make sure you have python installed. Run `python3 -V` in a terminal. If it shows a version number, you're good to go. Otherwise, download Python from the [official website](https://www.python.org/downloads/).
1. Head over to [Releases](https://github.com/Syrapt0r/PastaScraper/releases).
1. Download scraper.py.
1. Run the scraper by typing `python3 scraper.py` in your terminal.
1. s c r a p e

### Notes
Please be aware that you have to whitelist your IP address on the [Pastebin Scraper API website](https://pastebin.com/doc_scraping_api). I will not take responsibility if you get banned from the scraper API or if this script downloads a super virus to your hard drive.
You also have to install some modules for this script to work. You can do this by running `python3 -m pip install -r requirements.txt` in the repository directory.

### Parameters
Parameters are back baby

| Parameter | Optional? | Default | Effect |
| --------- | --------- | ------- | ------ |
| -k / --keywords | Yes | None | A file containing keywords to scrape for. One keyword per line. |
| -i / --infinite | Yes | No | Whether to run in infinite mode or in keyfile mode |

### Roadmap
- [X] Parameter input
