import threading
from datetime import datetime
import requests
from os import path, mkdir
from progress.bar import Bar


def status(message):
    print("{0} {1}".format(datetime.now(), message))


def main():
    status("Fetching latest pastes...")

    current_request = requests.get("https://scrape.pastebin.com/api_scraping.php?limit=100")
    current_json = current_request.json()

    status("Fetched {0} items. Processing...".format(len(current_json)))
    skipped_pastes = 0

    for entry in current_json:
        path_t = path.join("files", "{0}.txt".format(entry["key"]))
        if path.isfile(path_t):
            skipped_pastes += 1

    with Bar("Processing", max=len(current_json) - skipped_pastes, fill=">") as bar:
        for entry in current_json:
            path_t = path.join("files", "{0}.txt".format(entry["key"]))
            if path.isfile(path_t):
                continue

            entry_request = requests.get("https://scrape.pastebin.com/api_scrape_item.php?i={0}"
                                         .format(entry["key"]))

            f = open(path_t, "w+")
            f.write(entry_request.text)
            f.close()

            bar.next()

        bar.finish()

        if skipped_pastes is not 0:
            status("Skipped {0} previously fetched pastes".format(skipped_pastes))

    status("Hibernating for 60 seconds...")
    print()
    threading.Timer(60, main).start()


if not path.isdir("files"):
    status("No file directory found, creating...")
    mkdir("files")

main()
