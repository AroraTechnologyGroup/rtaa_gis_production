import ldap3
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE


class LDAPQuery:
    """
    Instantiate this class with a remote user name and
        perform queries on Active Directory or LDAP
    """
    def __init__(self, username, ldap_url):
        self.username = username
        self.server = Server(ldap_url, get_info=ALL)
        print(self.server.info)

    def get_groups(self):
        conn = Connection(self.server, user="GISAPPS\\gissetup", password="AroraGIS123!", authentication=NTLM,
                               auto_bind=True)
        total_entries = 0
        try:
            conn.search(
                search_base="dc=GISAPPS, dc=aroraengineers, dc=com",
                search_filter="(&(objectClass=User)(cn={}))".format(self.username),
                search_scope=SUBTREE,
                attributes=ldap3.ALL_ATTRIBUTES,
            )

        except Exception as e:
            print(e.args)

        total_entries += len(conn.response)
        target_groups = []
        for entry in conn.response:
            try:
                print(entry['dn'], entry['attributes'])
                groups = entry['attributes']['memberOf']
                for x in groups:
                    target_groups.append(x.split(',')[0].split('=')[-1])
            except KeyError:
                pass

        # print('Total entries retrieved', total_entries)
        conn.unbind()
        # print(target_groups)
        return target_groups

if __name__ == "__main__":
    query = LDAPQuery("Richard P. Hughes", "gisapps.aroraengineers.com")
    x = query.get_groups()
    print(x)

