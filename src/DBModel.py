#!/usr/bin/env python

#========================================================
#   This file contains the database model behind pda tool
#========================================================
from pymongo import MongoClient
import datetime

class DBModel(object):
    @staticmethod
    def factory(type):
        # simple factory method for creating database objects
        if type == "MongoDB": return MongoDB()
        assert 0, "Bad database creation: " + type

class MongoDB(DBModel):

    def connect(self, host, port):
        '''Connect to MongoDB database server through the pymongo driver
        '''

        self.client = MongoClient(host, port)
        # for name in self.client.database_names():
        #     db = self.client[name]
        #     print 'database: "' + name + '" with collections:', db.collection_names()

    def close(self):
        '''Close database connection
        '''

        self.client.close()

    def insert(self, dbname, collection_name, document):
        '''Insert a document (a row in SQL) into a mongodb collection
           mongodb creates the collection IMPLICITLY on the first insert
           operation.
        '''

        self.client[dbname][collection_name].insert(document)

    def drop(self, dbname, collection_name):
        '''Drop a collection in a database
        '''

        self.client[dbname][collection_name].drop()

    def query(self, dbname, collection_name):
        '''Print all the documents in a collection
        '''

        cursor = self.client[dbname][collection_name].find() 

        for bson_obj in cursor:
            print bson_obj

    def update(): pass
    def delete(): pass


def main():

    # create a document for insertion
    doc1 = {
            'author': 'henry', 
            'text'  : 'my first collection!',
            'date'  : datetime.datetime.utcnow()
           }

    doc2 = {
            'author': 'flora', 
            'text'  : 'her first collection!',
            'date'  : datetime.datetime.utcnow()
           }

    # create mongodb database object
    db = DBModel.factory('MongoDB')

    # connect to mongodb database server
    db.connect('localhost', 27017)

    # insert documents into collection 'tmp' in database 'local'
    db.insert('local', 'tmp', doc1)
    db.insert('local', 'tmp', doc2)

    # query the documents stored in collection 'tmp' in database 'local'
    db.query('local', 'tmp')

    # drop collection 'tmp' in database 'local'
    db.drop('local', 'tmp')

    # close databse connection
    db.close()

if __name__ == '__main__':
    main()
