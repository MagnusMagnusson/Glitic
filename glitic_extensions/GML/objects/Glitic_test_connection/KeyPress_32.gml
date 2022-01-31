if(!Glitic().is_connected()){
	var request = Glitic().connect("ZukZY","FPyO-9o8ob9Rz")

	request.onSuccess(function(data){
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("Glitic.Connect() connection established");
		}
		Glitic_test_table.getTables();
	}).onException(function(error){		
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("Glitic.Connect() exception " + string(error));
		}
		lastmessage = "Glitic().connect() Exception occurred - " + string(error);
	}).onFail(function(data, status){
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("Glitic.Connect() rejected with status " + string(status) + ", " + string(data));
		}
	});
} else{
	var request = Glitic().disconnect();
	request.onSuccess(function(data){
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("Glitic.disconnect() connection established");
		}
	}).onException(function(error){		
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("Glitic.disconnect() exception " + string(error));
		}
	}).onFail(function(data, status){
		if(instance_exists(Glitic_test_log)){
			Glitic_test_log.log("Glitic.disconnect() rejected with status " + string(status) + ", " + string(data));
		}
	});
}