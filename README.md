# rtaa_gis_framework_app_640
[![Build Status](https://travis-ci.org/Ricardh522/rtaa_gis.svg?branch=master)](https://travis-ci.org/Ricardh522/rtaa_gis)

Installation

1. Install the free Anaconda 32 bit environment manager to the inetpub directory.
2. Open the Anaconda Navigator, and create a new environment using the Python version 3.5
3. Use the package installer to install Django 1.10.x. and pywin32.
4. Next, from the terminal window activate the conda environment.
5. Using conda install the arcgis package from the esri channel.
6. Using conda install Pillow and reportlab
7. Next, use pip to install the packages listed in the requirements.txt file in the project root
8. In the terminal navigate to the Scripts folder and run wfastcgi-enable OR create the fastcgi program from within IIS.
9. Refer to the documentation on the wfastcgi script available online.
10. After all of the dependencies are installed, make sure the database configuration is correct.
11. Run the migrate task to build all of the tables for the project.  One database is needed to store all of the models.
12. Run the createsuperuser task to create the local admin for the django admin site
13. Run the collectstatic task to copy all of the static files from the dependencies to the project's static directory.
14. Run check, test, and runserver to verify that the django site is running correctly.