/*
	GliticUtil
	A general collection of contained functions intended to either handle completely or aid in 
	Glitic operations. It is encapsulated within a struct to minimize polluting the global namespace.
*/

global.GliticUtil = {
	//str_split(str, del). 
	//Takes in a string and delimeter and returns an array of strings that were divided by said delimeter
	// ex. str_split('test_string_here', '_') => ["test","string","here"]
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
	
	//EMPTY_GAME()
	//Returns a 'clean' object struct with nothing in it.
	//Called whenever the game struct is initialized or reset (f.i on disconnect)
	EMPTY_GAME : function(){
		return  {
			id : undefined,
			name : undefined,
			tables : [],
		};
	},
	
	//NETWORK_OBJECT()
	//Finds the instance of the network manager instance and  returns it
	//If no instance exists in the room it is created first. 
	NETWORK_OBJECT : function(){		
		if(!instance_exists(o_glitic_network_manager)){
			instance_create_depth(0,0,0,o_glitic_network_manager)
		}
		return o_glitic_network_manager;
	},
	
	//HTTP_ASYNC_RESPONSE(async_load)
	//Top level call for the http event.
	//Takes the async_load map generated by the event and prepares it for consumption by the Glitic library
	//Will retrieve the responsible request object, divert the request to correct subfunction, and call callback
	HTTP_ASYNC_RESPONSE : function(async_load){
		var req = undefined;
		var _id = async_load[? "id"];
		var http_status, result, status;
		status = async_load[?"status"];
		if(status == 1){ //We do not concern ourselves with in-progress responses. Skip the event and revisit it when the response is fully completed. 
			return;
		}
		try{ 
			http_status = async_load[?"http_status"];
			result = async_load[? "result"];
			req = global.GliticRequestMap[? _id]; //Retrieve the correct request object from global map. 
			var manager;
			if(is_undefined(req)){
				exit; //This response is not meant for Glitic, it is triggered by something else. Ignore. 
			} else{			
				req.status = http_status
				req.result = result;
				manager = req.owner;
				ds_map_delete(global.GliticRequestMap, async_load[?"id"]); // This is our request. Delete it from the in-waiting requests. 
			}
			
			if(status == 0){ //Good response. 
				if(http_status >= 200 && http_status < 300){ //Server accepted response
					var type = req.req_type;
					var data = {};
					switch(type){ //Decide who should handle this request. 
						case GliticRequestType.connect : { //Glitic().connect()
							data = global.GliticUtil.HTTP_ON_CONNECT(req, async_load);
							if(variable_struct_exists(req.conf,"success")){
								req.conf.success(data);
							}
							break;
						}
						case GliticRequestType.disconnect : { //Glitic().disconnect()
							global.GliticUtil.HTTP_ON_DISCONNECT(req);
							if(variable_struct_exists(req.conf,"success")){
								req.conf.success(data);
							}
							break;
						}
						case GliticRequestType.highscores_fetch : { //Glitic().table().get()
							data = global.GliticUtil.HTTP_ON_HIGHSCORES_FETCH(req, async_load);
							if(variable_struct_exists(req.conf,"success")){
								req.conf.success(data);
							}
							break;
						}
						default:{ //Something went wrong, whoever generated this request did not mark it as a valid type. 
							show_debug_message("UNKNWON REQUEST TYPE "+ string(type));
						}
					}
				} else{ //Server rejected the request. Trigger fail callback.
					if(variable_struct_exists(req.conf,"fail")){
						req.conf.fail(result, http_status);
					}
				}
			} else{	//Request came back in failed state. 					
				if(variable_struct_exists(req.conf,"fail")){
					req.conf.fail(result, http_status);
				}
			}
			
			//Whatever happens response is always called. 
			if(!is_undefined(req) && variable_struct_exists(req.conf,"response")){
				req.conf.response(data);
			}
		} catch(e){		
			//Something raised an exception in processing message. Alert the exception handling callback, or bubble exception up. 
			if(!is_undefined(req) && variable_struct_exists(req.conf,"caught")){
				req.conf.caught(e);
			} else{
				throw e;
			}
			//Whatever happens response is always called.
			if(!is_undefined(req) && variable_struct_exists(req.conf,"response")){
				req.conf.response(e);
			}
		}
	},
	
	//HTTP_ON_CONNECT(req,async_load)
	//A handler for the request and async_load indicating a connection to Glitic has been made.
	//Handle the request, parse data body, and fill in game.
	HTTP_ON_CONNECT : function(req, async_load){ //Connection has been made. 
		var manager = req.owner;
		var data = {};
		data = json_parse(async_load[? "result"]);
		//The response will include information about the connected game. Fill it in. 
		manager.game = data.game;
		manager.sToken = data.token;
		manager.connected = true;
		return data.game;
	},
		
	//HTTP_ON_DISCONNECT(req,async_load)
	//A handler for the request and async_load indicating a connection to Glitic has been terminated.
	//Handle the request, clear out game
	HTTP_ON_DISCONNECT : function(req){ //Connection has been terminated by client
		var manager = req.owner;
		manager.connected = false;
		//Clear out all game info.
		manager.game = global.GliticUtil.EMPTY_GAME();
		manager.cToken = undefined;
		manager.sToken = undefined;
	},
	
	//HTTP_ON_HIGHSCORES_FETCH(req,async_load)
	//A handler for the request and async_load indicating a table request has been served
	//Handle the request, fill table data, return table array
	HTTP_ON_HIGHSCORES_FETCH : function(req, async_load){ //A highscore table request has been recieved. 
		//Determine what table is being referenced in request. 
		var subtable = req.subtable_name;
		var table = req.table_id;
		var manager = req.owner;
		var data = {};
		data = json_parse(async_load[?"result"]);
		//Fill in table in memory before returning data to callback.
		manager.table(table).data[$ subtable] = data;
		return data;
	},
	
	//GENSTRING(n)
	//Generates a random base-64 string of length n.
	//Used to create random tokens, strings, id's, and other data
	//Ex. GENSTRING(7) => "2_cQL3m"
	GENSTRING : function(n){	
		var alph = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-_";
		var token = "";
		for(var i = 0; i < n; i++){
			token += string_char_at(alph, irandom(string_length(alph) - 1));
		}
		return token;
	},
	
	CREATENEWSETTINGS : function(){
	},
	
	LOADSETTINGS : function(){
		var valid = true;
		var buffer = buffer_load("glconf.dat");
		global.GliticLoadedSettings = {};
		try{
			if(buffer != -1){
		        var json = buffer_read(buffer, buffer_string);
		        buffer_delete(buffer)
		        var conf = json_parse(json);
				if(!is_struct(conf)){
					valid = false;
				}
				if(variable_struct_exists(conf, "clid")){
					global.GliticLoadedSettings[$ "clid"] = conf[$ "clid"];
				} else{
					valid = false;
				}
			} else{
				valid = false;
			}
		} catch(c){
			valid = false;
		}
		
		if(!valid){
			return global.GliticUtil.CREATENEWSETTINGS();
		}
	}
}


global.GliticRequestMap = ds_map_create();
global.GliticLoadedSettings = undefined;