from pytonik.Model import Model
from pytonik.Session import Session
from pytonik.Functions.path import path

class Users(Model, path):

    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None
        
    def __init__(self, *args, **kwargs):
        self.Session = Session()
        return None

    def by_email(self, email):
        query = self.table('users').where('users_email', email).select().get()
        return query.rowCount, query.result
    
    def by_id(self, id):
        query = self.table('users').where('users_id', id).select().get()
        return query.rowCount, query.result
    
    def get_by_id(self, id, col):
        query = self.table('users').where('users_id', id).select().get()
        return query.result[0]["col"] if query.rowCount > 0 else ""
    
    def insert(self, data):
        query = self.table('users').insert(data)
        return query
    
    def insertGetId(self, data, id):
        query = self.table('users').insertGetId(data)
        return query
    
    def update(self, data, id):
        query = self.table('users').where('users_id', "=", id).update(data)
        return query

    @staticmethod
    def currency(currency='NGN'):
        c = {
            'NGN': str('&#8358;')
        }
        return c.get(currency, '₦')