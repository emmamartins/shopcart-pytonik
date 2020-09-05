from pytonik.Model import Model
from pytonik.Session import Session
from pytonik.Functions.path import path

class Medias(Model, path):

    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None
        
    def __init__(self, *args, **kwargs):
        self.Session = Session()
        return None

    def list(self):
        query = self.table('medias').select().get()
        return query.rowCount, query.result
    

    def insert(self, data):
        query = self.table('medias').insert(data)
        return query
    
    def by_id(self, id):
        query = self.table('medias').where('medias_id', '=', id).insert(data)
        return query
    
    def insertGetId(self, data):
        query = self.table('medias').insertGetId(data)
        return query
    