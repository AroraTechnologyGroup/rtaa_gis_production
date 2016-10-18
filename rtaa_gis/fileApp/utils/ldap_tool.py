import ldap3
from ldap3 import Server, Connection, ALL, NTLM

server = Server('gisapps.aroraengineers.com', get_info=ALL)
conn = Connection(server, user="GISAPPS\\gissetup", password="AroraGIS123!", authentication=NTLM,
                  auto_bind=True)

print(server.info)
print(conn.extend.standard.who_am_i())

