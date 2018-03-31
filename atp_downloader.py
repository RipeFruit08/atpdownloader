import datetime
import os
import sys

def get_last_ep():
    prefix = "atp"
    suffix = ".mp3"
    filenames = os.listdir('.')
    filenames.remove(sys.argv[0])
    filenames = list(s[len(prefix):] for s in filenames)
    print(filenames)
    filenames = list(s[:-len(suffix)] for s in filenames)
    print(filenames)
    filenames.remove("_S")
    filenames = list(int(s) for s in filenames)
    last_ep = max(filenames)
    return last_ep

def download_persist():
    cutoff_time = datetime.datetime.now().replace(hour=0, minute=30,
        second=0, microsecond=0)
    current_ep = get_last_ep() + 1
    ep_portion = 0
    print(current_ep)
    ep_name = "atp" + str(current_ep) + "-" + str(ep_portion) + ".mp3"
    command = "curl -o " + ep_name + " marco.org:8001/listen"
    #while(datetime.datetime.now() < cutoff_time):
    os.system(command)
    print(os.path.getsize(ep_name))

def main():
    print("hello world")
    download_persist()

if __name__ == "__main__":
    main()

