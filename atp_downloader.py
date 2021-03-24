"""
TODO: Some meaningful header here
Author: Stephen Kim
Date: Feb 23rd, 2017
"""

import datetime
import os
import sys

DIRECTORY="out/"
PREFIX="atp"
SUFFIX=".mp3"
DEBUG=False

"""
Prints data as long as DEBUG flag is true
"""
def dprint(data):
    if DEBUG:
        print(data)

"""
Creates a list of all files in a given directory that aren't hidden
"""
def listdir_nohidden(path):
    return list(listdir_nohiddenhelper(path))

"""
Creates a list generator for all files in a given directory that aren't hidden
"""
def listdir_nohiddenhelper(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

"""
Assumes DIREC/eTORY variables points to a directory comprising entirely files
that begin with PREFIX and end with SUFFIX. 

Gets all of the files in that directory then trims the file until it just 
has the numbers of each file. Return the max number of that list which will
be the number of the last episode

TODO: this function may need to be reworked depending on how a proper 
implementation of download_persist works
"""
def get_last_ep():
    filenames = listdir_nohidden(DIRECTORY)
    # removes prefixes
    filenames = list(s[len(PREFIX):] for s in filenames)
    dprint(filenames)
    # removes suffixes
    filenames = list(s[:-len(SUFFIX)] for s in filenames)
    dprint(filenames)
    filenames = list(int(s) for s in filenames)
    last_ep = max(filenames)
    return last_ep

"""
Downloads the stream to an mp3 file

The downloader is just a curl command. Nothing fancy

TODO: actually make this a persistent downloader. In situations where the
stream is congested or the connection cuts out for some reason it would be nice
to continue to download the stream. A tool to stitch together mp3 files
together would be necessary to achieve this. If this were to happen it might
also require get_last_ep function to be reworked to deal with interim files
"""
def download_persist():
    cutoff_time = datetime.datetime.now().replace(hour=0, minute=30,
        second=0, microsecond=0)
    current_ep = get_last_ep() + 1
    ep_portion = 0
    dprint(current_ep)
    ep_name = DIRECTORY + "atp" + str(current_ep) + "-" + str(ep_portion) + \
        ".mp3"
    command = "curl -o " + ep_name + " https://atp.fm:8443/listen"
    #while(datetime.datetime.now() < cutoff_time):
    os.system(command)
    dprint(os.path.getsize(ep_name))

def main():
    dprint("hello world")
    download_persist()

if __name__ == "__main__":
    main()

