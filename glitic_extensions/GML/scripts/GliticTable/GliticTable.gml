function GliticTable(gliticmanager, tid, tname) constructor{
	table_id = tid;
	table_name = tname;
	data = {
		def:[]
	};
	primary_asc = false;
	secondary_asc = false;
	user_unique = false;
	manager = gliticmanager;
	
	fetch = function(filters, subtable_name){
		if(is_undefined(subtable_name)){
			subtable_name = "def";
		}
		var qs = "";
		if (!is_undefined(filters)){
			var keys =  variable_struct_get_names(filters);
			for(var i = 0; i < array_length(keys); i++){
				var key = keys[i];
				if(qs == ""){
					qs = "?";
				} else{
					qs +="&"
				}
				qs += string(key)+"=" + string(filters[$ key]);
			}
		}
		var req = new GliticRequest(self.manager, "/highscore/"+self.table_id+"/scores/"+qs, {
			meth:"GET"
		});
		req.req_type = GliticRequestType.highscores_fetch;
		req.subtable_name = subtable_name;
		req.table_id = self.table_id;
		req._send();
		return req;
	};
	submit = function(username, userid, primary_score, secondary_score, label){
		var d = {
			username : username,
			userid : userid,
			primary : primary_score,
			secondary : secondary_score,
			label: label,
			meth : "POST"
		}
		
		var req = new GliticRequest(self.manager, "/highscore/"+self.table_id+"/scores/", d);
		req.req_type = GliticRequestType.highscores_post;
		req.table_id = self.table_id;
		req._send();
		return req;
	};
	
	size = function(subtable){
		if(is_undefined(subtable)){
			subtable = "def";
		}
		return array_length(data[$subtable]);
	}
	
	data = function(subtable){
		if(is_undefined(subtable)){
			subtable = "def";
		}
		return self.data[$subtable];
	}
	
	draw = function(x,y, subtable_name){
		if(!manager.is_connected()){
			draw_text(x,y, "No game connected for table");
		}
		if(is_undefined(subtable_name)){
			subtable_name = "def";
		}
		if( variable_struct_exists(self.data, subtable_name)){
			var lineHeight = string_height("1.");
			var dat = self.data[$ subtable_name];
			var lim = array_length(dat)
			for(var i = 0; i < lim; i++){
				draw_text(x,y + i*lineHeight, string(1 + i) + ". " + string(dat[i].username) + " - " + string(dat[i].primary) + " / " + string(dat[i].secondary));
			}
		} else{
			draw_text(x,y, "Highscore subtable '"+subtable_name+"' not found");
		}
	};
}