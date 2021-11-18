global.GliticUtil = {
	str_split : function(str, del){
		var ret, part, ind;
		ret = [];
		part = ""; 
		ind = 0;
		for(var i = 0; i < string_length(str); i++){
			var c = string_char_at(str,i + 1);
			if(c == del){
				ret[ind++] = part;
				part = "";
			} else{
				part += c;
			}
		}
		ret[ind] = part;
		return ret;
	},
	
	
	NETWORK_OBJECT : function(){		
		if(!instance_exists(o_glitic_network_manager)){
			instance_create_depth(0,0,0,o_glitic_network_manager)
		}
		return o_glitic_network_manager;
	},
	
	HTTP_ASYNC_RESPONSE : function(async_load){
		var req = undefined;
		try{
			req = ds_map_find_value(global.GliticRequestMap, async_load[? "id"])
			req.status = async_load[?"http_status"];
			req.result = async_load[? "result"];
			var manager = req.owner;
			if(is_undefined(req)){
				exit;
			} else{
				ds_map_delete(global.GliticRequestMap, async_load[?"id"])
			}

			if(async_load[?"http_status"] >= 200 && async_load[?"http_status"] < 300){
				var type = req.req_type;
				switch(type){
					case GliticRequestType.connect : {
						var data = global.GliticUtil.HTTP_ON_CONNECT(req, async_load);
						if(variable_struct_exists(req.conf,"success")){
							req.conf.success(data);
						}
						break;
					}
					case GliticRequestType.disconnect : {
						manager.connected = false;
						manager.game = undefined;
						manager.cToken = undefined;
						manager.sToken = undefined;
						if(variable_struct_exists(req.conf,"success")){
							req.conf.success();
						}
						break;
					}
				}
			} else{
				if(variable_struct_exists(req.conf,"fail")){
					req.conf.fail(async_load[? "result"]);
				}
			}
		} catch(e){				
			if(!is_undefined(req) && variable_struct_exists(req.conf,"caught")){
				req.conf.caught(e);
			}
		}
	},
	
	HTTP_ON_CONNECT : function(req, async_load){
		var manager = req.owner;
		var data = {};
		try{
			data = json_parse(async_load[? "result"]);
			manager.game = data.game;
			manager.sToken = data.token;
			manager.connected = true;
			return data.game;
			
		}
		return data;
	},
	
	GENSTRING : function(n){	
		var alph = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-_";
		var token = "";
		for(var i = 0; i < n; i++){
			token += string_char_at(alph, irandom(string_length(alph) - 1));
		}
		return token;
	}
}