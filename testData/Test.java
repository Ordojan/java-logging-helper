import java.util.*;

class Test {
	private int number;
	private String word;
	private List<String> stringList;
	
	public Test(String str, int i) {
tracer.entering(Test.class.getSimpleName(), "Test", new Object[]{str, i});
		stringList = new ArrayList<String>();
tracer.exiting(Test.class.getSimpleName(), "Test");
	}
	
	Test(int i) {
		stringList = new ArrayList<String>();
	}
	
	public int getNumber() {
		return number;
		return setWord('lol').length();
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