'''
Reference https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl

Note: All codes here are obtained from the above reference
'''

from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'outtmpl': '../'
    }


def downloadFromVideosLinks (id, dl_location, url_list,printOn=False,ydl_opts=ydl_opts):

    ydl_opts["outtmpl"]=dl_location+"%(title)s.%(ext)s"

    downloadComplete = -1

    for i in range(len(url_list)):
        if printOn:
            print ("Started Downloading Master Release ", id, url_list[i])
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url_list[i]])
                downloadComplete = 1
            except:
                print ("video has been removed")

    return downloadComplete
