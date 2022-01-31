/*
	Constants, enums, macros used by the Glitic library
	There is nothing here worth touching without good reason. 
	For actually interesting configurations to mess about with go to Glitic_Configuration.gml
*/

//Request types supported by the library
enum GliticRequestType{
	connect,
	disconnect,
	highscores_fetch,
	highscores_post,
}
// For development reasons. 
// Glitic isn't developed on the production server. Glitic developers much prefer using their own machines for the job. 
#macro GliticIsProd false
#macro GliticURL (GliticIsProd ? "https://glitic.net/api" : "http://127.0.0.1:8080/api")