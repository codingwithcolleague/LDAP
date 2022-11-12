from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError


def connect_ldap_server():

    try:
        
        # Provide the hostname and port number of the openLDAP      
        server_uri = f"ldap://localhost:10389"
        server = Server(server_uri, get_info=ALL)
        # username and password can be configured during openldap setup
        connection = Connection(server,          
                                user='uid=rahul,dc=company,dc=com', 
                                password='111')
        bind_response = connection.bind() # Returns True or False 
        return connection
    except LDAPBindError as e:
        connection = e


def get_ldap_users():
    
    # Provide a search base to search for.
    search_base = 'ou=users,dc=company,dc=com'
    # provide a uidNumber to search for. '*" to fetch all users/groups
    search_filter = '(uid=*)'

    # Establish connection to the server
    ldap_conn = connect_ldap_server()
    try:
        # only the attributes specified will be returned
        ldap_conn.search(search_base=search_base,       
                         search_filter=search_filter,
                         search_scope=SUBTREE, 
                         attributes=['cn','sn','uid'])
        # search will not return any values.
        # the entries method in connection object returns the results 
        results = ldap_conn.entries
        print("results",results)
    except LDAPException as e:
        results = e

# get_ldap_users()

def get_all_users_from_ldap():
    from ldap3 import Server, Connection, ALL
    server_uri = f"ldap://localhost:10389"
    server = Server(server_uri, get_info=ALL)
    conn = Connection(server, 'uid=rahul,ou=users,dc=company,dc=com', '000', auto_bind=True)
    eee = conn.search('ou=users,dc=company,dc=com', '(objectclass=person)')
    print("sss",conn.entries)

get_all_users_from_ldap()