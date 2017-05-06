import java.io.*;
import java.util.*;

public class Formatter3{
	public static void main(String[] args){
	Scanner input = new Scanner(System.in);
	String filepath = input.next();
	
	String line = "";
	int count = 0;
	String temp = "";
	double temp2 = 0.0;
	double av1 = 0;
	double av2 = 0;
	double av3 = 0;
	double av4 = 0;
	double av5 = 0;
	double av6 = 0;
	double av7 = 0;
	double av8 = 0;
	try{
		Scanner reader = new Scanner(new File(filepath));
	    File outFile = new File ("5-4(8.38-22.22)out.txt");
	    FileWriter fWriter = new FileWriter (outFile);
	    PrintWriter pWriter = new PrintWriter (fWriter);
		while(reader.hasNext()){
			temp = reader.next();
			if(temp.matches("Reading")){
				temp = reader.next();
				if(temp.matches("1:")){
					if(reader.hasNextDouble()){
						temp2 = reader.nextDouble(); 
						av1 += temp2;
					}else{temp = reader.next();}
				}else if(temp.matches("2:")){
					if(reader.hasNextDouble()){
						temp2 = reader.nextDouble(); 
						av2 += temp2;
					}else{temp = reader.next();}
				}else if(temp.matches("3:")){
					if(reader.hasNextDouble()){
						temp2 = reader.nextDouble(); 
						av3 += temp2;
					}else{temp = reader.next();}
				}else if(temp.matches("4:")){
					if(reader.hasNextDouble()){
						temp2 = reader.nextDouble(); 
						av4 += temp2;
					}else{temp = reader.next();}
				}else if(temp.matches("5:")){
					if(reader.hasNextDouble()){
						temp2 = reader.nextDouble(); 
						av5 += temp2;
					}else{temp = reader.next();}
				}else if(temp.matches("6:")){
					if(reader.hasNextDouble()){
						temp2 = reader.nextDouble(); 
						av6 += temp2;
					}else{temp = reader.next();}
				}else if(temp.matches("7:")){
					if(reader.hasNextDouble()){
						temp2 = reader.nextDouble(); 
						av7 += temp2;
					}else{temp = reader.next();}
				}else if(temp.matches("8:")){
					if(reader.hasNextDouble()){
						temp2 = reader.nextDouble(); 
						av8 += temp2;
					}else{temp = reader.next();}
				}
			}
			if(temp.matches("\\d\\d:00")){
				pWriter.print(temp);
				pWriter.print("\t"+av1/60);
				pWriter.print("\t"+av2/60);
				pWriter.print("\t"+av3/60);
				pWriter.print("\t"+av4/60);
				pWriter.print("\t"+av5/60);
				pWriter.print("\t"+av6/60);
				pWriter.print("\t"+av7/60);
				pWriter.print("\t"+av8/60+"\n");
				
				av1 = 0;
				av2 = 0;
				av3 = 0;
				av4 = 0;
				av5 = 0;
				av6 = 0;
				av7 = 0;
				av8 = 0;	
				
			}


		}
		pWriter.flush();
	    pWriter.close();
	}
	catch(FileNotFoundException e) {
            System.out.println(
                "Unable to open file '" + 
                filepath + "'");                
    }
    catch(IOException e) {
            System.out.println(
                "Error reading file '" 
                + filepath + "'");                  
            
    }
        
	
	}
}