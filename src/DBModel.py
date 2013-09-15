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

    def create(self, dbname, collection_names):
        '''Create collection(s) in a database named 'dbname'
           @dbname          : a database name string
           @collection_names: a list of collection names
        '''

        for collection in collection_names:
            self.client[dbname].createCollection[collection]

    def insert(self, dbname, collection_name, document):
        '''Insert a document (a row in SQL) into a mongodb collection
           mongodb creates the collection IMPLICITLY on the first insert
           operation.
           @dbname         : a database name string
           @collection_name: a string of collection name
           @document       : a python dictionary containing things to be inserted
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

        print 'Records in ', collection_name, ':'
        for bson_obj in cursor:
            print bson_obj

    def update(): pass
    def delete(): pass


def main():

    # create mongodb database object
    db = DBModel.factory('MongoDB')

    # connect to mongodb database server
    db.connect('localhost', 27017)

    # create collections
    db.create('local', ['todo', 'tolearn'])

    # insert documents into collection 'tmp' in database 'local'
    db.insert('local', 'todo', {'item': "look for jobs", \
                                'year': False,           \
                                'season': False,         \
                                'month':  False,         \
                                'week': False,           \
                                'day': True,             \
                                'prio': -1,              \
                                'date': datetime.datetime.utcnow()})

    db.insert('local', 'todo', {'item': "study triangulation algorithm", \
                                'year': False,           \
                                'season': False,         \
                                'month':  False,         \
                                'week': False,           \
                                'day': True,             \
                                'prio': -1,              \
                                'date': datetime.datetime.utcnow()})

    db.insert('local', 'tolearn', {'item': "GNU autotools",\
                                    'year': False,           \
                                    'season': False,         \
                                    'month':  False,         \
                                    'week': False,           \
                                    'day': True,             \
                                    'prio': -1,              \
                                    'date': datetime.datetime.utcnow()})

    # query the documents stored in collection 'tmp' in database 'local'
    db.query('local', 'todo')
    db.query('local', 'tolearn')

    # drop collection 'tmp' in database 'local'
    db.drop('local', 'todo')
    db.drop('local', 'tolearn')

    # close databse connection
    db.close()

if __name__ == '__main__':
    main()
