from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django_python3_ldap.auth import LDAPBackend 
from django_python3_ldap.ldap import connection ,Connection
from django_python3_ldap import utils
import ldap3

def home(request):
    fff = LDAPBackend.authenticate(request,username='rahul',password='000')
    # dd = fff.connection(request,username='rahul',password='000')
    # print(dir(fff))
    # print("ggggg",fff)
    # dd = utils.group_lookup_args(['ou'])
    # print()
    return HttpResponse("hi")