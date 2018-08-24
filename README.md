# discogs-youtube-dl

The python codes available through this project can be used to collect releases from Discogs. For each release, if there is a video link available, the audio from the video will be downloaded

## Dependancies

* youtube-dl: available at https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
* Numpy

## Requirements
* Discogs Developer API Token: obtain from https://www.discogs.com/developers/
* Google/Youtube Developer API 

## How to Use
#### Collect releases from Discogs using 
1. Open **DownloadDiscogs.py** 

2. Enter your Discogs Authentication Token (Line 20)
```
token = "ENTER TOKEN HERE"
```  
3. Modify your search query for obtaining relavant releases (Lines 27-37)
```
# Create Search Query
path = 'https://api.discogs.com/database/search?'
format_exact = "12\""
year = "1985"
style = "Funk"
genre = "Electronic"
type = "master"
decade = "1980"
sort = "hot"
per_page = 1000
startpage = 1
```
4. Run the code and the metadata for each release will be available as a json file in a folder with the same release ID. 
  
Structure of collected releases: project_root/**year_style_genre**/**ReleaseID**/ReleaseID.json

Example:                         project_root/1985_Funk_Slectronic/158041/158041.json                       
    
#### Download Videos
1. Open **YoutubeDownloader.py**

2. Modify download settings:
```
# Enter youtube API
utubeDataAPI = "Enter Youtube Developer API Here"

# Enter Directory containing discogs releases
SearchDirectory = "1985_Funk_Electronic"

# specify keywords essential for downloading videos
keyWords = None
#keyWords="Instrumental"

# specify Max number releases to download videos for
maxNumberOfReleasesToReview = 1000

# Download most popular video or all videos? (Set False for most popular)
allLinks = True
```
3. Run the code and the audio from the videos will be collected in each of the releaseID folders
