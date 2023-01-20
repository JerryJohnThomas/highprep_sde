# v1 plan


rupesh dummy user creation
with thismuch username, password, type , age , bike details, phone number, user_id


log in

f : user puts in username and password, type of user 
f: sends across like that (post)
b: will check if username exists if so send token
	* database of active tokens -> user_id
f: if you get back token you are logged in, else -1 or something not logged in

******
after this each time just send the token



warehouse guy
* login
* initally a batch of points are ready to be processed at the start of the day
* how to get that points
	* given an excel sheet, you find geo coordinates, distance and time matrix.
	* algo_api : list of rider -> ordered set of places : 
		* you need to know which all riders are available (need an api)
* frontend page : see all rider routes
	* with directions : backend 
* riders : for now assume all riders are available
* api_call : m riders avaiable and rest not avaialble 
* super_token

rider 
* login
* map with directions to go
* see his bag
	* database for bag

customer 
* login
* dummy page / just have a map view (Depending on time)

