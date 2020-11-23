# download-all-360.io-panoramas
download all your 360.io images, because the service is shutting down on 2021-02-09

# usage
* install "requests" via pip3: ```pip3 install requests```
* open the file **rescue360.py** and edit the settings section
* run the script: ```python3 rescue360.py```

# settings
### user_urls
this is a *list* of user urls from 360.io    
**a single entry, example:** ```user_urls = ['http://360.io/user/3ca6-11/vikas-reddy/']```    
**multiple entries, example:** ```user_urls = ['http://360.io/user/3ca6-11/vikas-reddy/','http://360.io/user/4db7-22/example-username/']```    

---

### target_path
* this is your local path where the images will be downloaded to
* leave this empty to download the images to the current script location
* make sure the path/folder exists
* the path must end with a slash (```/```)    
**example:** ```/home/username2000/panos/```    

---

### download_images
this can be set to True or False     
**True:** the script downloads the images     
**False:** the script just displays all the image urls     


