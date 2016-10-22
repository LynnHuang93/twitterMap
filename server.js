//Setup web server and socket
var express = require('express'),
    app = express(),
    http = require('http'),
    bodyParser = require('body-parser'),
    server = http.createServer(app),
    client = require('./connection.js');

server.listen(process.env.PORT || 8081);
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());

app.get('/search', function(req, res) {
    var key = req._parsedOriginalUrl.query;
    client.search({
                    index: 'tweet',
                    type: 'tweet',
                    body: {
                        "query":{
                            "bool":{
                                must: {
                                    term : { "text" : key }
                                  }
                            }
                        }
                    }
                }, function (error, response, status) {
                    if (error) {
                        res.send("search error: " + error);
                    }
                    else {
                        res.send(response);
                    }
                });
});