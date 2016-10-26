import ldap3
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import logging


class LDAPQuery:
    """
    Instantiate this class with a remote user name and
        perform queries on Active Directory or LDAP
    """
    def __init__(self, username, ldap_url):
        self.username = username
        self.target_groups = ['GIS', 'Planning', 'Operations']
        self.server = Server(ldap_url, get_info=ALL)
        logging.info(self.server.info)

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
            logging.error(e.args)

        slicegroup = list()
        total_entries += len(conn.response)
        for entry in conn.response:
            try:
                logging.info(entry['dn'], entry['attributes'])
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
            logging.debug(e.args)

        # print(target_groups)
        logging.info(slicegroup)
        if len(slicegroup):
            pass

        return slicegroup

if __name__ == "__main__":
    query = LDAPQuery("Richard P. Hughes", "gisapps.aroraengineers.com")
    x = query.get_groups()
    logging.info(x)

