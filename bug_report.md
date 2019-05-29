Bug Issue 1:
bubble plots - when we hit onchange, we expect to see an updated plot but we get 500 internal server error

Bug Issue 2:
When we merge the leaflet mapping with the app.js and index.html, none of the plots render.
we get internal server error isues.

Expected outcome:

We expect that when we select a new dropdown, that the leaflet map would render a new set of markers, and that the bubble plots would update.
We will also add a barplot for the cuisine category with average cost.

Higherchy issues:
-we probably need to start off with the cuisine category dropdown
-This should then be fed into the leaflet maping
-and the bubble plot should then be built simultaneously
