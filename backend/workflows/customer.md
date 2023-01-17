## customer experience 

* login
* add pickup
* put in package info and location (post)
* admin will do a get request after every x seconds 
* admin will accept or reject (post)
* if accepted will go to algo
* algo will tell which rider 
	* rider needs to be updated
		* new point added 
		* directions updated
		* pop for rider happens (frontend only)
	* customer needs to be notified about accepting
		* pop up
		* ETA or ETD if possible 
* after pick up by rider
	* customer
		* pop up - tnx for riding 
	* rider
		* that point is marked as done
			* in the active list no longer there
			* history list still there 
		* directions are updated
