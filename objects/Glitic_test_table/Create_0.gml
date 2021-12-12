getTables = function(){
	Glitic().table("Table A").fetch({
		ordering:"username",
		user_unique : "true"
	}).onSuccess(function(data){		
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("table('Table A').fetch() arrived successfully");
		}
	}).onFail(function(data, status){
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("table('Table A').fetch() failed with error code "+string(status) + ": " + string(data));
		}
	}).onException(function(data){
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("table('Table A').fetch() exception:" +  string(data));
		}
	});
	Glitic().table("Table B").fetch().onSuccess(function(data){		
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("table('Table B').fetch() arrived successfully");
		}
	}).onFail(function(data, status){
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("table('Table B').fetch() failed with error code "+string(status) + ": " + string(data));
		}
	}).onException(function(data){
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("table('Table B').fetch() exception:" +  string(data));
		}
	});
	Glitic().table("Table C").fetch().onSuccess(function(data){		
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("table('Table C').fetch() arrived successfully");
		}
	}).onFail(function(data, status){
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("table('Table C').fetch() failed with error code "+string(status) + ": " + string(data));
		}
	}).onException(function(data){
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("table('Table C').fetch() exception:" +  string(data));
		}
	});
}