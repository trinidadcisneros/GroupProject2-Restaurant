// # ************************************
// # CREATE DROPDOWN MENU
// # ************************************
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

// # ************************************
// # CUISINE LIST -> 1 CUISINE -> getRestaurantID
// # ************************************
function constructMetaData() {
    d3.json("/cuisine_categories").then(function(data) {
        var first_cuisine_selection;
        first_cuisine_selection = data[0];
        console.log(first_cuisine_selection);
        getRestaurantID(first_cuisine_selection);
    });
}

// # ************************************
// # CUISINE -> RESTAURANT ID to buildMetaData and Bubble Plot
// # ************************************
function getRestaurantID(cuisine_category) {
    d3.json(`/restaurants/${cuisine_category}`).then(function(data) {
      console.log(data);
      restaurant_id = data[0]["restaurant_id"];
      console.log(restaurant_id);
      buildMetadata(restaurant_id);
      initiatlizeChart(data);
      buildMaps(data); 
    });
}

// # ************************************
// # BUILDS METADATA RESTAURANT INFO HTML
// # ************************************
function buildMetadata(business_id) {
    d3.json(`/restaurant_by_id/${business_id}`).then((data) => {
      console.log(data);
      var panel = d3.select("#sample-metadata");
      panel.html("");
      Object.entries(data).forEach(([key, value]) => {
      panel.append('h6').text(`${key}: ${value}`);
      });
    });
}


// # ************************************
// # BUILDS BUBBLE PLOTS
// # ************************************
function initiatlizeChart(data) {

    console.log(data);
    var ratings = [];
    var ave_cost = [];
    var votes = [];
    var price_range = [];
    data.forEach((d) => { 
      Object.entries(d).forEach(([key, value]) => {
        if (key === "restaurant_rating") {
          ratings.push(value);
        } if (key === "ave_cost") {
          ave_cost.push(value);
        } if (key == "nbr_votes") {
          votes.push(value);
        } if (key == "price_range") {
          price_range.push(value);
        } else {
        }
      });
    });
    console.log(ratings);
    console.log(ave_cost);
    console.log(votes);
    console.log(price_range);

    var trace1 = {
      x: ratings,
      y: ave_cost,
      mode: 'markers',
      marker: {
        size: votes/50,
        color: price_range
      }
    };

    var data1 = [trace1];
    
    var layout = {
      title: "Average Cost (for two) versus Rating",
      xaxis: { title : "Restaurant Rating (1-5)"},
      yaxis: { title : "Average cost for two ($)"}
    };
    
    Plotly.plot("bubble", data1, layout);
    Plotly.plot("boxplot", data1, layout);
}




function init() {
    createDropDown();
    constructMetaData();
}

  // Fetch new data each time a new sample is selected
function optionChanged(newSelection) {
    Plotly.deleteTraces("bubble", 0);
    console.log(newSelection);
    getRestaurantID(newSelection);
}


init();