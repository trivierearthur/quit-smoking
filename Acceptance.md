#Acceptance criterias 

- Your solution should be built using Python version 3.7 or later, so that you can focus on writing modern
Python code. The tools and libraries used to implement your habit tracker application are entirely your
own choice. However, you are not permitted to directly use or modify existing, third-party habit tracking
tools that you might find on the internet of elsewhere.

- The software you submit must come with detailed, self-contained installation and run instructions so that
it is clear how to install the project and use your habit tracker. A well-written README.md or similar is
enough, given that you provide all the information properly. Make sure your code is documented with
Python docstrings, too.

- The concept of a habit should be encoded as a class using object-oriented programming. Depending on
your design, you may or may not need more classes for this project.

-o Your tracker should be able to let users create at least two habit periods, namely weekly and daily habits.


- Your solution comes with 5 predefined habits (at least one weekly and one daily habit). It should be clearly
documented how new habits can be created with your solution. Also, make transparent how a user can
complete a task within a given period.

- For each habit, your system tracks when it has been created, and the date and time the habit tasks have
been completed.

- For each predefined habit, you should provide example tracking data for a period of 4 weeks. This example data will later be used for testing purposes as so called “test fixture”. It will also be helpful to validate
your approach as you program your solution, as you can more easily load habits when resorting to predefined data.

- You need some way of storing, or persisting, habit data in between user sessions. Storing and loading
data can either be done with a simple file-based solution, e.g., by reading and writing JSON files with
Python’s built-in json module, or with a relational database solution using tools like sqlite3. Both approaches can work well but going with a DB is likely more professional and can teach you more going
forward.

- Your solution has an analytics module that allows users to analyse their habits. The functionality of this
analytics module must be implemented using the functional programming paradigm. You are free to consider implementing other functionality as well, but these are the minimal requirements. Provide functionality to
- return a list of all currently tracked habits,
- return a list of all habits with the same periodicity,
- return the longest run streak of all defined habits,
- and return the longest run streak for a given habit.

- Your solution has to have a clean API that users understand. You do this by exposing a command line
interface (CLI) tool to the user that allows them to create, delete and analyse their habits. There are great
tools like fire or click to build CLIs, but you can also use a simple main loop for your program, e.g., with
the built-in input command to create an interactive menu. If you’re experienced in building graphical user
interfaces, you can alternatively build out a GUI, too. An idea could be to use tkinter or similar Pythonbased tools or go for a more modern web-development approach with flask or django. Just note that you
won’t gain any extra points with a more visually pleasing solution. In the end, the submission will be
graded according to the acceptance criteria and the quality of your Python code.

- The critical parts of your solution, in particular the validity of your habit tracking components and the
analytics module, should be tested by providing a unit test suite that can be run following the instructions
provided with the solution. It is recommended that you work with either pytest or unittest for this.