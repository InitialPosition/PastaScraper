import threading
from datetime import datetime
import requests
from os import path, mkdir
import argparse
from sys import modules

try:
    from progress.bar import Bar

except ModuleNotFoundError:
    print("Make sure the progress module is installed.")
    exit(0)


def status(message):
    print("{0} {1}".format(datetime.now(), message))


def main():
    status("Fetching latest pastes...")

    # fetch latest 100 pastes
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
            path_t_important = path.join("files_important", "{0}.txt".format(entry["key"]))

            if path.isfile(path_t):
                continue

            entry_request = requests.get("https://scrape.pastebin.com/api_scrape_item.php?i={0}"
                                         .format(entry["key"]))

            entry_content = entry_request.text

            entry_file = open(path_t, "w+")
            entry_file.write(entry_content)
            entry_file.close()

            if keywords is not None:
                for keyword in keywords:
                    if keyword.upper() in entry_content.upper():
                        print(" [KEYWORD] Paste \'{0}\' contains keyword \'{1}\'".format(entry["key"], keyword))

                        entry_file = open(path_t_important, "w+")
                        entry_file.write(entry_content)
                        entry_file.close()

                        break

            bar.next()

    bar.finish()

    if skipped_pastes is not 0:
        status("Skipped {0} previously fetched pastes".format(skipped_pastes))

    status("Hibernating for 60 seconds...")
    print()
    threading.Timer(60, main).start()


# make sure file directories exists
if not path.isdir("files"):
    status("No file directory found, creating...")
    mkdir("files")

if not path.isdir("files_important"):
    status("No important file directory found, creating...")
    mkdir("files_important")

# parse arguments
keywords = None

parser = argparse.ArgumentParser(description="A script to scrape pastebin.com with optional keyword search")
parser.add_argument("--keywords", "-k", help="A file containing keywords for the search")
args = parser.parse_args()

if args.keywords is not None:
    f = open(args.keywords)
    keywords = f.readlines()
    f.close()

    keywords = [keyword.strip() for keyword in keywords]

    status("Loaded {0} keywords".format(len(keywords)))

main()
