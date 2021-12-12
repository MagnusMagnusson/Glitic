var tableList = Glitic().table_list();
var expectations;
if Glitic().is_connected(){
	expectations = connectedExpectation;
} else{
	expectations = disconnectedExpectation
}

var name = string(Glitic().game.name);
var tableCount = string(array_length(Glitic().table_list()));
var _id = string(Glitic().game.id);
draw_text(32, 160, "Connected game information test");
draw_text(32, 160 + 1 * 32, "Game ID : '"+string(_id)+"'. Expected '"+string(expectations.id)+"'");
draw_text(32, 160 + 2 * 32, "Game name : '"+string(name)+"'. Expected '"+string(expectations.name)+"'");
draw_text(32, 160 + 3 * 32, "Highscore tables found : '"+string(tableCount)+"'. Expected '"+string(expectations.tableCount)+"'");