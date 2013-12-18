"""MongoDB
==========
"""
from pymongo import MongoClient
from werkzeug.exceptions import NotFound


class MongoDB(object):
    """Interface to MongoDB. This implements a CRUD interface
    (Create, Read, Update, Delete) to MongoDB.
    """
    DB_VERSION = '0.0'
    """Database Version..."""

    def __init__(self, host, port):
        """Create a connection to the MongoDB database.
        """
        self.db = MongoClient(host, port)

    #CRUD Database operations
    #------------------------
    def create(self, collection, doc):
        """**Create** a new `doc` in a MongoDB `collection`."""
        doc.update(version=self.DB_VERSION)
        return collection.insert(doc)

    def read(self, collection, id):
        """**Read** and return a document with `id` from a MongoDB `collection`."""
        data = collection.find_one(id if isinstance(id, dict) else {'_id':id})
        if not data:
            raise NotFound
        return data

    def update(self, collection, doc):
        """**Update** an existing `doc` in a MongoDB `collection`."""
        doc.update(version=self.DB_VERSION)
        return collection.save(doc)

    def delete(self, collection, id):
        """**Delete** a document with `id` from a MongoDB `collection`."""
        return collection.remove(id)

    #Other Database operations
    #-------------------------
    def drop_collection(self, collection):
        """Delete **All** documents in collection."""
        return collection.drop()

    def list(self, collection, spec):
        """**List** and return all doucments matching `spec` from a MongoDB `collection`."""
        return collection.find(spec)

    def nuke(self, collection, spec):
        """Remove **all** documents matching `spec` from a MongoDB `collection`."""
        return collection.remove(spec)


class MIM(MongoDB):
    """A Mongo In-Memory database, to mock a real MongoDB connection -
    used for testing to avoid a dependency on an external database service.

    .. inheritance-diagram:: MIM
    """
    def __init__(self, host):
        """Create the Mongo-in-Memory Datastore.
        Note: import from ming here, so as to avoid a dependency on ming
        in the production environment.
        """
        from ming import create_datastore
        self.db = create_datastore('mim://localhost:27017/').db

    def drop_collection(self, collection):
        """Don't delete.
        TODO - Why doesn't this work in MIM?????.
        """
        return #collection.drop()


class DBApplication(object):
    """This adds a MongoDB Databse connection to the Application.
    (via the :class:`.MongoDB` class).
    """
    Database = MongoDB
    """:class:`.MongoDB` is the service provider class for
    connecting to the database.
    """
    def __init__(self, host):
        self.db = self.new_database(host)

    def new_database(self, host):
        """Return the Database, opening a connection.
        This is usally the app's `Database` class,
        but `host="MIM"` will override this and return a
        Mongo-In-Memory connection instead.
        """
        return MIM(self) if host=='MIM' else self.Database(self)

    @property
    def database(self):
        """Return the Application's MongoDB Database."""
        return self.db.db[self.config.DB_NAME]


