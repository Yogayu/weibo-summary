var twitter = require('ntwitter');
var fs = require('fs');

var twit = new twitter({
  consumer_key: '0A6TqJSaqcUV3G3Soj5YML95v',
  consumer_secret: 'vlsdh1SEvB8PD5RRyMI113GeZeHIJvZV3D5SxG5qm08UTIz7fQ',
  access_token_key: '2923130468-fJ4s4XSfzDZQSXGzRmOlRikonYxEYRPzpSWvhgw',
  access_token_secret: 'z5ggQB54hoXpIa8N4K1mZsnsN4v2of6cZVYbjQkwm9EIV'
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

