# Design Document
This file should discuss how you implemented your project and why you made the design decisions you did, both technical and ethical. Your design document as a whole should be at least several paragraphs in length. Whereas your README.md is meant to be a user’s manual, consider your DESIGN.md your opportunity to give the staff a tour of your project underneath its hood.

## Technical Decisions
### In this section, share and justify the technical decisions you made.

On a broad level, Rohan and I decided to use Python, Flask, and HTML to create our project since these were the languages freshest in our head, and it made sense to use Flask and HTML to create a website based platform. We ran into a number of design challenges whilst navigating through our final project. First of all, we noticed immediately after handing in our proposal that creating a poker hand solver would be intensely difficult. For one, there are many ways to play poker effectively, and no one way is superior. Second, to create a solver, we would need a repository of poker hand equities (which can be achieved by simulating a large number of hands and aggregating their percentage chance of winning), and this is quite difficult. To rectify these design challenges, we firstly decided to combine two common forms of playing poker (a mathematical and a practical approach) to integrate in our project. To address the second challenge, we decide to import a poker equity solver library into our project, partly also because we noticed there were many of these in a variety of coding languages online. Ultimately we decided that a solver was much more unique, and there were not that many of these on the internet.

To provide a bit more background on how our solver works, we take into account the mathematics behind poker as an initial assessment of what to do, then take into account practical variables such as pre-flop aggression and opponent type as a secondary "tie breaker" of sorts. If the solver's reccomendation to call is clear (your equity is much larger than your pot odds), then these secondary variables do not get implemented in the code.

Throughout the project, a variety of CS50 backed tools were extremely helpful, including Bootstrap and W3Schools.

## Ethical Decisions
### What motivated you to complete this project? What features did you want to create and why?

Our main motivation behind executing this project is that we love poker, and wanting to create something that poker players at Harvard could use. Poker solvers in the status quo are either extremely rare, unreliable (not backed by solid poker principles) or expensive (we only found one free poker website)! Initially, we wanted to code the equity calculator ourselves, but realized that thousands of people have already done this. Tackling the poker solver portion of the project would be much more unique.


### Who are the intended users of your project? What do they want, need, or value?

The intended users of our project are 1. Those who wish to learn poker 2. Experienced players who wish to improve their game. By having a variety of functions (a guide for poker, a solver, and two quizes a basic quiz and an advanced training simulator) poker players from all walks of life can use our solver.

These are the users who interact directly with our project, and intuitively, they want and need a way to improve their poker play. Depending on their view on poker, they may value the game as a purely entertaining pass time, or even a source of income. Hopefully our project will benefit poker players 


You should consider your project's users to be those who interact _directly_ with your project, as well as those who might interact with it _indirectly_, through others' use of your project.



### How does your project's impact on users change as the project scales up? 
You might choose one of the following questions to reflect on:
* How could one of your project's features be misused?
* Are there any types of users who might have difficulty using your project?
* If your project becomes widely adopted, are there social concerns you might anticipate?


