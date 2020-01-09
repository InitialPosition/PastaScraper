import argparse
import threading
from datetime import datetime
from json import decoder
from os import path, mkdir
from os.path import isfile

try:
    from progress.bar import Bar
    import requests
    import termcolor

except ImportError:
    print("You are missing modules. Run \"python3 -m pip install -r requirements.txt --user\" to "
          "install them.")
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

    current_json = []
    try:
        current_json = current_request.json()

    except decoder.JSONDecodeError:
        status(termcolor.colored("Unable to fetch latest pastes. Make sure your IP is whitelisted at "
                                 "https://pastebin.com/doc_scraping_api", "red"))
        exit(0)

    status("Pastes fetched. Processing...")

    # clean up fetched ids
    cleaned_json = []
    for entry in current_json:
        if entry["key"] not in paste_ids:
            cleaned_json.append(entry)

    # create a progress bar and start downloading pastes
    with Bar("Processing", max=len(cleaned_json), fill=">") as bar:
        for entry in cleaned_json:
            # download the raw paste data
            entry_request = requests.get("https://scrape.pastebin.com/api_scrape_item.php?i={0}"
                                         .format(entry["key"]))

            entry_content = entry_request.text
            path_t_important = path.join("files", "{0}.txt".format(entry["key"]))

            paste_ids.append(entry["key"])
            # if we have a provided keyword list, check for keywords
            if keywords is not None:
                for keyword in keywords:
                    if keyword.upper() in entry_content.upper():
                        print(termcolor.colored(" [KEYWORD] Paste \'{0}\' contains keyword \'{1}\'".format(entry["key"]
                                                                                                           , keyword)
                                                , "green"))

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

    if args.infinite is False:
        if not isfile("runfile"):
            print()
            status("Runfile no longer found, exiting...")
            exit(0)

    skipped_pastes = fetch_limit - len(cleaned_json)
    if skipped_pastes is not 0:
        status("Skipped {0} previously fetched pastes".format(skipped_pastes))

    status("Cleaning up internal ID list...")
    while len(paste_ids) > max_id_list_size:
        paste_ids.pop(0)

    # start 60 second loop
    status("Hibernating for 60 seconds...")
    print()
    threading.Timer(60, main).start()


if __name__ == '__main__':

    AUTHOR = "SYRAPT0R"
    COPYRIGHT = "2019-2020"
    VERSION = "0.4.4"

    status("STARTING PASTA SCRAPER {0}, (c) {1} {2}".format(VERSION, COPYRIGHT, AUTHOR))
    print()

    # make sure file directories exists
    if not path.isdir("files"):
        status(termcolor.colored("No file directory found, creating...", "yellow"))
        mkdir("files")

    # parse arguments
    keywords = None

    parser = argparse.ArgumentParser(description="A script to scrape pastebin.com with optional keyword search")

    parser.add_argument("-k", "--keywords", help="A file containing keywords for the search")
    parser.add_argument("-i", "--infinite", help="Whether to run in infinite mode.", action="store_true")

    args = parser.parse_args()

    # create non infinite file if needed
    if args.infinite is False:
        status("Creating run file...")
        f = open("runfile", "w+")
        f.close()
    else:
        status("Running in infinite mode...")

    if args.keywords is not None:
        f = open(args.keywords)
        keywords = f.readlines()
        f.close()

        keywords = [keyword.strip() for keyword in keywords]

        status("Loaded {0} keywords".format(len(keywords)))

    # create paste ID index
    paste_ids = []
    max_id_list_size = 200

    # preparation done, enter main loop
    status("Entering main loop...")
    print()

    main()
