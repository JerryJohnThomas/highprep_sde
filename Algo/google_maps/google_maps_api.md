# findings regarding google maps api

* places to gps : geocoding 
    * we only need this for the dataset
    * https://developers.google.com/maps/documentation/javascript/geocoding
* routes api : between 2 points i think




documentation: 
* https://developers.google.com/maps/documentation/routes/compute_route_matrix
* https://developers.google.com/maps/documentation/routes/compute_route_matrix




Request limits: The Compute Route Matrix methods enforce the following request limits:
* If you specify TRAFFIC_AWARE_OPTIMAL, then the number of elements cannot exceed 100. For more on TRAFFIC_AWARE_OPTIMAL, see Configure quality vs latency.
* The number of elements (number of origins × number of destinations) cannot exceed 625.




||a|b|c| d| 
|-|--|--|--|-|
|a|0 | | |
|b| |0 | |
|c| | | |
|d| | | |



250*250/