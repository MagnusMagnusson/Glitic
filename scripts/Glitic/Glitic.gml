global.GliticSingleton = undefined;

function Glitic(){
	if(is_undefined(global.GliticSingleton)){
		global.GliticSingleton = new GliticManager();
	}
	return global.GliticSingleton
}