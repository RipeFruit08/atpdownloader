# Author: Stephen Kim
# Date: March 31st, 2021
#
# Script that checks whether @atpfm recently tweeted that they'll be going
# live. If they did, run the downloader script.
#
# TODO: get script running in some instance of a recurring job making sure
# not to re-run this script if it is currently being run as that might cause
# multiple instances of the downloader to run
#

python3 atp_recent_live.py

RESULT=$?
echo $RESULT

# if script exited successfully, run downloader script
if [[ $RESULT == 0 ]]
then
    python3 atp_downloader.py
fi
