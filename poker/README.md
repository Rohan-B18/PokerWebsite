As a broad overview, our website teaches users and includes the following:
* How to play poker strategically (Guide to Poker page)
* What to do when given community cards, pot size, and equity, and other contributing factors (Poker Solver)
* A tester that gives the user a random hand and asks what action they should take (Advanced Poker Simulator)
* What our own tips and tricks are (Tips and Tricks)
* A quiz containing questions about equity and pot odds (Poker Knowledge Quiz)

Our website uses python to create the poker solver, and HTML / CSS to design the interface. We use flask to run the website. We have also used a few external resources / libraries to improve our project, including a poker equity solver (which gives users the percentage chance their hand will win, a critical variable for our poker solver) and code from both of our trivia and homepage problem sets.

To use our project, complete the following steps:

* Open our project.zip file
* Type cd poker into terminal
* Install the python poker engine by executing the following command: pip install PyPokerEngine
* Install flask if necessary by executing the following command: pip install flask
* Making sure that you are in the poker directory, execute flask run
* Click on the generate link (command C on mac) to visit our website
* Similar to the finance problem set, register for an account then log in
* When in the website, use the navigation bar on the top left of each page to visit particular pages
* Some pages will allow you to interact with specific buttons and drop down bars, but these are fairly intuitive!
    * In the quiz tab, click your answer of choice. The correct answer will pop up as green, the incorrect as red
    * In the poker solver tab, enter the needed inputs and variables. Some entries have drop down menus, others have short form response tables.
    * IMPORTANTLY: To enter your hole cards and communities cards, use the following format: [SUIT/CARD]
            * ie. Ace of Diamonds == DA ... King of Spades == SK
ᐧ