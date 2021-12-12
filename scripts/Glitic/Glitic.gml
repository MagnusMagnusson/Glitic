/*
	Glitic.gml
	
	Thank you for chosing Glitic for your online highscore and analytic needs.
	
	We recommend that you read 
*/

global.GliticSingleton = undefined;

function Glitic(){
	if(is_undefined(global.GliticSingleton)){
		global.GliticSingleton = new GliticManager();
	}
	return global.GliticSingleton
}