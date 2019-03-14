// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
var map, infoWindow;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 6
  });
  infoWindow = new google.maps.InfoWindow;

  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      // Send user's location into server alert route
      $.get('/locations', pos, (results) => {
        $('#success-location').append(`
                                        <br><br>
                                        <div class="g-container--sm g-padding-y-80--xs g-padding-y-125--xsm">
                                            <div class="g-text-center--xs g-margin-b-60--xs">
                                            <img alt="" src="/static/img/widgets/gmap/cd-icon-location.svg" draggable="false">
                                                <h2 class="g-font-size-32--xs g-font-size-36--md g-color--white">Location Found</h2>
                                                <a href="https://www.google.com/maps/place/${pos.lat},${pos.lng}"><b>Click here to see your current location!</b></a>
                                            </div>
                                        </div>
                                     `
                                     );
      });

      infoWindow.setPosition(pos);
      infoWindow.setContent('Location found.');
      infoWindow.open(map);
      map.setCenter(pos);
    }, function() {
      handleLocationError(true, infoWindow, map.getCenter());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
  }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}
