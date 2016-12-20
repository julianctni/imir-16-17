Interactive Multimedia Information Retrieval
TU Dresden, Wintersemester 2016/17

Team: Finn Schlenk, Jonas Fischer, Julian Catoni, Stephan Dinter

Programming Language: Python (Version 3.5)


Task 2 - Color Layout Descriptior Image Search
----------------------------------------------

1. Usage

You need Python3 to use this program and have two options to start it.
Also make sure, you have the Pillow module for image analysis installed.

The PlantCLEF2016 data set needs to be put in a folder called 'PlantCLEF2016Test' in the main directory.
The folder structure should be as followed:

	└── task2  
	....├── PlantCLEF2016Test 
	....├── screenshots <-- screenshots of the Mac OS Build
	....├── assets   
	....|...└── index.csv <-- will later be build here, prebuilt index included  
	....├── src  
	....|...├── analyze.py  
	....|...├── app.py 
	....|...├── buildIndex.py 
	....|...├── search.py 			
	....|...└── utilities.py  
	....├── readme.txt   
	....├── result.css
	....├── result.html <-- will later be build here, example result included  
	....├── setup.py
	....└── ez_setup.py
 

1.1 GUI

For the GUI version you need the Tkinter module. You then can start the program by running: 

python3 app.py in the src folder. 

You also have the option to build an executable version by running:

python3 setup.py

A prebuild Mac OS version is included.


1.2 Commandline

cd src

python3 buildIndex.py
python3 search.py

Building the index can take up to 20 minutes. To search for similar images, enter an imagename from the dataset (e.g. 113227.jpg)

The functionality was tested on Ubuntu 16.04 and OS X El Capitan, Version 10.11.6