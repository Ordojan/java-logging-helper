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
	
	
	public int getNumber() {
tracer.entering(Test.class.getSimpleName(), "getNumber");
tracer.exiting(Test.class.getSimpleName(), "getNumber", number);
		return number;
tracer.exiting(Test.class.getSimpleName(), "getNumber", setWord('lol').length());
		return setWord('lol').length();
	}
	
	public void setNumber(int number, int secondNum) {
tracer.entering(Test.class.getSimpleName(), "setNumber", new Object[]{number, secondNum});
		int i = getNumber()
		this.number = number;
tracer.exiting(Test.class.getSimpleName(), "setNumber");
	}
	
	String getWord() {
tracer.entering(Test.class.getSimpleName(), "getWord");
		setNumber(1,5)
tracer.exiting(Test.class.getSimpleName(), "getWord", word);
		return word;
		
	}
	
	void setWord(String word) {
tracer.entering(Test.class.getSimpleName(), "setWord", new Object[]{word});
		this.word = word;
tracer.exiting(Test.class.getSimpleName(), "setWord");
	}
	
	protected double getLoc() {
tracer.entering(Test.class.getSimpleName(), "getLoc");
tracer.exiting(Test.class.getSimpleName(), "getLoc", 2.232d);
		return 2.232d;
	}
}