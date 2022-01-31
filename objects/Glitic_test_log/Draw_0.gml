draw_set_color(c_navy);

draw_rectangle(x,y,x+w,y+h, false);
draw_set_color(c_white);

draw_set_font(Glitic_test_font_consola);
draw_text(x + 16, y + 32, "Network Log");

var off = 48;

var i = 0; 
var l = array_length(_log);
while(i < l && off < h){
	var xx, yy, sep, width;
	xx = x + 16;
	yy = y + off;
	sep = 2+string_height("A");
	width = w - 32;
	
	draw_text_ext(xx, yy, _log[i], sep, width);
	off += 16 + string_height_ext(_log[i], sep, width);
	i++;
}