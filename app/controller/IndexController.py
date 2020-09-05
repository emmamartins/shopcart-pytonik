from pytonik.Web import App, Version, url
from FlashBootstrap.FlashBootstrap import *

app = App()

try:
    from model.Region import Region
    from model.Users import Users
    from model.Address import Address
    from model.Products import Products
except Exception as err:
    exit(err)


def index(Session):

    if Session.has('users_id') == True:
        users_id = Session.get('users_id')
    else:
        users_id = ""
    Product = Products().isActive(12)
    data = {
        'title': 'Welcome',
        'name': 'Pytonik',
        'flash': FlashBootstrap.display(),
        'theme': 'cart1',
        'countProduct': Product[0], 
        'Product': Product[1], 
        'users_id': users_id,
        'currency': '' ,
    }

    return app.views('themes/cart1/home', data)


def product(Session):
    if Session.has('users_id') == True:
        users_id = Session.get('users_id')
    else:
        users_id = ""
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',


            'theme': 'cart1',
            'users_id': users_id
        }
        return app.views('themes/cart1/product', data)

def product_detail(Request, Session):
    app.header()
    
    if Request.method == "GET":
        product_para = Request.get('product_para')
        productDetails = Products().by_para(product_para)
        if productDetails[0] > 0:
            data = {
                'title': 'Welcome',
                'name': 'Pytonik',
                'theme': 'cart1',
                'currency': '' ,
                'products_amount_dis': productDetails[1][0]['products_amount'] if productDetails[1][0]['products_discount'] == 0 else  float(productDetails[1][0]['products_amount']) - (float(productDetails[1][0]['products_amount']) * float(productDetails[1][0]['products_discount']) / 100),
                'products_discount': productDetails[1][0]['products_discount'], 
                'products_id': productDetails[1][0]['products_id'], 
                'products_amount': productDetails[1][0]['products_amount'],
                'products_name': productDetails[1][0]['products_name'],
                'products_description': productDetails[1][0]['products_description'],
                'products_para': product_para,
                'products_pictures': productDetails[1][0]['products_pictures'],
                'countProduct': productDetails[0], 
                'users_id': Session.get('users_id')
            }

            return app.views('themes/cart1/detail-product', data)
        else:
            return app.redirect('', True)
    else:
        return app.redirect('', True)

def list_product(Session):
    data = {
        'title': 'Welcome',
        'name': 'Pytonik',
        'theme': 'cart1',
        'users_id': Session.get('users_id')
    }

    return app.views('index', data)


def cart(Request, Session):
    
    Product = []
    totalCost = []
    discountCost = []
    for lcart in Session.get("shop_to_cart"):
        lProduct = Products().by_id(lcart["product_id"])
        if lProduct[0] > 0:
            dProduct = {}
            for lPro in lProduct[1]:
                bestcost = float(lPro['products_amount']) - (float(lPro['products_amount']) * float(lPro['products_discount']) / 100)
                dProduct.update({"product_dim_quantity":lcart["product_dim_quantity"]})
                dProduct.update({"products_amount_quantity":  bestcost * float(lcart["product_dim_quantity"])})
                totalCost.append(float(lPro["products_amount"]) * float(lcart["product_dim_quantity"]))
                discountCost.append(lPro["products_discount"])
                dProduct.update({"products_amount":bestcost})
                
                for k, v in lPro.items():
                    if k != "products_amount":
                        dProduct.update({k:v})
                Product.append(dProduct)

    totalCostl = sum(totalCost)
    discountCostl = float(totalCostl) * float(sum(discountCost)) / 100
    data = {
        'title': 'Welcome',
        'name': 'Pytonik',
        'theme': 'cart1',
        'ProductCart': Product,
        'currency': Users.currency(),
        'totalCost': totalCostl,
        'discountCost': discountCostl,
        'finalCost': totalCostl - discountCostl,
        'flash': FlashBootstrap.display(),
        'users_id': Session.get('users_id')
    }

    return app.views('themes/cart1/cart', data)

