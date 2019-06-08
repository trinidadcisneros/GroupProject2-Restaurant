// # ************************************
// # BUILDS LEAFLET MAP from data passed from APP.JS
// # ************************************
function buildMaps(data) {
  console.log(data);
  
  var myMap = L.map("map", {
      center: [34.0522, -118.2437],
      zoom: 11
    });
  
  // Adding tile layer to the map
  
  var street = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox.streets',
      accessToken: API_KEY
    }).addTo(myMap);
  
    var dark = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.dark",
      accessToken: API_KEY
    });
  
    var baseMaps = {
      Street: street,
      Dark: dark
      };

  
  //   // Create a new marker cluster group
    var markers = L.markerClusterGroup();
    var heatArray = [];

  
  //   // Loop through data
    for (var i = 0; i < data.length; i++) {

      console.log(data[i]);

        // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([data[i].restaurant_lat, data[i].restaurant_lng])
      .bindPopup("<h1>" + data[i].restaurant_name + "</h1> <hr> <h3> price range" + data[i].price_range + "</h3>" + "</h1> <hr> <h3>rating " + data[i].restaurant_rating + "</h3>")
        );
      
      heatArray.push([data[i].restaurant_lat, data[i].restaurant_lng]
        );
  }
  console.log(heatArray)
  
  //  var heat = L.heatLayer(heatArray, {
  //    radius: 20,
  //    blur: 35
  //  }).addTo(myMap);
  
  // myMap.addLayer(markers);
  
  // var overlayMaps = {
  //   Restaurants: markers,
  //   Density: heat
  // };
  
  
  // //Overlays that may be toggled on or off
    
  
    // Add our marker cluster layer to the map
    // L.control.layers(baseMaps, overlayMaps).addTo(myMap);
    L.control.layers(baseMaps).addTo(myMap);
}
  
  //heatmap
  // d3.json(local).then(function(data) {
  
  //   //console.log(data.restaurants[0].restaurant.location.longitude);
  
  //  var heatArray = [];
  
  //  for (var i = 0; i < data.restaurants.length; i++) {
  //  //   //var location = data.restaurants[i].restaurant.location;
  //  //   console.log(data.restaurants[i].restaurant.location.longitude);
     
  //    if (location) {
  //      heatArray.push([data.restaurants[i].restaurant.location.latitude, data.restaurants[i].restaurant.location.longitude]);
  //     }
  //   };
   
  //  console.log(heatArray)
  
  //  var heat = L.heatLayer(heatArray, {
  //    radius: 20,
  //    blur: 35
  //  }).addTo(myMap);
  
  // });
  