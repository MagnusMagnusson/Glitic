enum GliticRequestType{
	connect,
	disconnect,
	
}

#macro GliticIsProd false
#macro GliticURL (GliticIsProd ? "https://glitic.net/api" : "http://127.0.0.1:8080/api")