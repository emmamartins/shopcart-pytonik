from pytonik.Model import Model
from pytonik.Session import Session
from pytonik.Functions.path import path

class Address(Model, path):

    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None
        
    def __init__(self, *args, **kwargs):
        self.Session = Session()
        return None

    def address(self):
        query = self.table('address').select().get()
        return query.rowCount, query.result
    
    def by_id(self, id):
        query = self.table('address').where('address_id', "=", id).select().get()
        return query.rowCount, query.result

    def by_user_id(self, users_id):
        query = self.table('address').where('users_id', "=", users_id).select().get()
        return query.rowCount, query.result

    def delete_id(self, id):
        query = self.table('address').where('address_id', "=", id).delete(data)
        return query
    
    def delete_id_user(self, address_id, users_id):
        query = self.table('address').where('address_id', "=", address_id).where('users_id', "=", users_id).delete()
        return query

    def insert(self, data):
        query = self.table('address').insert(data)
        return query
    
    def insertGetId(self, data, id):
        query = self.table('address').insertGetId(data)
        return query
    
    def update(self, data, id):
        query = self.table('address').where('address_id', "=", id).update(data)
        return query
    
    
    def update_user_id(self, data, users_id):
        query = self.table('address').where('users_id', "=", users_id).update(data)
        return query

    def update_id_userid(self, data, address_id, users_id):
        query = self.table('address').where('address_id', "=", address_id).where('users_id', "=", users_id).update(data)
        return query