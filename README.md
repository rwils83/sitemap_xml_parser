# Sitemap xml parser

## What is it?
Basic parser because I was tired of figuring out the URLs from sitemap.xml files

## How do I use it?
usage: main.py [-h] -u URL [-o [OUTPUT]] [-d] [-f [FILE]] [-dl [DELETE_URL_FILE]] [-v] [-e [EXCLUDE]]

Parse Sitemap.xml files.

optional arguments:  
  -h, --help            show this help message and exit  
  -o [OUTPUT], --output [OUTPUT]
                        Use -o/--output to write all URLs found to a file  
  -d, --delete          Use -d/--delete to delete all locally written xml files  
  -f [FILE], --file [FILE]
                        Future use  
  -dl [DELETE_URL_FILE], --delete_url_file [DELETE_URL_FILE]
                        Use to clean up a url file from previous runs, mostly was used during testing the script.  
  -v, --verbose         Use for debugging  
  -e [EXCLUDE], --exclude [EXCLUDE]
                        Use to exclude urls breaking the script

Required Arguments:
  -u URL, --url URL     Enter the URL that lists sitemap.xml files, ex. https://www.tiktok.com/robots.txt

## Whats to come?
See the TODO.md

## How do I contribute?
See the CONTRIBUTIONS.md