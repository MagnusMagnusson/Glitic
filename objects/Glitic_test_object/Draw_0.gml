draw_set_color(c_white);
if( Glitic().is_connected()){
	draw_text(32,32,"Glitic connected!");
	draw_text(32,64,Glitic().game.name);
} else{
	draw_text(32,32,"Glitic: No Game Connected");
}