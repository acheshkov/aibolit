class Foo {
  void bar() {
    // some other code
    try {  // here!
      // some code
    } catch (Exception ex) {
		try {
		  // some code
		} catch (IOException iex) {
		  throw iex;
		}
    }
  }
}