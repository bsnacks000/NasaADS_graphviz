### NASA ADS: Graph Vizualization Tool
#### DATA 620: Final Project - John DeBlase and Daina Bouquin

This repo contains files to allow you to locally run a the NASA-ADS Vizualization Tool. This Flask app allows a user to visualize information about publication patterns in specific domains of astronomy and astrophysics. The app uses data from the [SAO/NASA Astrophysics Data System](https://ui.adsabs.harvard.edu/) and is powered by Flask and sigma.js.

####To build and run the app locally:
1. clone this repo
2. create a fresh [virtual env](http://docs.python-guide.org/en/latest/dev/virtualenvs/) in that directory
3. activate the venv (tested on Python 2.7.9 + 2.7.11)
4. pip install dependencies
5. Run python app.py in the top level of the App directory to boot the server to localhost:5000

To just run the app with our ready made database, you can just pip install flask, numpy and pandas with an installation of Python 2.7.9 +
```
pip install flask numpy pandas
```
If you want to re-build the database or add more subjects using our processing classes in the Data Cleaning top level folder you will need to add several more packages to manually run scripts
```
pip install ads sqlalchemy odo jupyter
```
Alternatively you can install everything using requirements.txt
```
pip install -r requirements.txt
```

Instructions for building the database can be found each of the ipython notebooks in the Data Cleaning folder. Be forewarned that this process is not automatic and will require the user to correctly create additional .py files in the orm folder.
