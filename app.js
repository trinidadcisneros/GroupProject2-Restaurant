
// Will provide restaurant informaiton in side panel
function buildMetadata(business_id) {
  d3.json(`/restaurant/${business_id}`).then((data) => {
    var panel = d3.select("#sample-metadata");
    panel.html("");
    Object.entries(data).forEach(([key, value]) => {
    panel.append('h6').text(`${key}: ${value}`);
    });
  });

}

function getBusinessId(cuisine_category) {
    // Add the metadata for restaurant at init
    d3.json(`/restaurants/${cuisine_category}`).then(function (data) {
      console.log(data);
      first_restaurant_in_category = data[0]["restaurant_id"];
      console.log(first_restaurant_in_category);
      buildMetadata(first_restaurant_in_category);
    });
}



function buildChart(cuisine_category) {

  d3.json(`/restaurants/${cuisine_category}`).then((data) => {
    var ratings = data.restaurant_rating;
    var ave_cost = data.ave_cost;
    console.log(data);
    console.log(ratings);
    console.log(ave_cost);

    var trace1 = {
      x: ratings,
      y: ave_cost,
      mode: 'markers',
      marker: {
        size: ave_cost,
        color: ratings
      }
    };

    var data1 = [trace1];
    
    Plotly.plot("bubble", data1);
  });
}



function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Add categories to dropdown menu
  d3.json("/cuisine_categories").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      console.log(sample);
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });
  
  const first_category = sampleNames[0];
  var first_restaurant_in_category;

  // Add the metadata for restaurant at init
  d3.json(`/restaurants/${first_category}`).then(function (data) {
    first_restaurant_in_category = data[0]["restaurant_id"];
    console.log(first_restaurant_in_category);
    buildMetadata(first_restaurant_in_category);
  });
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  // Plotly.deleteTraces('bubble', 0);
  console.log(newSample);


  // Plotly.deleteTraces('pie', 0);will have leaflet map
  // div.html("") for leaflet to clear map
  // buildCharts(newSample);
  getBusinessId(newSample);
  buildCharts(newSample);
  // buildMetadata(newSample);

}

// Initialize the dashboard
init();