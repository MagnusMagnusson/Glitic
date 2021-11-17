function glitic_connect(gameId, key){
	if(glitic_is_connected()){
		exit;
	}
	var networker = global.GliticUtil.NETWORK_OBJECT();
	
	var sk, pre, post;
	sk = global.GliticUtil.str_split(key, "-");
	if(array_length(sk) != 2 || string_length(sk[0]) != 4 || string_length(sk[1]) != 8){
		throw "Glitic: Key in incorrect format. Key should be of format XXXX-XXXXXXXX";
	}
	pre = sk[0];
	post = sk[1];
	var _url = GliticURL;
	var token = global.GliticUtil.GENSTRING(8);
	global.GliticData.cToken = token;
	
	var req = new GliticRequest(_url + "/game/"+gameId+"/connect/",{
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

function glitic_disconnect(){
	if(!glitic_is_connected()){
		return;
	}
	var req, game, _url;
	game = global.GliticData.game.id;
	_url = GliticURL;
	_url += "/game/"+game+"/disconnect/";
	req = new GliticRequest(_url, {
		method: "POST",
		body : {
			token : global.GliticData.sToken
		}
	});
	req.req_type = GliticRequestType.disconnect;
	req._send();	
}

function glitic_is_connected(){
	return global.GliticData.connected;
}