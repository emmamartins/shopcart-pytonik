from pytonik.Model import Model
from pytonik.Session import Session
from pytonik.Functions.path import path

class Region(Model, path):

    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None
        
    def __init__(self, *args, **kwargs):
        self.Session = Session()
        return None

    def countries(self):
        query = self.table('countries').select().get()
        return query.rowCount, query.result
    
    def by_city_id(self, city_id):
        city_id = city_id if city_id != None  and city_id != "" else 0
        query = self.table('cities').where('city_id', city_id).select().get()
        return query.rowCount, query.result

    def by_country_id(self, country_id):
        country_id = country_id if country_id != None  and country_id != "" else 0
        query = self.table('countries').where('country_id', country_id).select().get()
        return query.rowCount, query.result
    

    def by_state_id(self, state_id):
        state_id = state_id if state_id != None  and state_id != "" else 0
        query = self.table('states').where('state_id', state_id).select().get()
        return query.rowCount, query.result
    

    def state_by_country_id(self, country_id):
        country_id = country_id if country_id != None  and country_id != "" else 0
        query = self.table('states').where('country_id', country_id).select().get()
        return query.rowCount, query.result
    
    
    def city_by_state_id(self, state_id=0):

        state_id = state_id if state_id != None and state_id != "" else 0
        query = self.table('cities').where('state_id','=', state_id).select().get()
        return query.rowCount, query.result
