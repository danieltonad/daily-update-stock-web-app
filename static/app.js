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


$("#test").click(()=>{

  alert(100)
  promp_notification("")
})

function promp_notification(message) {
  target = $(".notify-pop")
  target.css("bottom","0")

  setTimeout(() => {
    target.css("bottom","-5rem")
    alert(200)
  }, 10000);

  
}