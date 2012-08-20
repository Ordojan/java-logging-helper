import java.util.*;

class Test {
	private int number;
	private String word;
	private List<String> stringList;
	
	public Test(String str, int i) {
		stringList = new ArrayList<String>();
	}
	
	Test(int i) {
		stringList = new ArrayList<String>();
	}
	
	public int getNumber() {
		return number;
	}
	
	public void setNumber(int number, int secondNum) {
		int i = getNumber()
		this.number = number;
	}
	
	String getWord() {
		setNumber(1,5)
		return word;
	}
	
	void setWord(String word) {
		this.word = word;
	}
	
	protected double getLoc() {
		return 2.232d;
	}
}