// # ************************************
// # BUILDS LEAFLET MAP from data passed from APP.JS
// # ************************************
function initializeMap(data) {
  console.log(data);
  var myMap = L.map("map", {
    center: [34.0522, -118.2437],
    zoom: 11,
    layers: markersLayer
  });
  
  // Adding tile layer to the map
  
  var street = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox.streets',
      accessToken: API_KEY
    }).addTo(myMap);

    var markers = [];

  //   // Loop through data
    for (var i = 0; i < data.length; i++) {
      console.log(data[i]);
      console.log(data[i].restaurant_lat);
      // Add a new marker and provides a pop-up
      markers.push(L.marker([data[i].restaurant_lat, data[i].restaurant_lng])
      .bindPopup("<h1>" + data[i].restaurant_name + "</h1> <hr> <h3> price range" + data[i].price_range + "</h3>" + "</h1> <hr> <h3>rating " + data[i].restaurant_rating + "</h3>")
        );
  }
    console.log(markers);
    var markersLayer = L.layerGroup(markers);

    // L.control.layers(overlayMaps, {collapsed: false}).addTo(myMap);
}


// # ************************************
// # REBUILD LEAFLET MAP
// # ************************************
// function buildMap(data) {
//   console.log(data);

//   var myMap = L.map("map", {
//       center: [34.0522, -118.2437],
//       zoom: 11
//     });
  
  
//   // Adding tile layer to the map
  
//   var street = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
//       attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
//       maxZoom: 18,
//       id: 'mapbox.streets',
//       accessToken: API_KEY
//     }).addTo(myMap);
  
//     var dark = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
//       attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
//       maxZoom: 18,
//       id: "mapbox.dark",
//       accessToken: API_KEY
//     });
  
//     var baseMaps = {
//       Street: street,
//       Dark: dark
//       };

  
//   //   // Create a new marker cluster group
//     var markers = L.markerClusterGroup();
//     var heatArray = [];

  
//   //   // Loop through data
//     for (var i = 0; i < data.length; i++) {

//       console.log(data[i]);

//         // Add a new marker to the cluster group and bind a pop-up
//       markers.addLayer(L.marker([data[i].restaurant_lat, data[i].restaurant_lng])
//       .bindPopup("<h1>" + data[i].restaurant_name + "</h1> <hr> <h3> price range" + data[i].price_range + "</h3>" + "</h1> <hr> <h3>rating " + data[i].restaurant_rating + "</h3>")
//         );
      
//       heatArray.push([data[i].restaurant_lat, data[i].restaurant_lng]
//         );
//   }
//   console.log(heatArray)
//     L.control.layers(baseMaps).addTo(myMap);
// }
