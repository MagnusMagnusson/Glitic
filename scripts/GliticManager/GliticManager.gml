function GliticManager() constructor{
	game = global.GliticUtil.EMPTY_GAME();
	sToken = undefined;
	cToken = undefined;
	connected = false;
	clid = undefined;
	tableObjects = {};
	
	connect = function(gameId, key){
		if(self.is_connected()){
			exit;
		}
		
		var sk, pre, post;
		sk = global.GliticUtil.str_split(key, "-");
		if(array_length(sk) != 2 || string_length(sk[0]) != 4 || string_length(sk[1]) != 8){
			throw "Glitic: Key in incorrect format. Key should be of format XXXX-XXXXXXXX";
		}
		pre = sk[0];
		post = sk[1];
		var token = global.GliticUtil.GENSTRING(8);
		self.cToken = token;
	
		var req = new GliticRequest(self, "/game/"+gameId+"/connect/",{
			method : "POST",
			body : {
				key : pre,
				token : token,
				hash : sha1_string_utf8(token + post),
				encoding : "sha1"
			}
		});
	
		req.req_type = GliticRequestType.connect;
		req._send();
		return req;
	}

	disconnect = function(){
		if(!self.is_connected()){
			return;
		}
		var req, game, _url;
		game = self.game.id;
		_url = "/game/"+game+"/disconnect/";
		req = new GliticRequest(self,_url, {
			method: "POST",
			body : {
				token : self.sToken
			}
		});
		req.req_type = GliticRequestType.disconnect;
		req._send();
		return req;
	}

	is_connected = function(){
		return self.connected;
	}
	
	table_list = function(){
		if(!self.is_connected()){
			return [];
		} else{
			return game.tables;
		}
	}
	
	table = function(table_name_or_id){
		var tables = self.game.tables;
		for(var i = 0; i < array_length(tables); i++){
			var t = tables[i];
			if(t.id == table_name_or_id || t.name == table_name_or_id){
				if(variable_struct_exists(self.tableObjects,t.id)){
					show_debug_message(table_name_or_id + " has been found at id " + string(t.id))
					return self.tableObjects[$ t.id];
				} else{
					show_debug_message(table_name_or_id + " got created at " + string(t.id))
					var tob = new GliticTable(self, t.id, t.name);
					self.tableObjects[$ t.id] = tob;
					return tob;
				}
			}
		}
		throw "GliticManager.Table(): No table with name or id " + string(table_name_or_id);
	}

}