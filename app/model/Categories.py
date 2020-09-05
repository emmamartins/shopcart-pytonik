from pytonik.Model import Model
from pytonik.Session import Session
from pytonik.Functions.path import path

class Categories(Model, path):

    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None
        
    def __init__(self, *args, **kwargs):
        self.Session = Session()
        return None

    def list(self):
        query = self.table('categories').select().get()
        return query.rowCount, query.result
        
    def parent(self):
        query = self.table('categories').where('categories_parent', '=', 0).select().get()
        return query.rowCount, query.result
    

    def by_parent(self, id):
        query = self.table('categories').where('categories_parent', '=', id).select().get()
        return query.rowCount, query.result
    