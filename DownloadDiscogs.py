"""

Developed by Behzad Haki (behzadhaki88@gmail.com

This code downloads makes a search query on Discogs database and stores the metadata for each release in an
individual dedicated subfolder

References:
    [1] https://gist.github.com/volpefoxx/1d8a6832e588f3ffa6c9c680f9dada38
    [2] https://www.discogs.com/developers/#page:authentication

"""

import requests
import json
import time
import os

# Enter Discogs Token for Developement (Refer to Discogs/settings/Developer)
token = "sHfxyRqgndyzVnelQINOTerYZKdSrrXTFMKQhkSb"

# AUTHENTICATION HEADER (https://curl.trillworks.com/#) --- Do not Modify
headers = {
    'Authorization': 'Discogs token='+token,
}

# Create Search Entries
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

# --------------------- Downloading Search Results Starts here

# create search URL
for page in range(startpage,1000):
    collection_url = "{path}format_exact={format_exact}&year={year}&style={style}&genre={genre}&" \
                     "type={type}&decade={decade}&per_page={per_page}&page={page}".format(
        path=path,
        format_exact=format_exact,
        year=year,
        style=style,
        genre=genre,
        type=type,
        decade=decade,
        per_page=per_page,
        #sort=sort,
        page=page
    )

    # download search results
    releases = requests.get(collection_url,headers=headers)

    # Create Subfolder to save entries by Discogs' master id example: 1985_House_Electronic
    mainsubfolder = year+"_"+style+"_"+genre
    if not os.path.isdir(mainsubfolder):
        os.mkdir(mainsubfolder)

    # Store the search results in the relative subfolder
    with open("../" + mainsubfolder+"/SearchResult.json", "w") as fp:
        # use this online json viewer to inspect the content: http://jsoneditoronline.org/
        json.dump(releases.json(), fp)

    # Create individual subsubfolders for each master release with an indivual master json metadata file

    data = releases.json()      #Jsonize search results

    for i in range(len(data["results"])):
        # get master metadata
        masterdata = requests.get(data["results"][i]["resource_url"], headers=headers).json()
        # get id of master release
        masterID = masterdata["id"]
        print ("masterID: ",masterID)

        masterStyles = masterdata["styles"]
        masterGenres = masterdata["genres"]

        print ("Page #", page, "Master Release #", i, masterStyles, masterGenres)

        if len(masterStyles)==1 and len(masterGenres)==1:
            if masterStyles[0]==style and masterGenres[0]==genre:
                # create individual folder for master release
                if not os.path.isdir("../"+mainsubfolder+"/"+str(masterID)):
                    os.mkdir("../"+mainsubfolder+"/"+str(masterID))

                # Save master metadata json
                with open("../"+mainsubfolder+"/"+str(masterID)+"/"+str(masterID)+".json", "w") as fp:
                    json.dump(masterdata, fp)

                print("Metadata for Master Release ID# "+str(masterID)+" Successfully created")

        time.sleep(.5)   # max allowed communication with server is 60 requests/min for authorized transactions
