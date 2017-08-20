# rtaa_gis_framework_app_640
[![Build Status](https://travis-ci.org/Ricardh522/rtaa_gis.svg?branch=master)](https://travis-ci.org/Ricardh522/rtaa_gis)

Installation

- Install the free Anaconda 32 bit or 64 bit environment manager to the inetpub directory.

- Open the Anaconda Navigator, and create a new environment using the Python version 3.5

- Use the package installer to install Django 1.10.x, pywin32, pillow, and reportlab

- Next, from the terminal window activate the rtaa_gis conda environment.

- Using conda install the arcgis package from the esri channel.

- Next, use pip to install the packages listed in the requirements.txt file in the project root

- In the terminal navigate to the Scripts folder and run wfastcgi-enable OR create the fastcgi program from within IIS.

- Refer to the documentation on the wfastcgi script available online.

- After all of the dependencies are installed, make sure the database configuration is correct.

- Run the migrate task to build all of the tables for the project.  One database is needed to store all of the models.

- Run the createsuperuser task to create the local admin for the django admin site

- Run the collectstatic task to copy all of the static files from the dependencies to the project's static directory.

- Run check, test, and runserver to verify that the django site is running correctly.

- After building the document store, run the dump_fixtures.py script to create the test fixtures