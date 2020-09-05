from pytonik.Model import Model
from pytonik.Session import Session
from pytonik.Functions.path import path

class Products(Model, path):

    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None
        
    def __init__(self, *args, **kwargs):
        self.Session = Session()
        return None

    def list(self):
        query = self.table('products').select().get()
        return query.rowCount, query.result
    
    
    def by_id(self, products_id):
        query = self.table('products').where('products_id','=', products_id).select().get()
        return query.rowCount, query.result


    def by_para(self, products_para):
        query = self.table('products').where('products_para','=', products_para).select().get()
        return query.rowCount, query.result

    def isActive(self, limit):
        query = self.table('products').where('products_is_active','=', 1).limit(limit).select().get()
        return query.rowCount, query.result


    def insert(self, data):
        query = self.table('products').insert(data)
        return query
    
    def insertGetId(self, data):
        query = self.table('products').insertGetId(data)
        return query
    
    def update(self, data, id):
        query = self.table('users').where('users_id', "=", id).update(data)
        return query
    
    def by_product_id_wishlist(self, products_id):
        query = self.table('wishlist').where('products_id','=', products_id).select().get()
        return query.rowCount, query.result

    def insert_wishlist(self, data):
        query = self.table('wishlist').insert(data)
        return query