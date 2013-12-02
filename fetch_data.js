var twitter = require('ntwitter');
var fs = require('fs');

var twit = new twitter({
  consumer_key: '7OHEVs11pynr9S1zabh9A',
  consumer_secret: '1dlyFmH2sMBqVEdyJISdiUX5YTPG7FCMzrO7ogCFg',
  access_token_key: '1428655608-H6NphXvpQjyWaoCKysTrUsmqFZotGNa0BlOuiNR',
  access_token_secret: '3fFdnUFW9ZLF1BLgl4Q6q75JH4ORwhRFiJyycu2gf6Xkn'
});

function search(topic, maxid, count) {
      twit.search(topic, {count:100, lang:"en", max_id:maxid}, function(err, data) {
        if(err) {
         console.log(err);
         return;
        } 
        var stream = fs.createWriteStream("./data/"+topic+".txt", { 'flags': 'a' } );
        stream.once('open', function(fd) {
          data.statuses.forEach( function(tweet) {
            //console.log("writing tweet "+tweet.text);
            parsed = tweet.text;
            parsed = parsed.replace(/\r?\n|\r/g,'');
            parsed = parsed.toLowerCase();
            if(parsed) {
              stream.write(parsed+"\n");
            }
          });
          stream.end();
          if(count > 0) {
            if(data.statuses[data.statuses.length-1]) {
              search(topic, data.statuses[data.statuses.length-1].id, count-1);
            } else {
              console.log("exited topic " + topic + " with count " + count);
            }
          }
       });
      });
}

///*
//fetch tweets of topics from file
fs.readFile('./topic_list-11-21.txt', 'utf8', function(err, data) {
  topics = data.split('\n');
  topics.forEach( function(topic) {
    //console.log("looking at topic "+topic);
    search(topic, -1, 5);
  });
});
//*/

