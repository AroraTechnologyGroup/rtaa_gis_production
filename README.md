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

IIS Configuration

<?xml version="1.0" encoding="UTF-8"?>

<configuration>

	<appSettings>
	    <!-- Required settings -->
	    <add key="PYTHONPATH" value="C:\inetpub\rtaa_gis_django\rtaa_gis" />
	    <add key="WSGI_HANDLER" value="django.core.wsgi.get_wsgi_application()" />
	    <add key="WSGI_LOG" value="C:\inetpub\rtaa_gis_django\rtaa_gis\logs\wsgi.log" />
	    <add key="WSGI_RESTART_FILE_REGEX" value=".*((\.py)|(\.config))$" />
	    <add key="DJANGO_SETTINGS_MODULE" value="rtaa_gis.settings" />
	</appSettings>
    <system.webServer>
        <handlers accessPolicy="Read, Execute, Script">
        	<clear />
            <add name="Python FastCGI" path="*" verb="*" type="" modules="FastCgiModule" scriptProcessor="C:\inetpub\Anaconda3\envs\rtaa_gis\python.exe|C:\inetpub\Anaconda3\envs\rtaa_gis\Lib\site-packages\wfastcgi.py" resourceType="Unspecified" requireAccess="Script" />
        </handlers>
        <httpProtocol>
            <customHeaders>
                <remove name="Access-Control-Allow-Headers" />
                <remove name="Access-Control-Allow-Origin" />
                <remove name="Access-Control-Allow-Methods" />
                <add name="Access-Control-Allow-Headers" value="Content-Type, Content-Range, Content-Length, X-Requested-With, X-CSRFToken, Authorization" />
                <add name="Access-Control-Allow-Credentials" value="true" />
                <add name="Access-Control-Allow-Methods" value="OPTIONS, GET, POST, DELETE" />
                <add name="Access-Control-Allow-Origin" value="https://gis.renoairport.net" />
            </customHeaders>
        </httpProtocol>
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
        <security>
            <authorization>
                <add accessType="Allow" users="*" roles="" />
            </authorization>
        </security>
    </system.webServer>
</configuration>
