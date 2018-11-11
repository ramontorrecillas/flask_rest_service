from flask_restful import request,Api,Resource
from flask import Flask,make_response
from flask_pymongo import PyMongo
from simplexml import dumps
from os import getenv

#constantes
DATA='data'
TEXT='textList'
XML='application/xml'

#configuration application FLASK
myApp=Flask('__name__')

#Configuration MongoDB_ATLAS
MONGO_DEFAULT="mongodb://127.0.0.1:27017/dedblists"
MONGO_ATLAS="mongodb+srv://user_name:password@name_cluster.mongodb.net/dedblists"

myApp.config['MONGO_URI']=getenv('MONGO_URI',MONGO_DEFAULT)
myApp.config['MONGO_DBNAME']='dedblists'
myMongo=PyMongo(myApp)

#xml representation FLASK rest service
myApi=Api(myApp)

@myApi.representation(XML)
def xml(data, code, headers):
    data[DATA][TEXT]={'line-'+str(num):item for num,item in enumerate(data[DATA][TEXT])}
    myResponse = make_response(dumps({'response':data}), code)
    myResponse.headers.extend(headers)
    return myResponse

import app.resource
