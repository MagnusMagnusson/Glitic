function GliticTable(tid, tname) constructor{
	table_id = tid;
	table_name = tname;
	data = [];
	ready = false;
	primary_asc = false;
	secondary_asc = false;
	user_unique = false;
	
	static fetch = function(page, pageSize, user_unique){};
	static search = function(filters, include_position){};
	static add = function(username, userid, primary_score, secondary_score, label){};
	static submit = function(){};
	static draw = function(){};
}