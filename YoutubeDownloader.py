import json

import shutil, os

from glob import glob

from youtube_dl_downloader import downloadFromVideosLinks

import re

import requests


from datetime import date

import numpy as np

def getURLs (ReleaseDirectory, keyWords=None,allLinks = False):
    #if allLinks == False, returns the best link as defined below
    #returns the best YouTube URL representing a release
    #best representation:
    #                 1. No remix or rework or alternative version
    #                 2. Most popular release on youtube ranked based on Total YT view * likes/(likes+dislikes)
    #                 3.
    if allLinks:
        url_list = []
        title_list = []
        id = ReleaseDirectory.split("/")[-2]
        with open(ReleaseDirectory + id + ".json", "rb") as fp:  # read master metadata json
            ReleaseMetaData = json.load(fp)

        try:
            youtubeVideosMetadata = ReleaseMetaData["videos"]
            videoCount = len(youtubeVideosMetadata)
            linksExist = True
        except:
            print ("no video for ", id)
            linksExist = False


        if linksExist:
            url_list = []
            for i in range(videoCount):
                url = ReleaseMetaData["videos"][i]["uri"]
                title = ReleaseMetaData["videos"][i]["title"]

                if keyWords!=None:
                    tempTitle = re.sub('[^A-Za-z0-9]+', ' ', title).lower()
                    tempTitle = tempTitle.split(" ")
                    #print tempTitle

                    for keyWord in keyWords.lower().split(" "):
                        #print keyWord
                        if keyWord in tempTitle:
                            print (title)
                            url_list.append(url)
                            title_list.append(title)
                            break
                else:
                    url_list.append(url)
                    title_list.append(title)

            if url_list == []:
                linksExist = False

        return id, url_list, title_list,linksExist



def getMostPopularVideos ( url_list, youtubeAPIKey = "AIzaSyAZ_O1GtX3AWPLM4Y6hPA-HrQJC5uf3a5Q", PopularityLimit = 1000):
    #Popularity =  viewes/(years since uploaded)*likes/(likes+dislikes)
    #reference: https://www.quora.com/How-can-I-get-the-count-of-likes-and-dislikes-of-each-and-every-video-on-YouTube-Does-YouTube-Data-API-support-that
    #https://developers.google.com/youtube/v3/getting-started#part
    # returns MostPopularCnt number of links in descending popularity rate

    #https: // www.googleapis.com / youtube / v3 / videos?id = C0DPdy98e4c & key = YOUR_API_KEY & part = statistics

    viewcounts = []
    likecounts = []
    dislikecounts = []
    yearsSincePublisheds = []

    popularityList = []
    urlSuccessful = []  #urls for which data was successfully obtained
    for utubeLink in url_list:
        videoid = utubeLink.split("v=")[-1]
        stat_collection_url = "https://www.googleapis.com/youtube/v3/videos?id={videoid}&key={API_KEY}&part=snippet,statistics".format(
            videoid=videoid,
            API_KEY=youtubeAPIKey
        )

        try:
            vidstats = requests.get(stat_collection_url)
            vidstats = json.loads(vidstats.text)

            viewcount= float(vidstats["items"][0]["statistics"]["viewCount"])
            viewcounts.append(viewcount)
            likecount = float(vidstats["items"][0]["statistics"]["likeCount"])
            likecounts.append(likecount)
            dislikecount = float(vidstats["items"][0]["statistics"]["dislikeCount"])
            dislikecounts.append(dislikecount)
            datePublished = vidstats["items"][0]["snippet"]["publishedAt"][:10].split("-")

            date_published = date(int(datePublished[0]),int(datePublished[1]),int(datePublished[2]))
            now = date.today()
            yearsSincePublished = (now-date_published).days/365.0
            yearsSincePublisheds.append(yearsSincePublished)

            popularity = viewcount/yearsSincePublished*(likecount/(likecount+dislikecount))
            popularityList.append(popularity)
            urlSuccessful.append([utubeLink])
        except:
            print("")

    if (popularityList!=[]):
        print ("popularityList ", popularityList)
        print ("urlSuccessful", urlSuccessful)
        MostPopularIndex = np.argmax(popularityList)
        print (MostPopularIndex)
        print (urlSuccessful[MostPopularIndex])
        popularity_rating = popularityList[MostPopularIndex]
        views = viewcounts[MostPopularIndex]
        likes = likecounts[MostPopularIndex]
        dislikes = dislikecounts[MostPopularIndex]
        yearsSinceUpload = yearsSincePublisheds[MostPopularIndex]
        return urlSuccessful[MostPopularIndex], popularity_rating, views, likes, dislikes, yearsSinceUpload
    else:
        print ("empty")
        return [], [], [], [], [], []








