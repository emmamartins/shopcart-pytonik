from pytonik.Model import Model
from pytonik.Session import Session
from pytonik.Functions.path import path

class Condition(Model, path):

    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None
        
    def __init__(self, *args, **kwargs):
        self.Session = Session()
        return None

    def is_active(self):
        query = self.table('condition').where('condition_is_active', 1).select().get()
        return query.rowCount, query.result
    