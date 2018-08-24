# discogs-youtube-dl

The python codes available through this project can be used to collect releases from Discogs. For each release, if there is a video link available, the most popular video will be downloaded

## Dependancies

* youtube-dl: available at https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
* Discogs Developer API Token: obtain from https://www.discogs.com/developers/

## How to Use
1. Collect releases from Discogs using 
  - Open **DownloadDiscogs.py** 
  
  - Enter your Discogs Authentication Token (Line 20)
  ```
  token = "ENTER TOKEN HERE"
  ```
  
  - Modify your search query for obtaining relavant releases (Lines 27-37)
  ```
  # Create Search Query
path = 'https://api.discogs.com/database/search?'
format_exact = "12\""
year = ""
style = "Funk"
genre = "Electronic"
type = "master"
decade = "1980"
sort = "hot"
per_page = 1000
startpage = 1
  ```
  
  - Run the code and the releases will be available in a new folder in the root
  
