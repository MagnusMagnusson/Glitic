Glitic().connect("acdefghi","JObg-K8loxmX3").success(function(data){
	show_message(data);
}).caught(function(error){
	throw error;
}).fail(function(data){
	show_message("Fail");
	show_message(data);
});