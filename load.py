import pymongo
import csv
import sys,os
import bson
from datetime import datetime,date,time

NAMEFILE='d:\\files\listadosV.csv'
KEYSNAMES=['bankList','officeList','dateCreateList','typeList','textList']
TEXT='textList'
OFI='officeList'
BANK='bankList'
TYPE='typeList'
DATE='dateCreateList'
TIME='dateInsertList'
ID='_id'
ZEROS='0000'
ZER20=str('0') * 20

#mongoDB conection
myMongoDb=pymongo.MongoClient("mongodb://a928358:mth%402012@clustermth-shard-00-00-zf21m.mongodb.net:27017,clustermth-shard-00-01-zf21m.mongodb.net:27017,clustermth-shard-00-02-zf21m.mongodb.net:27017/test?ssl=true&replicaSet=ClusterMth-shard-0&authSource=admin").dedblists
print ('connection-> ',myMongoDb)
#variable auxiliar
mytext=list()

def insertlistMongoDB(mytext,mylineaux):
    '''insert in mongoDB dedblists/list office, get denom if denom not exits no insert in dedblist'''

    #get _id /denom. typelist

    docdenomList=myMongoDb.cdenomList.find_one({'_id':bson.ObjectId(mylineaux.get(TYPE) + ZER20)},
                                               {'_id':0,'typeList':1})
    if not (docdenomList == None):
        mylineaux[TEXT] = mytext
        myObjectId = (mylineaux.get(BANK) + mylineaux.get(OFI) + mylineaux.get(TYPE) +
                      datetime.strftime(datetime.strptime(mylineaux.get(DATE),'%y%m%d'),'%Y%m%d') + ZEROS)
        mylineaux[ID] = bson.ObjectId(myObjectId)
        mylineaux[TIME] = datetime.isoformat(datetime.today())
        mylineaux[DATE] = datetime.isoformat(datetime.strptime(mylineaux[DATE], '%y%m%d'))
        mylineaux[TYPE]=docdenomList.get(TYPE)
        myMongoDb.cloadList.insert(mylineaux)

#validamos existencia fichero
if not os.path.exists(NAMEFILE):
    raise FileExistsError('<file {}'.format(NAMEFILE))

with open(NAMEFILE,mode='r') as myFile:
    myReader=csv.DictReader(myFile,fieldnames=KEYSNAMES,delimiter=';')
    mylinefile=mylineaux=myReader.__next__()
    while(True):
        try:
            mytext.append(mylinefile.get(TEXT))
            mylinefile = myReader.__next__()
            if not ((mylineaux.get(OFI) == mylinefile.get(OFI))
                and (mylineaux.get(TYPE) == mylinefile.get(TYPE))):
# insert in mongoDB dedblists/list office
                insertlistMongoDB(mytext,mylineaux)
                mylineaux=mylinefile
                mytext=list()
        except StopIteration:
# falta StopIteration / tratar ultimo listado
            if not (os.stat(NAMEFILE).st_size == 0):
                insertlistMongoDB(mytext,mylineaux)
            break

