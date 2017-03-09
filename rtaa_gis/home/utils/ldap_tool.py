import ldap3
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
from django.contrib.auth.models import User, Group
import logging


class LDAPQuery:
    """
    Instantiate this class with a remote user name and
        perform queries on Active Directory or LDAP
    """
    def __init__(self, username, ldap_url):
        self.username = username.split("\\")[-1]
        self.target_groups = ['GIS_admin', 'GIS_user', 'Utilities', 'Planning', 'Operations', 'Engineering']
        for group in self.target_groups:
            try:
                Group.objects.get(name=group)
            except Group.DoesNotExist:
                Group.objects.create(name=group)
        # self.server = Server(ldap_url, port=636, get_info=ALL, use_ssl=True)
        self.server = Server(ldap_url)

    def get_groups(self):
        slicegroup = list()
        try:
            # conn = Connection(self.server, user="AroraTeam", password="@R0r@G1$", authentication=NTLM,
            #                   auto_bind=True)
            conn = Connection(self.server)
            conn.bind()
            # conn.start_tls()
            total_entries = 0
            try:
                conn.search(
                    search_base="dc=renoairport, dc=net",
                    search_filter="(&(objectClass=User)(cn={}))".format(self.username),
                    search_scope=SUBTREE,
                    attributes=ldap3.ALL_ATTRIBUTES,
                )

            except Exception as e:
                print("Exception arguments: {}".format(e.args))

            total_entries += len(conn.response)
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
    query = LDAPQuery("siteadmin", "gisapps.aroraengineers.com")
    x = query.get_groups()
    print(x)

