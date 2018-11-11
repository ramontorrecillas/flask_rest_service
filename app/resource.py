from flask_restful import reqparse,fields,inputs,marshal_with
from flask_restful import request,Api,Resource
from flask import Flask,make_response
from flask_pymongo import PyMongo
from datetime import datetime
from app import myApp,myMongo,myApi
from bson import ObjectId

BANK_DEFAULT='0182'
HELP_OFFICE='<field office required>'
HELP_LIST='<field List (type/subtype) required or no_exits in database'
HELP_DATE='<field date (Fmt-AAAAmmdd) required'
XML='application/xml'
JSON='application/json'
TEXT='textList'
RESO='resource'
DATA='data'
ZEROS='0000'
ZER20=str('0') * 20

class MyApiRest(Resource):
    '''class MyApiRest resource and fields output'''
    resource_fields = {
        'result': fields.Nested({'code':fields.Integer,
                            'info':fields.String}),
        'data': fields.Nested({'mimetype': fields.String,
                            'bankList': fields.String,
                            'officeList': fields.String,
                            'typeList': fields.String,
                            'denomList': fields.String,
                            'dateCreateList': fields.String,
                            'textList':fields.List(fields.String),
                            'numLinesList':fields.Integer,
                            'dateInsertList': fields.String,
                            'urlResource': fields.Url(absolute=True)}),}

    def __init__(self,*args,**kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('bank', default=BANK_DEFAULT)
        self.parser.add_argument('office', help=HELP_OFFICE, required=True)
        self.parser.add_argument('type', help=HELP_LIST, required=True,type=self._validationType)
        self.parser.add_argument('date', help=HELP_DATE, required=True,
                            type=lambda value: datetime.strftime(datetime.strptime(value,'%Y%m%d'),'%Y%m%d'))
        super(MyApiRest,self).__init__()

    def _validationType(self,type):
        '''rules validation type access to MongoDb, validate type List and get denom'''
        self.myquery = myMongo.db.cdenomList.find_one({'_id': ObjectId(type + ZER20)},
                                                      {'_id': 0, 'denomList': 1})
        self.parser.add_argument('denom', default=self.myquery.get('denomList'))
        return type

    @marshal_with(resource_fields)
    def get(self):
        ''' Get access mongoDb and retreave list'''
        self.myparse=self.parser.parse_args()
        myId = (self.myparse.get('bank') + self.myparse.get('office') +
                self.myparse.get('type') + self.myparse.get('date') + ZEROS)
        myresult = myMongo.db.cloadList.find_one({'_id': ObjectId(myId)})

        if not (myresult):
            return {'result': {'code': 204, 'info': 'not exits information type/date'}, 'data': {}}

        myresult['denomList'] = self.myparse.get('denom')
        myresult['mimetype'] = request.headers.get('Accept', 'application/json')
        myresult['numLinesList'] = len(myresult['textList'])
        myresult = {'data': myresult, 'result': {'code': 200, 'info': 'OK'}}
        return (myresult)

myApi.add_resource(MyApiRest,'/api/report')

