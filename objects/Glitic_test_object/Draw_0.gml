draw_set_color(c_white);
if( glitic_is_connected()){
	draw_text(32,32,"Glitic connected!");
	draw_text(32,64,global.GliticData.game.name);
} else{
	draw_text(32,32,"Glitic: No Game Connected");
}