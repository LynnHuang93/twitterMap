# twitterMap

##FUNCTION

Twitter Map gives user a Web UI with google map to search for tweets with specific keyword and render search results on the map. The markers are clickable with tweet content in info window.

##CODE

###Web UI:
index.html
This file use google map api to visualize the world map and render the markers. jQuery is used to talk with web server.


###Web Server:
server.js, connection.js

Use Node.js Framework Express to build the simple web server and send elasticsearch query result on search request. Use a seperate file for connection keys.

Node Modules: elasticsearch, express, body-parser, http-aws-es

This part is running on AWS Elastic Beanstalk.


###Data Streaming Server:
poster.py, config.py

Use tweepy to filter the tweets with location info and push them to AWS elasticsearch. Use a seperate file for AWS access keys and twitter api keys.

This part is running on an AWS EC2 instance.