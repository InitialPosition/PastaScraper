import threading
from datetime import datetime
import requests
from os import path, mkdir, walk
import argparse

try:
    from progress.bar import Bar

except ModuleNotFoundError:
    print("Could not find the progress module. Run \"python3 -m pip install progress\" to install it.")
    exit(0)


# print a message with a time stamp
def status(message):
    print("{0} {1}".format(datetime.now(), message))


# main loop
def main():
    status("Fetching latest pastes...")

    # fetch latest 100 paste IDs
    fetch_limit = 100

    current_request = requests.get("https://scrape.pastebin.com/api_scraping.php?limit={0}".format(fetch_limit))
    current_json = current_request.json()

    status("Pastes fetched. Processing...")
    skipped_pastes = 0

    # determine how many new pastes we have to fetch
    for entry in current_json:
        if entry["key"] in paste_ids:
            skipped_pastes += 1

    # create a progress bar and start downloading pastes
    with Bar("Processing", max=len(current_json) - skipped_pastes, fill=">") as bar:
        for entry in current_json:
            path_t_important = path.join("files", "{0}.txt".format(entry["key"]))

            # this file was already downloaded, skipping
            if entry["key"] in paste_ids:
                continue

            # download the raw paste data
            entry_request = requests.get("https://scrape.pastebin.com/api_scrape_item.php?i={0}"
                                         .format(entry["key"]))

            entry_content = entry_request.text

            paste_ids.append(entry["key"])

            # if we have a provided keyword list, check for keywords
            if keywords is not None:
                for keyword in keywords:
                    if keyword.upper() in entry_content.upper():
                        print(" [KEYWORD] Paste \'{0}\' contains keyword \'{1}\'".format(entry["key"], keyword))

                        entry_file = open(path_t_important, "w+")
                        entry_file.write(entry_content)
                        entry_file.close()

                        break
            else:
                entry_file = open(path_t_important, "w+")
                entry_file.write(entry_content)
                entry_file.close()

            bar.next()

    bar.finish()

    if skipped_pastes is not 0:
        status("Skipped {0} previously fetched pastes".format(skipped_pastes))

    status("Cleaning up internal ID list...")
    while len(paste_ids) > 100:
        paste_ids.pop(0)

    # start 60 second loop
    status("Hibernating for 60 seconds...")
    print()
    threading.Timer(60, main).start()


if __name__ == '__main__':

    AUTHOR = "SYRAPT0R"
    COPYRIGHT = "2019"
    VERSION = "0.3.0"

    status("STARTING PASTA SCRAPER {0}, (c) {1} {2}".format(VERSION, COPYRIGHT, AUTHOR))
    print()

    # make sure file directories exists
    if not path.isdir("files"):
        status("No file directory found, creating...")
        mkdir("files")

    # parse arguments
    keywords = None

    parser = argparse.ArgumentParser(description="A script to scrape pastebin.com with optional keyword search")

    parser.add_argument("-k", "--keywords", help="A file containing keywords for the search")

    args = parser.parse_args()

    if args.keywords is not None:
        f = open(args.keywords)
        keywords = f.readlines()
        f.close()

        keywords = [keyword.strip() for keyword in keywords]

        status("Loaded {0} keywords".format(len(keywords)))

    # create paste ID index
    paste_ids = []

    # preparation done, enter main loop
    status("Entering main loop...")
    print()

    main()
