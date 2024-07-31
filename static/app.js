// Enable pusher logging - don't include this in production
Pusher.logToConsole = true;

var pusher = new Pusher('8a75da5b387b38d2d790', {
  cluster: 'us3'
});

var channel = pusher.subscribe('stock-update-channel');
channel.bind('crossover-event', function(data) {
  promp_notification(data)
});


function promp_notification(message) {
  target = $("#notify-pop")
  target.css("bottom","0")
  $("#notify-msg").html(message)
  
  // display nofification for 15 sec
  setTimeout(() => {
    target.css("bottom","-10rem")
  }, 50000);
 
}
