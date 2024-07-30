// Enable pusher logging - don't include this in production
Pusher.logToConsole = true;

var pusher = new Pusher('8a75da5b387b38d2d790', {
  cluster: 'us3'
});

var channel = pusher.subscribe('stock-update-channel');
channel.bind('crossover-event', function(data) {
  alert(JSON.stringify(data));
});

var channel = pusher.subscribe('stock-update-channel');
channel.bind('stock-update', function(data) {
  alert(JSON.stringify(data));
});