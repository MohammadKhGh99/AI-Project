To Run The Program:
	python3 game.py

There are two ways to run the program:
	When you run the above command a message will appear asking the user if you want to run the program by GUI 
	or just print the result and if the algorithm successed or failed.

1) By GUI:
	* When the initial message appear write "gui" then press Enter.
	* Then choose the sizes of the board, by default it is 5x5.
	* Then the GUI will appear to you, you can have fun now 😁.

2) By Print:
	* When the initial message appear write "print" then Enter.
	* Then choose the sizes of the board, by default it is 5x5.
	* Now, you have to choose which algorithm to run on the board:
		* If you choose LBS:
			* then you have to choose the number od initial states you want.
		* If you choose CSP:
			* You can choose whatever combination you want from the heuristics of CSP (separated by comma).
		* Otherwise, just press Enter and the magic will happen.
	* When the algorithm finishes, a message will appear saying to you:
		* If the algorithm has succeeded in finding a solution for the board, and the solved board will be printed out.
		* If the algorithm failed in finding a solution.
		* IF the timeout reached (3 minutes).
	