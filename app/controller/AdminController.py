from pytonik.Web import App, Version
from FlashBootstrap.FlashBootstrap import *
app = App()

try:
    import Users
    from model.Region import Region
    from model.Address import Address
    from model.Products import Products
    from model.Categories import Categories
    from model.Condition import Condition
except Exception as err:
    app.header()
    print(err)


def index(Session):
    if Session.has('admin_id') != True and Session.get('admin_id') == "":
        return app.redirect('/admin/login', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',
            'version': Version().VERSION_TEXT,
            'reversion': Version().VERSION_TEXT[0:6],
        }

        return app.views('admin/dashboard', data)

def login(Session):
    if Session.has('admin_id') == True and Session.get('admin_id') != "":
        return app.redirect('/admin', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',
            'flash': FlashBootstrap.display(),
            'version': Version().VERSION_TEXT,
            'reversion': Version().VERSION_TEXT[0:6],
        }

        return app.views('admin/login', data)



def list_users(Session):
    if Session.has('admin_id') != True and Session.get('admin_id') == "":
        return app.redirect('/admin/login', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',
            'flash': FlashBootstrap.display(),
            'version': Version().VERSION_TEXT,
            'reversion': Version().VERSION_TEXT[0:6],
        }

        return app.views('admin/list-users', data)

def add_users(Session):
    if Session.has('admin_id') != True and Session.get('admin_id') == "":
        return app.redirect('/admin/login', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',
            'flash': FlashBootstrap.display(),
            'version': Version().VERSION_TEXT,
            'reversion': Version().VERSION_TEXT[0:6],
        }

        return app.views('admin/list-users', data)


def edit_users(Session):
    if Session.has('admin_id') != True and Session.get('admin_id') == "":
        return app.redirect('/admin/login', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',
            'flash': FlashBootstrap.display(),
            'version': Version().VERSION_TEXT,
            'reversion': Version().VERSION_TEXT[0:6],
        }

        return app.views('admin/list-users', data)

def list_products(Session):
    if Session.has('admin_id') != True and Session.get('admin_id') == "":
        return app.redirect('/admin/login', True)
    else:
        Product = Products().list()
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',
            'Product': Product[1],
            'flash': FlashBootstrap.display(),
            'version': Version().VERSION_TEXT,
            'reversion': Version().VERSION_TEXT[0:6],
        }

        return app.views('admin/list-product', data)



def add_products(Session):
    app.header()
    if Session.has('admin_id') != True and Session.get('admin_id') == "":
        return app.redirect('/admin/login', True)
    else:
        lcatL = []
        for i, lcat in enumerate(Categories().parent()[1]):
            lcatD = {}
            
            if Categories().by_parent(lcat["categories_id"])[0] > 0: 
                
                for k, v in lcat.items():
                    lcatD.update({k:v})
    
                lcatLX = []
                for lcatS in Categories().by_parent(lcat["categories_id"])[1]: 
                    lcatDx = dict({'count':1})
                    lcatDx.update(dict(lcatS)) 
                    lcatLX.append(lcatDx)
                lcatD.update({'subCategories':lcatLX})
                
            else:
                for k, v in lcat.items():
                    lcatD.update({k:v})
                lcatD.update({'subCategories':[{'count':0}]})
            lcatL.append(lcatD)    
    
        Cat = [dict(Categories=lcatL)]
        data = {
            'title': 'Add Product',
            'name': '',
            'admin_id': Session.get('admin_id'),
            'countCondition': Condition().is_active()[0],
            'Condition': Condition().is_active()[1],
            'flash': FlashBootstrap.display(),
            'countCat': Categories().list()[0],
            'Cat': Cat,
            
        }

        
        return app.views('admin/add-product', data)