def proccess_cart(Request, Session):
    Product = []
    totalCost = []
    discountCost = []
    if Session.has('users_id') != True and Session.get('users_id') == "":
        FlashBootstrap.error(description="Authentication Proccess needed, <strong><a href='{url}'>Login</a></strong> and try agin".format(url=url('/login', True)), showin='cart')    
        return app.referer('/login', True) 
    else:
        if Session.has('shop_to_cart') == True and len(Session.get("shop_to_cart")) > 0:
            
            for lcart in Session.get("shop_to_cart"):
                lProduct = Products().by_id(lcart["product_id"])
                if lProduct[0] > 0:
                    dProduct = {}
                    for lPro in lProduct[1]:
                        bestcost = float(lPro['products_amount']) - (float(lPro['products_amount']) * float(lPro['products_discount']) / 100)
                        dProduct.update({"product_dim_quantity":lcart["product_dim_quantity"]})
                        dProduct.update({"products_amount_quantity":  bestcost * float(lcart["product_dim_quantity"])})
                        totalCost.append(float(lPro["products_amount"]) * float(lcart["product_dim_quantity"]))
                        discountCost.append(lPro["products_discount"])
                        dProduct.update({"products_amount":bestcost})
                        
                        for k, v in lPro.items():
                            if k != "products_amount":
                                dProduct.update({k:v})
                        Product.append(dProduct)

            totalCostl = sum(totalCost)
            discountCostl = float(totalCostl) * float(sum(discountCost)) / 100
            data = {
                'title': 'Welcome',
                'name': 'Pytonik',
                'theme': 'cart1',
                'ProductCart': Product,
                'currency': Users.currency(),
                'totalCost': totalCostl,
                'discountCost': discountCostl,
                'finalCost': totalCostl - discountCostl,
                'flash': FlashBootstrap.display(),
                'users_id': Session.get('users_id')
            }
            
            return app.views('themes/cart1/preview-payment', data)
        else:
            FlashBootstrap.error(description="Can not proccess empty cart", showin='cart')    
            return app.referer('/cart', True) 


def login(Session):
    if Session.has('users_id') == True and Session.get('users_id') != "":
        return app.redirect('/dashboard', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',
            'theme': 'cart1',
            'flash': FlashBootstrap.display(),
            'users_id': Session.get('users_id')
        }

        return app.views('themes/cart1/login', data)


def register(Session):

    if Session.has('users_id') == True and Session.get('users_id') != "":
        return app.redirect('/dashboard', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',
            'theme': 'cart1',
            'flash': FlashBootstrap.display(),
            'countCountries': Region().countries()[0],
            'Countries': Region().countries()[1],
            'users_id': Session.get('users_id')
        }

        return app.views('themes/cart1/register', data)


def forget_password(Session):
    if Session.has('users_id') == True and Session.get('users_id') != "":
        return app.redirect('/dashboard', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',
            'theme': 'cart1',
            'flash': FlashBootstrap.display(),
            'users_id': Session.get('users_id')
        }

        return app.views('themes/cart1/forget-password', data)


def dashboard(Session):
    if Session.has('users_id') != True and Session.get('users_id') == "":
        return app.redirect('/login', True)
    else:
        user = Users().by_id(Session.get('users_id'))
        if user[0] > 0:
            data = {
                'title': 'Welcome',
                'name': 'Pytonik',
                'users_prefix': str(user[1][0]["users_prefix"])+str(" .") if user[1][0]["users_prefix"] != None or user[1][0]["users_prefix"] != "" else "",
                'users_fname': user[1][0]["users_fname"],
                'users_lname': user[1][0]["users_lname"],
                'users_email': user[1][0]["users_email"],
                'users_area_code': user[1][0]["users_area_code"],
                'users_phone': user[1][0]["users_phone"],
                'users_created_at': user[1][0]["users_created_at"],
                'theme': 'cart1',
                'users_id': Session.get('users_id')
            }
            return app.views('themes/cart1/dashboard', data)
        else:
            return app.redirect('/logout', True)


def change_password(Session):
    data = {
        'title': 'Welcome',
        'name': 'Pytonik',
        'users_id': Session.get('users_id')
    }

    return app.views('index', data)


def new_password(Session):
    data = {
        'title': 'Welcome',
        'name': 'Pytonik',
        'theme': 'cart1',
        'users_id': Session.get('users_id')
    }

    return app.views('index', data)


def profile(Session):
    data = {
        'title': 'Welcome',
        'name': 'Pytonik',
        'theme': 'cart1',
        'users_id': Session.get('users_id')
    }

    return app.views('index', data)


def edit_profile(Session):
    if Session.has('users_id') != True and Session.get('users_id') == "":
        return app.redirect('/login', True)
    else:
        user = Users().by_id(Session.get('users_id'))
        if user[0] > 0:
            data = {
                'title': 'Edit Profile',
                'name': 'Pytonik',
                'countCountries': Region().countries()[0],
                'Countries': Region().countries()[1],
                'users_fname': user[1][0]["users_fname"],
                'users_lname': user[1][0]["users_lname"],
                'users_email': user[1][0]["users_email"],
                'users_area_code': user[1][0]["users_area_code"],
                'users_phone': user[1][0]["users_phone"],
                'users_created_at': user[1][0]["users_created_at"],
                'theme': 'cart1',
                'flash': FlashBootstrap.display(),
                'users_id': Session.get('users_id')
            }
            return app.views('themes/cart1/edit-profile', data)
        else:
            return app.redirect('/logout', True)


def order_history(Session):
    if Session.has('users_id') != True and Session.get('users_id') == "":
        return app.redirect('/login', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',


            'theme': 'cart1',
            'users_id': Session.get('users_id')
        }
        return app.views('themes/cart1/order-product', data)


def refund_history(Session):
    if Session.has('users_id') != True and Session.get('users_id') == "":
        return app.redirect('/login', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',


            'theme': 'cart1',
            'users_id': Session.get('users_id')
        }

        return app.views('index', data)


