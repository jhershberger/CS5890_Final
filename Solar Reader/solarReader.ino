import processing.serial.*;
Serial serialPort;
PrintWriter output;
String fileName;
void setup(){
	fileName = "r040317";
	serialPort = new Serial(this, Serial.list()[0],9600);
	output = createWriter(fileName);
}
void writeOut(){
	output.println("Sensor Data");
}
void newFile(){
	fileName = "newFileName";
	output.flush();
	output.close();
	output = createWriter(fileName);
}
void packUp(){
	output.flush();
	output.close();
	exit();
}