global.Glitic_manager_struct = {
	game : undefined,
	sk : undefined,
	connected : false,
}

function glitic_connect(gameId, key){
	if(!instance_exists(o_glitic_network_manager)){
		instance_create_depth(0,0,0,o_glitic_network_manager);
	}
}