def downloadYoutubeFromDiscogsMeta(SearchDirectory, utubeDataAPI, maxNumberOfReleasesToReview=10,keyWords=None , allLinks = False):

    MasterReleaseSubdirectories = glob(SearchDirectory + "/*/")

    print (len(MasterReleaseSubdirectories))

    if not keyWords==None:
        withoutAudioDirectory= SearchDirectory + "/"+ "without_audio"
        withAudioDirectory= SearchDirectory + "/"+ "with_audio (Title Filters -> "+keyWords+")"
    else:
        withoutAudioDirectory = SearchDirectory + "/" + "without_audio"
        withAudioDirectory = SearchDirectory + "/" + "with_audio (No Title Filter)"

    if not os.path.isdir(withoutAudioDirectory):
        os.mkdir(withoutAudioDirectory)
    if not os.path.isdir(withAudioDirectory):
        os.mkdir(withAudioDirectory)
    for ReleaseDirectory in MasterReleaseSubdirectories[:maxNumberOfReleasesToReview]:
        print ("\n\n")
        print (ReleaseDirectory)
        id, url_list, title_list,linksExist = getURLs(ReleaseDirectory, keyWords=keyWords,allLinks=allLinks)
        MostPopularVideoUrl = []
        if linksExist:
            MostPopularVideoUrl, popularity_rating, views, likes, dislikes, yearsSinceUpload = getMostPopularVideos(url_list,
                                                                                                                    youtubeAPIKey=utubeDataAPI,
                                                                                                                    PopularityLimit=1000)

            if MostPopularVideoUrl!=[]:
                downloadComplete = downloadFromVideosLinks(id, ReleaseDirectory, MostPopularVideoUrl,printOn=True)

            else:
                downloadComplete = -1

            if downloadComplete>-1:
                shutil.move(ReleaseDirectory, withAudioDirectory)
                youtube_data_json = {
                    "URL":MostPopularVideoUrl,
                    "Popularity Rating":popularity_rating,
                    "views":views,
                    "likes":likes,
                    "dislikes":dislikes,
                    "yearsSinceUpload":yearsSinceUpload
                }
                with open(os.path.join(withAudioDirectory, str(id))+"/videoLinkAndRating.json", "w") as fp:
                    json.dump(youtube_data_json, fp)
            else:
                shutil.move(ReleaseDirectory, withoutAudioDirectory)

        else:
            shutil.move(ReleaseDirectory, withoutAudioDirectory)


year = ""
#style = "House"
#genre = "Electronic"

style = "Soca"
genre = "Reggae"

utubeDataAPI = "AIzaSyAZ_O1GtX3AWPLM4Y6hPA-HrQJC5uf3a5Q"



SearchDirectory = "../"+year+"_"+style+"_"+genre


#downloadYoutubeFromDiscogsMeta(SearchDirectory, utubeDataAPI, maxNumberOfReleasesToReview=1000,keyWords="Instrumental",allLinks=True)
downloadYoutubeFromDiscogsMeta(SearchDirectory, utubeDataAPI, maxNumberOfReleasesToReview=1000,keyWords=None,allLinks=True)