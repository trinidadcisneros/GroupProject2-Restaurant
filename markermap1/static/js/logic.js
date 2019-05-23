// Creating map object
var myMap = L.map("map", {
  center: [34.0522, -118.2437],
  zoom: 11
});

// Adding tile layer to the map
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);



// Assemble API query URL
var local = "/restaurant.json";


// d3.json(local, function(data) {
//   console.log(data.restaurants[0].restaurant.location.latitude);
// });

// d3.json(local, function(data) {
//   console.log(data.restaurants[0].restaurant.location.longitude);
// });
 
// d3.json(local, function(data) {
//   console.log(data.restaurants);
// });
 

// Grab the data with d3
d3.json(local, function(data) {

  // Create a new marker cluster group
  var markers = L.markerClusterGroup();

  // Loop through data
  for (var i = 0; i < data.restaurants.length; i++) {
    var location = data.restaurants[i].restaurant.location
    // Set the data location property to a variable
    // var location = response.restaurants.restaurant.location;

    //Check for location property
    if (location) {

      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([location.latitude, location.longitude])
        );
    
  }
}

  // Add our marker cluster layer to the map
  myMap.addLayer(markers);

});

