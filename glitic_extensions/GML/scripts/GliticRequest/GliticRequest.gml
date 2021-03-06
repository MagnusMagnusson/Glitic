function GliticRequest(manager, _url, config) constructor{
	url = _url;
	conf = config;
	owner = manager;
	
	req_id = undefined;
	req_type = undefined;
	status = -1;
	result = "";
	imp = global.GliticUtil.GENSTRING(8);
	
	method_safe = function(meth){
		return meth == "GET" || meth == "OPTIONS" || meth == "HEAD";
	}
	
	_send = function(){
		global.GliticUtil.NETWORK_OBJECT();
		var headers = ds_map_create();
		headers[? "Accept"] = "application/json";
		headers[? "Content-Type"] = "application/json";	
		headers[? "Connection"] = "close";	
				
		var meth, bod;
		
		if(variable_struct_exists(conf, "method")){
			meth = conf.method
		} else{
			meth = "GET";
		}
	
		if(variable_struct_exists(conf, "body")){
			bod = json_stringify(conf.body);
		} else{
			bod = "";
		}
		
		if(self.owner.is_connected()){
			headers[? "X-token"] =self.owner.sToken;
			headers[? "X-imp"] = imp;
					
			if(self.method_safe(meth)){
				show_debug_message("/api"+self.url)
				headers[? "X-checksum"] = sha1_string_utf8("/api"+self.url + imp + self.owner.cToken);	
			} else{
				headers[? "X-checksum"] = sha1_string_utf8(bod + imp + self.owner.cToken);	
			}
		}

		req_id = http_request(GliticURL+ self.url, meth, headers, bod);
		global.GliticRequestMap[? req_id] = self;
		ds_map_destroy(headers);
	}
	
	onSuccess = function(func){
		conf.success = func;
		return self;
	}
	
	onFail = function(func){
		conf.fail = func;
		return self;
	}
	
	onException = function(func){
		conf.caught = func;
		return self;
	}
	
	onResponse = function(func){
		conf.response = func;
	}
}