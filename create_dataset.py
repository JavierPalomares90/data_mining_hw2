## File to download images for deep learning training using bing image search
bing_key_1='1ebb8bc96d5a41a29e6030a9b0932642'
bing_key_2 = 'b41d1be5be94e5b8a7fc2b13bc95b1b'

import argparse
import imageio
# import opencv as cv2
import os

import requests
from requests import exceptions

bing_key_1='1ebb8bc96d5a41a29e6030a9b0932642'
bing_key_2 = 'b41d1be5be94e5b8a7fc2b13bc95b1b'
API_KEY = bing_key_1
MAX_RESULTS = 1000
GROUP_SIZE = 50
# set the endpoint API URL
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

# when attempting to download images from the web both the Python
# programming language and the requests library have a number of
# exceptions that can be thrown so let's build a list of them now
# so we can filter on them
EXCEPTIONS = set([IOError, FileNotFoundError,
				  exceptions.RequestException, exceptions.HTTPError,
				  exceptions.ConnectionError, exceptions.Timeout])

def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--query", required=True,
        help="search query to search Bing Image API for")
    ap.add_argument("-o", "--output", required=True,
        help="path to output directory of images")
    args = vars(ap.parse_args())


    # store the search term in a convenience variable then set the
    # headers and search parameters
    term = args["query"]
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    params = {"q": term, "offset": 0, "count": GROUP_SIZE}

    # make the search
    print("[INFO] searching Bing API for '{}'".format(term))
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()

    # grab the results from the search, including the total number of
    # estimated results returned by the Bing API
    results = search.json()
    estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
    print("[INFO] {} total results for '{}'".format(estNumResults,
                                                    term))

    # initialize the total number of images downloaded thus far
    total = 0

    # loop over the estimated number of results in `GROUP_SIZE` groups
    for offset in range(0, estNumResults, GROUP_SIZE):
        # update the search parameters using the current offset, then
        # make the request to fetch the results
        print("[INFO] making request for group {}-{} of {}...".format(
            offset, offset + GROUP_SIZE, estNumResults))
        params["offset"] = offset
        search = requests.get(URL, headers=headers, params=params)
        search.raise_for_status()
        results = search.json()
        print("[INFO] saving images for group {}-{} of {}...".format(
            offset, offset + GROUP_SIZE, estNumResults))
        # loop over the results
        for v in results["value"]:
            # try to download the image
            try:
                # make a request to download the image
                print("[INFO] fetching: {}".format(v["contentUrl"]))
                r = requests.get(v["contentUrl"], timeout=30)

                # build the path to the output image
                ext = v["contentUrl"][v["contentUrl"].rfind("."):]
                p = os.path.sep.join([args["output"], "{}{}".format(
                    str(total).zfill(8), ext)])

                # write the image to disk
                f = open(p, "wb")
                f.write(r.content)
                f.close()

            # catch any errors that would not unable us to download the
            # image
            except Exception as e:
                # check to see if our exception is in our list of
                # exceptions to check for
                if type(e) in EXCEPTIONS:
                    print("[INFO] skipping: {}".format(v["contentUrl"]))
                    continue

            # update the counter
            total += 1

if __name__ == "__main__":
	main()