def save_product(Session):
    if Session.has('users_id') != True and Session.get('users_id') == "":
        return app.redirect('/login', True)
    else:
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',


            'theme': 'cart1',
            'users_id': Session.get('users_id')
        }

        return app.views('index', data)


def address(Session, Request):
    if Session.has('users_id') != True and Session.get('users_id') == "":
        return app.redirect('/login', True)
    else:
        addressL = []
        for address in Address().by_user_id(Session.get('users_id'))[1]:
            addressD = {}
            for k, v in address.items():
                if "address_country" == k:

                    addressD.update({k: Region().by_country_id(
                        v)[1][0]["country_name"] if Region().by_country_id(
                        v)[0] > 0 else 0})
                elif "address_state" == k:

                    addressD.update({k: Region().by_state_id(
                        v)[1][0]["state_name"] if Region().by_state_id(v)[0] > 0 else 0})
                elif "address_city" == k:
                    addressD.update({k: Region().by_city_id(
                        v)[1][0]["city_name"] if Region().by_city_id(v)[0] > 0 else 0})
                else:
                    addressD.update({k: v})
            addressL.append(addressD)
        users_id = Session.get('users_id')

        if Request.get('id') !="" and Request.get('type') == "on":
            
            
            dataon = [{
                        'address_default': 1,
                }]
            dataoff = [{
                        'address_default': 0,
                }]
            if Request.get('type') == "on":
                
                Address().update_user_id(dataoff, users_id)
                if Address().update(dataon, int(Request.get('id'))) == True:
                   FlashBootstrap.success(description='Address Default Updated Successfully', showin='address')
                   return app.redirect('/address', True) 

        if Request.get('id') !="" and Request.get('type') == "delete":
            if Request.get('type') == "delete":
                if Address().delete_id_user(int(Request.get('id')), users_id) == True:
                   FlashBootstrap.success(description='Address Deleted Successfully', showin='address')
                   return app.redirect('/address', True) 
        
        data = {
            'title': 'Welcome',
            'name': 'Pytonik',
            'theme': 'cart1',
            'countAddress': Address().by_user_id(Session.get('users_id'))[0],
            'Address': addressL,
            'flash': FlashBootstrap.display(),
            'users_id': Session.get('users_id')

        }

        return app.views('themes/cart1/address', data)


def add_address(Session, Request):

    if Session.has('users_id') != True and Session.get('users_id') == "":
        return app.redirect('/login', True)
    else:
        if Request.get("country_id") != '':
            country_id = Request.get("country_id")
        else:
            country_id = 0
        if Request.get("state_id") != '':
            state_id = Request.get("state_id")
        else:
            state_id = 0
        data = {
            'title': 'Add Address',
            'name': 'Pytonik',
            'flash': FlashBootstrap.display(),
            'theme': 'cart1',
            'countCountries': Region().countries()[0],
            'Countries': Region().countries()[1],
            'countState': Region().state_by_country_id(country_id)[0],
            'State': Region().state_by_country_id(country_id)[1],
            'countCity': Region().city_by_state_id(state_id)[0],
            'City': Region().city_by_state_id(state_id)[1],
            'users_id': Session.get('users_id')
        }

        return app.views('themes/cart1/add-address', data)


def edit_address(Session, Request):
    if Session.has('users_id') != True and Session.get('users_id') == "":
        return app.redirect('/login', True)
    else:
        if Request.get("address_id") != '':
            address_id = Request.get("address_id")
            address = Address().by_id(address_id)

            if address[0] > 0:
                state_id = address[1][0]["address_state"]
                country_id = address[1][0]["address_country"]
                data = {
                    'title': 'Edit Address',
                    'name': 'Pytonik',
                    'flash': FlashBootstrap.display(),
                    'theme': 'cart1',
                    'state_id': state_id,
                    'country_id': country_id,
                    'address_id': address[1][0]["address_id"],
                    'address_name': address[1][0]["address_name"],
                    'address_phone': address[1][0]["address_phone"],
                    'address_postal_code': address[1][0]["address_postal_code"],
                    'address_phone': address[1][0]["address_phone"],
                    'address_default': address[1][0]["address_default"],
                    'countCountries': Region().countries()[0],
                    'Countries': Region().countries()[1],
                    'countState': Region().state_by_country_id(country_id)[0],
                    'State': Region().state_by_country_id(country_id)[1],
                    'countCity': Region().city_by_state_id(state_id)[0],
                    'City': Region().city_by_state_id(state_id)[1],
                    'users_id': Session.get('users_id')
                }

                return app.views('themes/cart1/edit-address', data)
            else:
                FlashBootstrap.error('Address not found')
                return app.redirect('/address', True)
        else:
            FlashBootstrap.error('Invalid Request')
            return app.redirect('/address', True)


def logout(Session):

    set_c = Session.destroy('users_id')
    # FlashBootstrap.clear()
    if set_c == True:

        return app.redirect("/login", True)
    else:
        return app.redirect("/", True)


def response(Session):
    return ""
