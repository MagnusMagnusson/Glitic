_log = [];

w = room_width - x;
h = room_height - y;

log = function(msg){
	var now = date_current_datetime();
	array_insert(_log, 0, msg);
}