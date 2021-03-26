"""
TODO: script to download the ATP live show
Author: Stephen Kim
Date: Feb 23rd, 2017
"""

from datetime import datetime, timedelta
import os
import subprocess
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
Assumes DIRECTORY variables points to a directory comprising entirely files
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

The downloader is wrapper of a specific curl command with some logic to
determine the output file as well as maintain some persistence in situations
when the curl command fails.

a typical ATP show is around 2 hours, but can sometimes run long by as much as
3 hours so a good buffer of 3.5 hours is in place

TODO: use python built ins to interpret the results of the curl command to more
intelligently determine when to stop curling the stream

In ideal conditions, the persistence logic should not be needed, but in
situations where the stream is congested or it cuts out for some reason, the
script will wait for a short while, then attempt to try to download the stream
again. The output files for each attempt are changed slightly to reflect a new
"portion" of the live stream

TODO:
Something more intelligent than curling the stream as it doesn't make a proper
mp3 file. As it currently stands, the outputted file will not play the audio
nicely if any seeking is done. An easy workaround is to drop the output file
into an audio editor and exporting it to an mp3. If the audio file is listened
continuously from start to end, it should play fine

A tool to stitch the portions of these files together
"""
def download_persist():
    cutoff_time = datetime.now() + timedelta(hours=3) +  timedelta(minutes=30)
    print("script downloading with cutoff time %r"% (str(cutoff_time)))
    current_ep = get_last_ep() + 1
    ep_portion = 0
    dprint(current_ep)
    ep_name = DIRECTORY + "atp" + str(current_ep) + "-" + str(ep_portion) + \
        ".mp3"
    command = ["curl", "-o", ep_name, "https://atp.fm:8443/listen"]
    sleepcmd = ["sleep", "30"];
    #continues to run the download command until it reaches the cutoff time
    while(datetime.now() < cutoff_time):
        print("downloading stream with output file %r" % (ep_name))
        subprocess.run(command)
        ep_portion += 1
        # script ended, sleep for a couple of seconds before trying to
        # download another portion
        subprocess.run(sleepcmd)
        ep_name = DIRECTORY + "atp" + str(current_ep) + "-" + str(ep_portion) + \
        ".mp3"
        command[2] = ep_name # replace output file name in curl command
    print("done")
    #dprint(os.path.getsize(ep_name))

def main():
    dprint("hello world")
    download_persist()

# can be run from command line with first parameter to set DEBUG flag
# e.g. python3 atp_downloader.py t
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'True' or sys.argv[1] == 'T' or sys.argv[1] == 't':
            DEBUG = True;
    main()

