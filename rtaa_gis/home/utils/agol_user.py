import os
import sys
import arcgis
import django
import datetime
import time
from datetime import timedelta
from datetime import datetime
from django.conf import settings
import pprint

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rtaa_gis.settings'
django.setup()

LDAP_URL = settings.LDAP_URL

##############################################
if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")):
    os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/agol_UserCleanup.txt")
file = open(log_path, 'w')
file.close()
##############################################


def loggit(text):
    file = open(log_path, 'a')
    file.write("{}\n".format(text))
    pprint.pprint("{}\n".format(text))
    file.close()


###############################################


def agol_user(user_obj):
    """This agol_user function will create users in AGOL.  We are not using this.
    Instead we are automatically adding users as Level1 Viewers through SAML and then
    removing inactive users after 1 month"""
    loggit("agol_user script run {}".format(datetime.today()))
    try:
        username = user_obj.username
        firstName = user_obj.first_name
        lastName = user_obj.last_name
        email = user_obj.email
        localname = username.split("\\")[-1]

        if LDAP_URL == "renoairport.net":
            provider = "enterprise"
            password = None
            username = "{}_RTAA".format(localname)
            idpUsername = username

        else:
            provider = "arcgis"
            password = "testeruser123"
            username = "{}_RTAA".format(localname)
            idpUsername = None

        gis = arcgis.gis.GIS(url="https://rtaa.maps.arcgis.com",
                             username="data_owner",
                             password="GIS@RTAA123!")
        me = gis.users.me
        user = gis.users.get(username="{}".format(username))

        resp = {}

        if user:
            pass
            # account.delete(reassign_to='data_owner')
        else:
            # create an account
            if LDAP_URL == "renoairport.net":

                user = gis.users.create(username=username,
                                        firstname=firstName,
                                        lastname=lastName,
                                        email=email,
                                        level=1,
                                        role="org_viewer",
                                        provider=provider,
                                        password=password,
                                        idp_username=idpUsername)
            else:
                user = gis.users.create(username=username,
                                        firstname=firstName,
                                        lastname=lastName,
                                        email=email,
                                        level=1,
                                        role="org_viewer",
                                        provider=provider,
                                        password=password)

        if user:
            # ensure user is in the groups required for viewing
            target_groups = {
                "8aedb0ecfe6b417796993fb8ed4cfe0a": 'Published Layers',
                "90d7bc6eeaf94a24a661782a1d1ba0dc": 'Web Maps',
                "0d23c3513ba141c2b21b0c4b7325da1c": 'Basemaps in Web Mercator',
                "743f7e0190b6455da99dd847a3e76ab9": 'Basemaps in StatePlane'
            }
            user_groups = user.groups

            if len(user_groups):
                # if a user's group is included in the target_groups, remove it from the obj
                for gr in user_groups:
                    if gr.id in target_groups:
                        del(target_groups[gr.id])

            # for the remaining groups that the user is not a member of add them
            if len(target_groups):
                for group_id in target_groups:
                    # add the user to the remaining target_groups
                    agol_group = gis.groups.get(group_id)
                    if agol_group:
                        agol_group.add_users([username])
                # reset the user object to get the new groups list
                user = gis.users.get(username="{}".format(username))
            final_groups = user.groups
            resp["code"] = 0
            resp["message"] = username
            resp["groups"] = final_groups

        else:
            resp["code"] = -1
            resp["message"] = "error. Unable to create user"
            resp["groups"] = None

        return resp

    except Exception as e:
        raise Exception(e)


def clear_old_users():
    loggit("clear_old_users script run {}".format(datetime.today()))
    gis = arcgis.gis.GIS(url="https://rtaa.maps.arcgis.com",
                         username="data_owner",
                         password="GIS@RTAA123!")

    current_date = datetime.today()
    month_ago = current_date - timedelta(days=30)

    all_users = gis.users.search(query='*')
    number_inactive = 0
    for user in all_users:
        last_login = user.lastLogin
        if last_login != -1:
            login_date = datetime.fromtimestamp(last_login / 1000)
            if login_date < month_ago:
                if user.level == '1':
                    try:
                        user.delete()
                        number_inactive += 1
                        loggit("User {} removed from AGOL".format(user))
                    except Exception as e:
                        loggit(e)
                else:
                    loggit("Level {} {}, {}, inactive over 1 month.".format(user.level, user.role, user.username))
    if not number_inactive:
        loggit("Zero Level 1 Viewers have been inactive for 1 month or more")


if __name__ == "__main__":
    clear_old_users()
