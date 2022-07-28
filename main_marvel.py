#!/usr/bin/python3

## IMPORTING LIBRARIES ## 

import json
import requests
from pprint import pprint
import psycopg2
import os

## CONNECTION TO THE DATABASE CREATED LOCALLY ON THE COMPUTER ##

DB_Connect = psycopg2.connect(
    host = 'localhost',
    user = 'postgres',
    password = 'qtjNRnZed2!',
    database = 'marvel_db',
    port = '5432'
)

DB_Connect.autocommit = True

## CREATION OF THE TABLE IN THE DATABASE ##

def CreateTable():
    cursor = DB_Connect.cursor()
    query = 'CREATE TABLE characters(name varchar(30), description varchar(255), available_comics int, available_series int)'
    try:
        cursor.execute(query)
    except:
        print('TABLA EXISTENTE')

    cursor.close()

CreateTable()

list = []

## DATA FOR THE CONNECTION TO THE API, HASH AND KEYS ARE PROVIDED FOR ACCESSING ##

ts = '1'
private_key = '203737e955bec631506c894328da021dfd460119'
public_key = '99e5587b55d9dced8704ac12a32e44a7'
hash_md5 = '168a1fc337165c4babd7e5d4800812a9'

url = f'https://gateway.marvel.com:443/v1/public/characters?ts={ts}&apikey={public_key}&hash={hash_md5}'

## WE CREATE THE DICTIONARY FROM THE DATA OBTAINED THROUGH THE API ##
 
get = requests.get(url)

if get.status_code == 200:
    get_json  = json.loads(get.text)

    for x in get_json['data']['results']:

        Name = x['name']
        Description = x['description']
        Comics = x['comics']['available']
        Series = x['series']['available']

        dic = {'Name':Name, 'Description':Description, 'Comics':Comics, 'Series':Series}
        list.append(dic)

## FUNCTION THAT INSERTS THE LIST THAT HAS BEEN CREATED FROM THE API ##

def dataInsert():
    cursor = DB_Connect.cursor()
    columns = list.keys()
    for i in list.values():
        query = """INSERT INTO characters(name, description, available_comics, available_series) VALUES({});""".format(i)
    cursor.execute(query)
    cursor.close()
dataInsert()