

Upon starting the program the databases are generated (none included in submission, will be created upon running the program )

Program created & ran via python3: 
	-python3 chat_app.py 

If the URL link (e.g. http://127.0.0.1:5000) gives a 403 error/any other error when trying to launch upon running the program, please try the following:
	-I apologize for this error, I wasn't able to diagnose the cause and unable to replicate it (happens randomly)
	-open up a private tab in your browser and paste the link there
	-completely restart your browser and try pasting the link there 
	-restart the program (chat_app.py) in the command line 

Steps to successfully run the program:  
	1.  Create your account (assuming this already hasn't been done)
		-click the register button
		-enter your credentials 
	2. Upon successful creation of your account, you will be redirected to the login page with a success message
		-enter your credentials
		-if the credentials are correct, you will be redirected to the messaging page 
	3. Once at the messaging page 
		-if the database for the chat isn't empty, all the messages will be loaded instantly 
		-if it is empty, no messages will load
		-the chatbox is updated in intervals of 15 seconds
		-user messages (from the account being utilized) will be updated instantly
	4. Upon logging out
		-login token will be set to 0
		-will be sent to logout page 
			-click the link to return to the login page
	5. Rinse and repeat 

Thanks for a great semester! 
