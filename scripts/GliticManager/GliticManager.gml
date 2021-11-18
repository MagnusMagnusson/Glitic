function GliticManager() constructor{
	game = {
		id : undefined,
		name : undefined,
		tables : [],
	};
	sToken = undefined;
	cToken = undefined;
	connected = false;
	tableObjects = {};
	
	static connect = function(gameId, key){
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
		var _url = GliticURL;
		var token = global.GliticUtil.GENSTRING(8);
		self.cToken = token;
	
		var req = new GliticRequest(self, _url + "/game/"+gameId+"/connect/",{
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

	static disconnect = function(){
		if(!self.is_connected()){
			return;
		}
		var req, game, _url;
		game = self.game.id;
		_url = GliticURL;
		_url += "/game/"+game+"/disconnect/";
		req = new GliticRequest(self,_url, {
			method: "POST",
			body : {
				token : self.sToken
			}
		});
		req.req_type = GliticRequestType.disconnect;
		req._send();	
	}

	static is_connected = function(){
		return self.connected;
	}
	
	static table = function(table_name_or_id){
		if( !self.is_connected()){
			throw "GliticManager.Table(): Trying to access tables while not connected";
		}
		var tables = self.game.tables;
		for(var i = 0; i < array_length(tables); i++){
			var t = tables[i];
			if(t.id == table_name_or_id || t.name == table_name_or_id){
				if(variable_struct_exists(self.tableObjects,t.id)){
					return self.tableObjects[$ t.id];
				} else{
					var tob = new GliticTable(t.id, t.name);
					return tob;
				}
			}
		}
		throw "GliticManager.Table(): No table with name or id " + string(table_name_or_id);
	}

}