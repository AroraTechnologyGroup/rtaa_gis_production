# rtaa_gis_framework_app_640
[![Build Status](https://travis-ci.org/Ricardh522/rtaa_gis.svg?branch=master)](https://travis-ci.org/Ricardh522/rtaa_gis)

Installation

- Install the free Anaconda 32 bit or 64 bit environment manager to the inetpub directory.

- Open the Anaconda Navigator, and create a new environment using the Python version 3.5

- Use the package installer to install Django 1.11.x, pywin32, pillow, and reportlab

- Next, from the terminal window activate the rtaa_gis conda environment.

- Using conda install the arcgis package from the esri channel. (conda install -c esri arcgis)

- Next, use pip to install the packages listed in the requirements.txt file in the project root (pip install -r requirements.txt)

- In the terminal navigate to the Scripts folder and run wfastcgi-enable OR create the fastcgi program from within IIS.

- Refer to the documentation on the wfastcgi script available online.

- After all of the dependencies are installed, make sure the database configuration is correct.

- Run the migrate task to build all of the tables for the project.  One database is needed to store all of the models.

- Run the createsuperuser task to create the local admin for the django admin site

- Run the collectstatic task to copy all of the static files from the dependencies to the project's static directory.

- Run check, test, and runserver to verify that the django site is running correctly.

- After building the document store and any additional tables, run the dump_fixtures.py script to create the test fixtures

- If launching on IIS configure the URL Rewrite Rules in the web.config as follows
        ```
        <rewrite>
            <rules>
                <clear />
                <rule name="Redirect to HTTPS" enabled="true" patternSyntax="ECMAScript" stopProcessing="true">
                    <match url="(.*)" />
                    <conditions logicalGrouping="MatchAny" trackAllCaptures="false">
                        <add input="{HTTPS}" pattern="^OFF$" />
                    </conditions>
                    <action type="Redirect" url="https://{HTTP_HOST}/applications/{R:1}" />
                </rule>
                <rule name="setRootSlash" stopProcessing="true">
                    <match url="(.*)" />
                    <conditions logicalGrouping="MatchAll" trackAllCaptures="false">
                        <add input="{PATH_INFO}" pattern="/applications$" />
                    </conditions>
                    <action type="Redirect" url="https://{HTTP_HOST}/applications/" />
                </rule>
                <rule name="setHeaderValues" enabled="true" stopProcessing="false">
                    <match url="(.*)" />
                    <conditions logicalGrouping="MatchAll" trackAllCaptures="false" />
                    <serverVariables>
                        <set name="SCRIPT_NAME" value="{PATH_INFO}" />
                        <set name="PATH_INFO" value="/{R:0}" />
                        <set name="HTTP_X_ORIGINAL_ENCODING" value="{HTTP_ACCEPT_ENCODING}" />
                        <set name="HTTP_ACCEPT_ENCODING" value="0" />
                    </serverVariables>
                    <action type="None" />
                </rule>
            </rules>
        </rewrite>
        ```
        
        
Testing

- runtests.py is where each app's test suite is loaded
- within each test suite, the os.path is changed to the fixture dir, so each apps tests 


