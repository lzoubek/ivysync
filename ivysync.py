# simple script for syncing ivysilani.cz archives, requires youtube-dl
# set `programmes`

__author__ = 'Libor Zoubek'
__email__  = 'lzoubek@jezzovo.net'
import ivysilani
import subprocess
from subprocess import call
import socket
socket.setdefaulttimeout(60)
import os,sys

# TODO introduce config file
programmes = [{'id':'10818790010','dir':'Chuggington - Vesele Vlacky 3'}, {'id':'10641016902','dir':'Cislovanky'},{'id':'11066801199','dir':'Michalovy Barvy'}]

if __name__ == '__main__':
    # TODO logging
    print('ivysync starting')
    cwd = ''
    # TODO use argparse
    if len(sys.argv) > 1:
      cwd = sys.argv[1]
    devnull = open(os.devnull, 'w')    
    for p in programmes:
        print('Processing %s' % p['dir']) 
	prog = ivysilani.Programme(p['id'])
        prog_dir = os.path.abspath(os.path.join(cwd,p['dir']))
        if not os.path.exists(prog_dir):
            os.mkdir(prog_dir)
        print('Retrieving episodes...')
        episodes = prog.episodes(page_size=9999)
        print('Got %s episodes' % str(len(episodes)))
        for ep in episodes:
            video = os.path.join(prog_dir, ep.title+'-'+ep.ID+'.mp4')
            if os.path.exists(video):
                continue
            try:
                print("Getting video link for %s" % ep.title)
                link = ep.url("web")
                print("Downloading %s to %s" %(link, video))
                call(["youtube-dl", "-o", video, link], stdout=devnull, stderr=subprocess.STDOUT)
            except Exception, e:
                print("Failed to download video: %s " % str(e))
    print('ivysync done')
