# Travelling Salesman Tour planning tool.

![alt text](https://github.com/cjflanagan/travelling_salesman_for_trips/blob/master/front.jpg)

![alt text](https://github.com/cjflanagan/travelling_salesman_for_trips/blob/master/result.jpg)

**Introduction**

The TSP is famous NP-hard problem to which scholars have dedicated their entire careers to focus on. While there is no provably optimal solution, there are a number of solvers which get extremely close to what the optimal. In this tool I was trying to solve a specific problem I encountered recently, and one which I assume more people encounter...

**Problem being solved:**
While planning a trip to Europe I had seven cities I wanted to visit but I was unsure what the most efficient order I should visit them in.
This is the tool I wish I had to help me plan that trip and could not find.

**To run flask app _from parent directory_ :**
> pip install -r requirements.txt

> export FLASK_APP=app/main.py

> flask run

**Files**

- **app/main.py**
    - Primary file that routes are managed from.
    - compute_tour function is the primary method which coordinates the organization of the input coordinates, calls the calulation methods in the different files and pushes the results to the results.html file.

- **app/distance_calc.py**
    - File that querys for the disatances between each point and constructs the necessary distance matrix which is the input into the ortools libraries.

- **app/tsp_logic.py**
    - File that interacts with the ortools libraries. Responsible for the input of the distance matrix and handling of the tool output.

- **app/templates/base.html**
    - Base html which is shared throughout the webapp

- **app/templates/index.html**
    - Home page of tool. Takes input from user through display of map.

- **app/templates/results.html**
    - Displays the results with markers being added on map and animation applied.

- **app/templates/about.html**
    - Some useful information about the project and the TSP problem.

- **app/static/index.js**
    - javascript code for the webapp. Note: there is still some javascript in the html files - this is due to this code needing to call the python functions and when placed in index.js it did not work.

![alt text](https://github.com/cjflanagan/travelling_salesman_for_trips/blob/master/about.jpg)
