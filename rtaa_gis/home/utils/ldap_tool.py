import ldap3
import django
import sys
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rtaa_gis.settings'
django.setup()
from django.conf import settings
from django.contrib.auth.models import User, Group


class LDAPQuery:
    """
    Instantiate this class with a remote user name and
        perform queries on Active Directory or LDAP
    """
    def __init__(self, username, ldap_url):
        self.username = username.split("\\")[-1]

        self.target_groups = [
            '_RTAA GIS',
            '_RTAA Airport Economic Development',
            '_RTAA Finance & Administration',
            '_RTAA Information Services',
            '_RTAA Landside Operations',
            '_RTAA Operations & Public Safety',
            '_RTAA Planning',
            '_RTAA Planning and Engineering',
            '_RTAA Police Management',
            '_RTAA Police Officers',
            '_RTAA Stead Airport',
            '_RTAA Work Orders',
            'Arora'
        ]
        for group in self.target_groups:
            try:
                Group.objects.get(name=group)
            except Group.DoesNotExist:
                Group.objects.create(name=group)
        if settings.LDAP_URL == "gisapps.aroraengineers.com":
            # self.server = Server(ldap_url, port=636, get_info=ALL, use_ssl=True)
            self.server = Server(ldap_url, get_info=ALL)
        else:
            self.server = Server(ldap_url, get_info=ALL)

    def get_groups(self):

        slicegroup = list()
        try:
            if settings.LDAP_URL == "renoairport.net":
                conn = Connection(self.server, user="RENOAIRPORT\\AroraTeam", password="@R0r@G1$", authentication=NTLM,
                                  auto_bind=False)
            elif settings.LDAP_URL == "gisapps.aroraengineers.com":
                conn = Connection(self.server, user="GISAPPS\\gissetup", password="AroraGIS123:)", authentication=NTLM,
                              auto_bind=False)

            conn.bind()
            #conn.start_tls()
            total_entries = 0
            try:
                if settings.LDAP_URL == "renoairport.net":
                    conn.search(
                        search_base="dc=renoairport, dc=net",
                        search_filter="(&(objectclass=user)(sAMAccountName={}))".format(self.username),
                        search_scope=SUBTREE,
                        attributes=ldap3.ALL_ATTRIBUTES,
                    )
                else:
                    conn.search(
                        search_base="dc=GISAPPS, dc=aroraengineers, dc=com",
                        search_filter="(&(objectclass=user)(sAMAccountName={}))".format(self.username),
                        search_scope=SUBTREE,
                        attributes=ldap3.ALL_ATTRIBUTES,
                    )

            except Exception as e:
                print("Exception arguments: {}".format(e.args))

            total_entries += len(conn.response)
            print(conn.response)
            for entry in conn.response:
                try:
                    print("dn: [{}], attributes: {}".format(entry['dn'], entry['attributes']))
                    groups = entry['attributes']['memberOf']
                    for x in groups:
                        group = x.split(',')[0].split('=')[-1]
                        if group in self.target_groups:
                            slicegroup.append(group)
                except KeyError:
                    pass

            # print('Total entries retrieved', total_entries)
            try:
                conn.unbind()
            except Exception as e:
                print("Exception arguments: {}".format(e.args))

        except Exception as e:
            print(e)

        print(slicegroup)
        return slicegroup


if __name__ == "__main__":
    if settings.LDAP_URL == "renoairport.net":
        query = LDAPQuery("RENOAIRPORT\\AroraTeam", "renoairport.net")
    else:
        query = LDAPQuery("GISAPPS\\gissetup", "gisapps.aroraengineers.com")
    x = query.get_groups()
    print(x)

