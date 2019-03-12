## File to download images for deep learning training using bing image search
bing_key_1='1ebb8bc96d5a41a29e6030a9b0932642'
bing_key_2 = 'b41d1be5be94e5b8a7fc2b13bc95b1b'

from requests import exceptions
import argparse
import requests
import cv2
import os

bing_key_1='1ebb8bc96d5a41a29e6030a9b0932642'
bing_key_2 = 'b41d1be5be94e5b8a7fc2b13bc95b1b'
API_KEY = bing_key_1
MAX_RESULTS = 250
GROUP_SIZE = 50
# set the endpoint API URL
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
# when attempting to download images from the web both the Python
# programming language and the requests library have a number of
# exceptions that can be thrown so let's build a list of them now
# so we can filter on them
EXCEPTIONS = set([IOError, FileNotFoundError,
	exceptions.RequestException, exceptions.HTTPError,
	exceptions.ConnectionError, exceptions.Timeout])`

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

 to (quickly) build a deep learning image datasetPython
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
# loop over the estimated number of results in `GROUP_SIZE` groups
55
56
57
58
59
60
61
62
63
64
65
66

