draw_set_color(c_black);
draw_set_font(Glitic_test_font);
if( Glitic().is_connected()){
	draw_text(32,32,"Glitic: Connected");
	draw_text(32,64,"press <Spacebar> to disconnect from the testing game.");
} else{
	draw_text(32,32,"Glitic: Disconnected");
	draw_text(32,64,"press <Spacebar> to connect to the testing game.");
}

draw_text(32,96, "last request result was '"+ lastmessage+"'");