var twitter = require('ntwitter');
var fs = require('fs');

var twit = new twitter({
  consumer_key: '7OHEVs11pynr9S1zabh9A',
  consumer_secret: '1dlyFmH2sMBqVEdyJISdiUX5YTPG7FCMzrO7ogCFg',
  access_token_key: '1428655608-H6NphXvpQjyWaoCKysTrUsmqFZotGNa0BlOuiNR',
  access_token_secret: '3fFdnUFW9ZLF1BLgl4Q6q75JH4ORwhRFiJyycu2gf6Xkn'
});


// view trends
twit.getTrends(function(err, data) {
  data[0].trends.forEach( function(trend) {
    console.log(trend);
  });
});


