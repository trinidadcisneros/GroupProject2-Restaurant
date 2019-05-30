function createDropDown() {
    var selector = d3.select("#selDataset");
    d3.json("/cuisine_categories").then((sampleNames) => {
        sampleNames.forEach((sample) => {
          console.log(sample);
          selector
            .append("option")
            .text(sample)
            .property("value", sample);
        });
    });
}

function constructMetaData() {
    d3.json("/cuisine_categories").then(function(data) {
        var first_cuisine_selection;
        first_cuisine_selection = data[0];
        console.log(first_cuisine_selection);
        initializeMetaData(first_cuisine_selection);
    });
}

function initializeMetaData(cuisine_category) {
    d3.json(`/restaurants/${cuisine_category}`).then(function (data) {
      first_restaurant_in_category = data[0]["restaurant_id"];
      console.log(first_restaurant_in_category);
      buildMetadata(first_restaurant_in_category);
    });
}

function buildMetadata(business_id) {
    d3.json(`/restaurant/${business_id}`).then((data) => {
      var panel = d3.select("#sample-metadata");
      panel.html("");
      Object.entries(data).forEach(([key, value]) => {
      panel.append('h6').text(`${key}: ${value}`);
      });
    });
  
}

function constructChart() {
  d3.json("/cuisine_categories").then(function(data) {
      var cuisine_category;
      cuisine_category = data[0];
      console.log(cuisine_category);
      buildChart(cuisine_category);
  });
}

function buildChart(cuisine_category) {

    d3.json(`/restaurants/${cuisine_category}`).then(function (data) {
      var ratings = [];
      var ave_cost = [];
      data.forEach((d) => { 
        Object.entries(d).forEach(([key, value]) => {
          if (key === "restaurant_rating") {
            ratings.push(value);
          } if (key === "ave_cost") {
            ave_cost.push(value);
          } else {
          }
        });
      });
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
      
      var layout = {
        title: "Average Cost (for two) versus Rating",
        xaxis: { title : "Restaurant Rating (1-5)"},
        yaxis: { title : "Average cost for two ($)"}
      };
      
      Plotly.plot("bubble", data1, layout);
    });
}

function updateBubblePlot(cuisine_category) {

  d3.json(`/restaurants/${cuisine_category}`).then(function (data) {
    var x_ratings = [];
    var y_ave_cost = [];
    data.forEach((d) => { 
      Object.entries(d).forEach(([key, value]) => {
        if (key === "restaurant_rating") {
          x_ratings.push(value);
        } if (key === "ave_cost") {
          y_ave_cost.push(value);
        } else {
        }
      });
    });
    console.log(ratings);
    console.log(ave_cost);

    var trace2 = {
      x: x_ratings,
      y: y_ave_cost,
      mode: 'markers',
      marker: {
        size: y_ave_cost,
        color: x_ratings
      }
    };

    var data2 = [trace2];
    
    var layout = {
      title: "Average Cost (for two) versus Rating",
      xaxis: { title : "Restaurant Rating (1-5)"},
      yaxis: { title : "Average cost for two ($)"}
    };
    
    Plotly.plot("bubble", data2, layout);
  });
}


function init() {
    createDropDown();
    constructMetaData();
    constructChart();
}

  // Fetch new data each time a new sample is selected
function optionChanged(newSelection) {
    Plotly.deleteTraces("bubble", 0);
    console.log(newSelection);
    initializeMetaData(newSelection);
    updateBubblePlot(newSelection);
}


init();