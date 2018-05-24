# HTP-locust-request-generator

A quick multithreaded python script for crawling a site and generating a locust request file - https://locust.io/

Generally seems to be working though it is clear that some issues with relative URLs needs to be fixed.

Developed and tested with python3 (3.6.2 to be exact)

Requires bs4 and requests

TODO:

* Work on known relative pathing issues
* Test on a larger data set - Not sure of capacity and/or performance limitations of sets which are being used to store all URLS being retrieved - currently tested with 60K unique URLs
* Add some intelligence to weighting (paramter to @task) - perhaps based on number of URL segments (i.e. "/" being 1000, "/subdir/" being 100, "/subdir/subdir/" being 10, and everything else being "1")




Example usage:
docker run -e HOST=http://13.59.15.93 -e CLIENT_THREADS=10 jbgriffin/htp-locust-request-file-generator > requests.txt
