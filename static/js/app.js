// Will provide restaurant informaiton in side panel
function buildMetadata(business_id) {
  d3.json(`/metadata/${business_id}`).then((data) => {
    var panel = d3.select("#sample-metadata");
    panel.html("");
    Object.entries(data).forEach(([key, value]) => {
    panel.append('h6').text(`${key}: ${value}`);
    });
  });

}


function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");
  var panel = d3.select("#sample-metadata");

  // Use the list of sample names to populate the select options
  d3.json("/cuisine_categories").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

  // will get the information from the filtered restaurants by category
  // will then get the first value
  d3.json("/cuisines/<cuisine_categories>").then((cuisineCategory) => {
    cuisineCategory.forEach((sample) => {
      panel
    .append("option")
    .text(sample)
    .property("value", sample);
  });
    // Use the first sample from the list to build the initial plots
    const firstSample = cuisineCategory[0];
    // buildCharts(firstSample); <- will be the cuisine vs ratings plot
    buildMetadata(firstSample);
  });
}
// To use once we have everything wired up to set up initial displays
// function optionChanged(newSample) {
//   // Fetch new data each time a new sample is selected
//   Plotly.deleteTraces('bubble', 0);
//   Plotly.deleteTraces('pie', 0);
//   buildCharts(newSample);
//   buildMetadata(newSample);
// }

// Initialize the dashboard
init();
