"""CRUD
=======
"""

class CRUD(object):
    """Mix-in class to implement CRUD(L) database Verbs."""
    def read(self, id):
        """Read a document with `id` from the database."""
        return self.db.read(self.collection, id)

    def create(self, doc):
        """Create a new `doc` in a database collection."""
        return self.db.create(self.collection, doc)

    def update(self, doc):
        """Update an existing `doc` in a database collection."""
        return self.db.update(self.collection, doc)

    def delete(self, id):
        """Delete a document with `id` from a database collection."""
        return self.db.delete(self.collection, id)

    def list(self, **spec):
        """Read **all** documents matching `spec` from the database."""
        return self.db.list(self.collection, spec)

    #Other Database Operations
    def drop_collection(self):
        """Drop *all* documents in a collection."""
        return self.db.drop_collection(self.collection)

    def nuke(self, **spec):
        """Remove **all** documents matching `spec` from the database."""
        return self.db.nuke(self.collection, spec)

    def shovel(self, docs, *spec):
        """Add a **collection** of documents into the database.
        Return the result of listing the collection as per `spec`."""
        [self.update(doc) for doc in docs]#TODO - What about errors or unexpected results?
        return self.LIST(*spec)
