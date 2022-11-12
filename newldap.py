import ssl
from ldap3 import Server, Connection, ALL, SUBTREE

from flask import json
from ldap3 import Server, \
    Connection, \
    SUBTREE, \
    ALL_ATTRIBUTES, \
    Tls, MODIFY_REPLACE

OBJECT_CLASS = ['inetOrgPerson', 'organizationalPerson', 'person','top']
LDAP_HOST = 'ldap://localhost:10389'
LDAP_USER = 'rahul'
LDAP_PASSWORD = '000'
LDAP_BASE_DN = 'ou=users,dc=company,dc=com'
search_filter = "(displayName={0}*)"
tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1)


def find_ad_users(username):
    with ldap_connection() as c:
        c.search(search_base=LDAP_BASE_DN,
                 search_filter=search_filter.format(username),
                 search_scope=SUBTREE,
                 attributes=ALL_ATTRIBUTES,
                 get_operational_attributes=True)

    return json.loads(c.response_to_json())


def create_ad_user(username, forename, surname, new_password):
    with ldap_connection() as c:
        attributes = get_attributes(username, forename, surname)
        user_dn = get_dn(username)
        result = c.add(dn=user_dn,
                       object_class=OBJECT_CLASS,
                       attributes=attributes)
        if not result:
            msg = "ERROR: User '{0}' was not created: {1}".format(
                username, c.result.get("description"))
            raise Exception(msg)

        # unlock and set password
        c.extend.microsoft.unlock_account(user=user_dn)
        c.extend.microsoft.modify_password(user=user_dn,
                                           new_password=new_password,
                                           old_password=None)
        # Enable account - must happen after user password is set
        enable_account = {"userAccountControl": (MODIFY_REPLACE, [512])}
        c.modify(user_dn, changes=enable_account)

        # Add groups
        c.extend.microsoft.add_members_to_groups([user_dn], get_groups())


def ldap_connection():
    server = ldap_server()
    connection = Connection(server,          
                                user='uid=rahul,dc=company,dc=com', 
                                password='111')
    bind_response = connection.bind() # Returns True or False 
    return connection


def ldap_server():
    server_uri = f"ldap://localhost:10389"
    server = Server(server_uri, get_info=ALL)
    return server


def get_dn(username):
    return "uid={0},ou=users,dc=company,dc=com".format(username)


def get_attributes(username, forename, surname):
    return {
        "uid":username,
        "cn": username,
        "sn":username+"ss"
    }


def get_groups():
    postfix = ',OU=MyService,OU=My Groups,DC=test,DC=core,DC=bogus,DC=org,DC=uk'
    return [
         ('CN=ROLE_A%s' % postfix)
    ]


ff = create_ad_user('pop','pop','pop','000')
# ff = ldap_connection()
print(ff)