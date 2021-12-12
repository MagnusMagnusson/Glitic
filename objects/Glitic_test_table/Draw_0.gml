ex = [0, 300, 600]

if(Glitic().is_connected()){
	var A,B,C;
	A = Glitic().table("Table A");
	B = Glitic().table("Table B");
	C = Glitic().table("Table C");
	draw_text(x + ex[0], y - 32, "Table A is being drawn here");
	draw_text(x + ex[1], y-32, "Table B is being drawn here");
	draw_text(x + ex[2], y-32, "Table C is being drawn here");
	
	draw_text(x + ex[0], y, "Table A size: " + string(A.size()));
	draw_text(x + ex[1], y, "Table B size: " + string(B.size()));
	draw_text(x + ex[2], y, "Table C size: " + string(C.size()));
	
	A.draw(x + ex[0], y + 32);
	B.draw(x + ex[1], y + 32);
	C.draw(x + ex[2], y + 32);
} else{
	draw_text(x + ex[0], y-32, "Not connected, Table A not shown");
	draw_text(x + ex[1], y-32, "Not connected, Table B not shown");
	draw_text(x + ex[2], y-32, "Not connected, Table B not shown");
}