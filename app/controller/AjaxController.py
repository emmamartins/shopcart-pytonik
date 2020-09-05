from pytonik.Web import App, Version, url
from pytonik.Functions import validation, now
from pytonik.Flash import Flash
from FlashBootstrap.FlashBootstrap import *
from pytonik.Functions.rand import rand as random
from pytonik.Core import File, Helpers
app = App()
validate = validation.validation()
now = now.now()
try:
    import Users
    from model.Region import Region
    from model.Address import Address
    from model.Products import Products
    from model.Medias import Medias
    from model.Cart import Cart
except Exception as err:
    app.header()
    print(err)

users = Users.Users()

dimension = {58:53, 250:250, 480:480, 520:480}
list_ext = ['PNG', 'png', 'jpg', 'JPG', 'jpeg']
upload_dir = Helpers.mvc_dir('/public/uploads/')
upload_dir_resize =  Helpers.mvc_dir('/public/uploads/resize')

def login_admin(Request, Session):
    msg = 0
    jquery = Request.post('jquery')
    if Request.method == "POST":
        username = Request.post('username')
        password = Request.post('password')
        if username == "" and password == "":
            if jquery == "yes":
                msg = 6
            else:
                FlashBootstrap.error("Enter Username and Password")
                return app.redirect('/admin/login', True)
        elif password == "":
            if jquery == "yes":
                msg = 4
            else:
                FlashBootstrap.error("Enter Password")
                return app.redirect('/admin/login', True)

        elif validate.count(password) < 4:
            if jquery == "yes":
                msg = 4
            else:
                FlashBootstrap.warning("Password Should be greater than 4")
                return app.redirect('/admin/login', True)
        else:

            if users.by_email(username)[0] > 0:
                fetch = users.by_email(username)[1][0]
                if fetch["users_password"] == password:
                    Session.set('admin_id', fetch["users_id"])
                    # update Login activities
                    if jquery == "yes":
                        msg = 1
                    else:

                        FlashBootstrap.clear()
                        return app.redirect('/admin', True)

                else:
                    if jquery == "yes":
                        msg = 2
                    else:
                        FlashBootstrap.error("Incorrect Password")
                        return app.redirect('/admin/login', True)
            else:
                if jquery == "yes":
                    msg = 3
                else:
                    FlashBootstrap.warning(
                        "No Account link to this Username")
                    return app.redirect('/admin/login', True)
    else:
        if jquery == "yes":
            msg = 0
        else:
            FlashBootstrap.warning(
                description="Invalid Request", showin="admin/login")
            return app.redirect('/admin/login', True)

    return app.XHreponse(msg)


def add_products(Session, Request):
    msg = 0
    
    jquery = Request.post('jquery')
    
    if Request.method == "POST":
        owner_id = Request.post("owner_id")
        products_name = Request.post("products_name")
        products_description = Request.post("products_description")
        products_condition = Request.post("products_condition")
        products_amount = Request.post("products_amount") if Request.post("products_amount") !="" else 0
        products_category = Request.post("products_category") if Request.post("products_category") !="" else 0
        products_quantity = Request.post("products_quantity") if Request.post("products_quantity") !="" else 0
        products_discount = Request.post("products_discount") if Request.post("products_discount") !="" else 0
        products_size = Request.post("products_size")
        products_color = Request.post("products_color")
        products_pictures = Request.file("products_pictures[]")
        products_shipper = Request.post("products_shipper")
        products_created_at = now.datetime()
        users_admin_id = Request.post("users_admin_id") if Request.post("users_admin_id") !="" else 0 
        products_para = str(products_name).replace(' ', '-')+"-"+str(now.unix())

        if products_name == "" and products_description == "" and products_category == "" :
            if jquery == "yes":
                msg = 16
            else:
                FlashBootstrap.error("Fill out all required field")
                return app.redirect('/admin/add/products', True)
        elif products_category == "":

            if jquery == "yes":
                msg = 15
            else:
                FlashBootstrap.error("Choose Product Categories")
                return app.redirect('/admin/add/products', True)
        elif products_name == "":

            if jquery == "yes":
                msg = 15
            else:
                FlashBootstrap.error("Enter Product Name ")
                return app.redirect('/admin/add/products', True)
        elif products_description == "":

            if jquery == "yes":
                msg = 15
            else:
                FlashBootstrap.error("Enter Product Description")
                return app.redirect('/admin/add/products', True)
        else:
            file_new_name = []
            media_id = 0
            try:
                pict = products_pictures
                if pict.filename  !="":

                    if pict.filename != "" and pict.filename != None:
                        
                        rename = random().number(10)
                        file_name = pict.filename
                        ext = File.ext(file_name)

                        if ext not in list_ext :
                                FlashBootstrap.error("Invalid Image Formate")
                                return app.redirect('/admin/add/products', True)
                        else:
                            image = File.Image(upload_dir_resize, pict)
                            for w, h in dimension.items():
                                response = image.resize(w, h, rename)
                                if response == True:
                                            #file.upload(pict, upload_dir, rename)
                                    image.upload(rename, upload_dir)
                            file_new_name.append(str(rename)+str(file_name))
                    if len(file_new_name) > 0:
                       
                        data = [{

                                    'medias_name': ",".join(file_new_name),
                                    'medias_type': "img",
                                    'owner_id': owner_id,
                                    'medias_publish': 'yes',
                                    'medias_created_at': now.datetime(),
                            }]
                            
                        media_id = Medias().insertGetId(data)
                    else:
                        media_id = 0
                
            except Exception as err:
                
                try:
                    
                    for i, pict in enumerate(products_pictures):
                        
                        
                        if pict.filename  !="":

                            if pict.filename != "" and pict.filename != None:

                                rename = random().number(10)
                                file_name = pict.filename
                                ext = File.ext(file_name)

                                if ext not in list_ext :
                                    FlashBootstrap.error("Invalid Image Formate")
                                    return app.redirect('/admin/add/products', True)
                                else:
                                    image = File.Image(upload_dir_resize, pict)
                                    for w, h in dimension.items():
                                        response = image.resize(w, h, rename)
                                        if response == True:
                                            #file.upload(pict, upload_dir, rename)
                                            image.upload(rename, upload_dir)
                                        file_new_name.append(str(rename)+str(file_name))


                    if len(file_new_name) > 0:
                        data = [{

                                'medias_name': ",".join(file_new_name),
                                'medias_type': "img",
                                'owner_id': owner_id,
                                'medias_publish': 'yes',
                                'medias_created_at': now.datetime(),
                        }]
                        media_id = Medias().insertGetId(data)
                    else:
                        media_id = 0
                except Exception as err:
                    media_id = 0
        
            
            data = [{

                'products_para': products_para,
                'products_name': products_name,
                'products_description': products_description,
                'products_amount': products_amount,
                'products_category': ','.join(products_category),
                'products_quantity': products_quantity,
                'products_discount': products_discount,
                'products_size': ','.join(products_size),
                'products_color': ','.join(products_color),
                'products_shipper': products_shipper,
                'products_pictures': media_id,
                'products_created_at': products_created_at,
                'owner_id': users_admin_id

            }]
            
            if Products().insert(data) == True:

                # send message to registered user
                if jquery == "yes":
                    msg = 1
                else:
                    FlashBootstrap.success(
                        description="Product Added Successfully", title="", showin='admin/products')
                    return app.redirect('admin/products', True)
            else:
                if jquery == "yes":
                    msg = 2
                else:
                    FlashBootstrap.error("Unable To Proccess this action, Try again later")
                    return app.redirect('/admin/add/products', True)

    return app.XHreponse(msg)


# Home / Users AJAX

def login(Request, Session):
    msg = 0
    if Request.method == "POST":
        email = Request.post('email')
        password = Request.post('password')
        jquery = Request.post('jquery')
        if email == "" and password == "":
            if jquery == "yes":
                msg = 6
            else:

                FlashBootstrap.error("Enter Email Address and Password")
                return app.redirect('/login', True)

        elif validate.email(email) != True:
            if jquery == "yes":
                msg = 5
            else:
                FlashBootstrap.error("Invalid Email Address")
                return app.redirect('/login', True)

        elif password == "":
            if jquery == "yes":
                msg = 4
            else:
                FlashBootstrap.error("Enter Password")
                return app.redirect('/login', True)

        elif validate.count(password) < 4:
            if jquery == "yes":
                msg = 4
            else:
                FlashBootstrap.warning("Password Should be greater than 4")
                return app.redirect('/login', True)
        else:

            if users.by_email(email)[0] > 0:
                fetch = users.by_email(email)[1][0]
                if fetch["users_password"] == password:
                    Session.set('users_id', fetch["users_id"])
                    # update Login activities
                    if jquery == "yes":
                        msg = 1
                    else:
                        FlashBootstrap.clear()
                        return app.redirect('/dashboard', True)

                else:
                    if jquery == "yes":
                        msg = 2
                    else:
                        FlashBootstrap.error("Incorrect Password")
                        return app.redirect('/login', True)
            else:
                if jquery == "yes":
                    msg = 3
                else:
                    FlashBootstrap.warning(
                        "No Account link to this Email Address")
                    return app.redirect('/login', True)
    else:
        if jquery == "yes":
            msg = 0
        else:
            FlashBootstrap.warning("Invalid Request")
            return app.redirect('/login', True)

    return app.XHreponse(msg)


def register(Request, Session):
    msg = 0
    jquery = Request.post('jquery')
    if Request.method == "POST":
        email = Request.post('email')
        password = Request.post('password')
        repassword = Request.post('repassword')
        fname = Request.post('fname')
        lname = Request.post('lname')
        phone = Request.post('phone')
        area_code = Request.post('area_code')
        if fname == "" and lname == "" and email == "" and password == "" and email == "" and password == "":
            if jquery == "yes":
                msg = 16
            else:
                FlashBootstrap.error("Fill out all required field")
                return app.redirect('/register', True)
        elif fname == "":

            if jquery == "yes":
                msg = 15
            else:
                FlashBootstrap.error("Enter First Name")
                return app.redirect('/register', True)
        elif lname == "":

            if jquery == "yes":
                msg = 14
            else:
                FlashBootstrap.error("Enter Last Name")
                return app.redirect('/register', True)

        elif email == "":

            if jquery == "yes":
                msg = 13
            else:
                FlashBootstrap.error("Enter Email Address")
                return app.redirect('/register', True)

        elif validate.email(email) != True:

            if jquery == "yes":
                msg = 12
            else:
                FlashBootstrap.warning("Invalid Email Address")
                return app.redirect('/register', True)
        elif area_code == "":
            if jquery == "yes":
                msg = 11
            else:
                FlashBootstrap.error("Choose Country Code")
                return app.redirect('/register', True)

        elif phone == "":
            if jquery == "yes":
                msg = 10
            else:
                FlashBootstrap.error("Enter Phone Number")
                return app.redirect('/register', True)

        elif validate.phone(str(area_code)+str(phone)) != True:
            if jquery == "yes":
                msg = 9
            else:
                FlashBootstrap.error("Invalid Phone Number")
                return app.redirect('/register', True)

        elif password == "":
            if jquery == "yes":
                msg = 8
            else:
                FlashBootstrap.error("Enter Password")
                return app.redirect('/register', True)

        elif validate.count(password) < 4:
            if jquery == "yes":
                msg = 7
            else:
                FlashBootstrap.warning("Password Should be greater than 4")
                return app.redirect('/register', True)
        elif repassword == "":
            if jquery == "yes":
                msg = 6
            else:
                FlashBootstrap.error("Enter Repeat Password for confirmation")
                return app.redirect('/register', True)
        elif repassword != password:
            if jquery == "yes":
                msg = 5
            else:
                FlashBootstrap.warning(
                    "Repeat Password does not match main Password")
                return app.redirect('/register', True)
        else:

            data = [{
                'users_fname': fname,
                'users_lname': lname,
                'users_email': email,
                'users_area_code': area_code,
                'users_phone': phone,
                'users_password': password,
                'users_created_at': now.datetime(),
            }]

            if users.by_email(email)[0] < 1:
                if users.insert(data) == True:
                    # send message to registered user
                    if jquery == "yes":
                        msg = 1
                    else:
                        FlashBootstrap.success(
                            description="Account Registration is successful,  Login to access your account", title="", showin='login')
                        return app.redirect('/login', True)
                else:
                    if jquery == "yes":
                        msg = 2
                    else:
                        FlashBootstrap.error(
                            "Unable To Proccess this action, Try again later")
                        return app.redirect('/register', True)

            else:
                if jquery == "yes":
                    msg = 3
                else:
                    FlashBootstrap.warning(
                        "Account with Email Address Already Exist")
                    return app.redirect('/register', True)
    else:
        if jquery == "yes":
            msg = 0
        else:
            FlashBootstrap.warning("Invalid Request")
            return app.redirect('/register', True)

    return app.XHreponse(msg)


def update_profile(Request, Session):
    msg = 0
    jquery = Request.post('jquery')
    if Request.method == "POST":
        email = Request.post('email')
        fname = Request.post('fname')
        lname = Request.post('lname')
        phone = Request.post('phone')
        jquery = Request.post('jquery')
        users_id = Request.post('users_id')
        if fname == "" and lname == "" and email == "" and area_code == "" and phone == "":
            if jquery == "yes":
                msg = 12
            else:
                FlashBootstrap.error("Fill out all required field")
                return app.redirect('/edit/profile', True)
        elif fname == "":

            if jquery == "yes":
                msg = 11
            else:
                FlashBootstrap.error("Enter First Name")
                return app.redirect('/edit/profile', True)
        elif lname == "":

            if jquery == "yes":
                msg = 10
            else:
                FlashBootstrap.error("Enter Last Name")
                return app.redirect('/edit/profile', True)

        elif email == "":

            if jquery == "yes":
                msg = 9
            else:
                FlashBootstrap.error("Enter Email Address")
                return app.redirect('/edit/profile', True)

        elif validate.email(email) != True:

            if jquery == "yes":
                msg = 8
            else:
                FlashBootstrap.warning("Invalid Email Address")
                return app.redirect('/edit/profile', True)
        elif area_code == "":
            if jquery == "yes":
                msg = 7
            else:
                FlashBootstrap.error("Choose Country Code")
                return app.redirect('/edit/profile', True)

        elif phone == "":
            if jquery == "yes":
                msg = 6
            else:
                FlashBootstrap.error("Enter Phone Number")
                return app.redirect('/edit/profile', True)

        elif validate.phone(str(area_code)+str(phone)) != True:
            if jquery == "yes":
                msg = 5
            else:
                FlashBootstrap.error("Invalid Phone Number")
                return app.redirect('/edit/profile', True)

        else:

            data = [{
                'users_fname': fname,
                'users_lname': lname,
                'users_email': email,
                'users_area_code': area_code,
                'users_phone': phone,
                'users_updated_at': now.datetime(),

            }]
            if users.by_id(users_id)[0] > 0:
                if users.update(data, users_id) == True:
                    # send message to registered user
                    if jquery == "yes":
                        msg = 1
                    else:

                        FlashBootstrap.success("Profile Updated Successfully")
                        return app.redirect('/edit/profile', True)

                else:
                    if jquery == "yes":
                        msg = 2
                    else:
                        FlashBootstrap.error(
                            "Unable To Proccess this action, Try again later")
                        return app.redirect('/edit/profile', True)

            else:
                if jquery == "yes":
                    msg = 3
                else:
                    FlashBootstrap.error(
                        description="Account doesnot exist or has been deleted", showin='login')
                    return app.redirect('/logout', True)
    else:
        if jquery == "yes":
            msg = 0
        else:
            FlashBootstrap.warning("Invalid Request")
            return app.redirect('/edit/profile', True)

    return app.XHreponse(msg)


def add_address(Request, Session):
    msg = 0
    jquery = Request.post('jquery')
    if Request.method == "POST":
        address_country = Request.post('address_country')
        address_state = Request.post('address_state')
        address_city = Request.post('address_city') if Request.post(
            'address_city') != "" else 0
        address_postal_code = Request.post('address_postal_code')
        address_phone = Request.post('address_phone')
        address_name = Request.post('address_name')
        address_default = Request.post('address_default')
        users_id = Request.post('users_id')

        if address_country == "" and address_state == "" and address_city == "" and address_name == "" and address_phone == "":
            if jquery == "yes":
                msg = 10
            else:
                FlashBootstrap.error("Fill out all required field")
                return app.redirect('/add/address', True)
        elif address_country == "":
            if jquery == "yes":
                msg = 9
            else:
                FlashBootstrap.error("Choose Country")
                return app.redirect('/add/address', True)

        elif address_state == "":
            if jquery == "yes":
                msg = 8
            else:
                FlashBootstrap.error("Choose State")
                return app.redirect('add/address', True)

        elif address_postal_code == "":
            if jquery == "yes":
                msg = 7
            else:
                FlashBootstrap.error("Enter Postal")
                return app.redirect('/add/address', True)

        elif address_name == "":
            if jquery == "yes":
                msg = 6
            else:
                FlashBootstrap.error("Enter Address")
                return app.redirect('add/address', True)

        elif address_phone == "":
            if jquery == "yes":
                msg = 5
            else:
                FlashBootstrap.error("Enter Phone")
                return app.redirect('add/address', True)

        elif validate.phone(address_phone) != True:
            if jquery == "yes":
                msg = 4
            else:
                FlashBootstrap.error("Invalid Phone Number")
                return app.redirect('add/address', True)
        else:

            if address_default == 'on':
                default = 1
            else:
                default = 0

            data = [{
                'users_id': users_id,
                'address_country': address_country,
                'address_state': address_state,
                'address_city': address_city,
                'address_postal_code': address_postal_code,
                'address_name': address_name,
                'address_phone': address_phone,
                'address_default': default,
                'address_created_at': now.datetime(),
            }]

            if default == 1:
                datadefault = [{
                    'address_default': 0,
                }]
                Address().update_user_id(datadefault, users_id)

            if Address().insert(data) == True:
                # send message to registered user
                if jquery == "yes":
                    msg = 1
                else:
                    FlashBootstrap.success(
                        description="New Address added successfully", title="", showin='address')
                    return app.redirect('/address', True)
            else:
                if jquery == "yes":
                    msg = 2
                else:
                    FlashBootstrap.error(
                        "Unable To Proccess this action, Try again later")
                    return app.redirect('/add/address', True)

    else:
        if jquery == "yes":
            msg = 0
        else:
            FlashBootstrap.warning(
                description="Invalid Request",  showin="/add/address")
            return app.redirect('/add/address', True)


def update_address(Request, Session):
    msg = 0
    jquery = Request.post('jquery')
    if Request.method == "POST":
        address_country = Request.post('address_country')
        address_state = Request.post('address_state')
        address_city = Request.post('address_city') if Request.post(
            'address_city') != "" else 0
        address_postal_code = Request.post('address_postal_code')
        address_phone = Request.post('address_phone')
        address_name = Request.post('address_name')
        address_default = Request.post('address_default')
        users_id = Request.post('users_id')
        address_id = Request.post('address_id')
        if address_country == "" and address_state == "" and address_city == "" and address_name == "" and address_phone == "":
            if jquery == "yes":
                msg = 10
            else:
                FlashBootstrap.error("Fill out all required field")
                return app.redirect('/edit/address/{}'.format(address_id), True)
        elif address_country == "":
            if jquery == "yes":
                msg = 9
            else:
                FlashBootstrap.error("Choose Country")
                return app.redirect('/edit/address/{}'.format(address_id), True)

        elif address_state == "":
            if jquery == "yes":
                msg = 8
            else:
                FlashBootstrap.error("Choose State")
                return app.redirect('/edit/address/{}'.format(address_id), True)

        elif address_postal_code == "":
            if jquery == "yes":
                msg = 7
            else:
                FlashBootstrap.error("Enter Postal")
                return app.redirect('/edit/address/{}'.format(address_id), True)

        elif address_name == "":
            if jquery == "yes":
                msg = 6
            else:
                FlashBootstrap.error("Enter Address")
                return app.redirect('/edit/address/{}'.format(address_id), True)

        elif address_phone == "":
            if jquery == "yes":
                msg = 5
            else:
                FlashBootstrap.error("Enter Phone Number")
                return app.redirect('/edit/address/{}'.format(address_id), True)

        elif validate.phone(address_phone) != True:
            if jquery == "yes":
                msg = 4
            else:
                FlashBootstrap.error("Invalid Phone Number")
                return app.redirect('/edit/address/{}'.format(address_id), True)
        else:

            if address_default == 'on':
                default = 1
            else:
                default = 0

            data = [{
                'address_country': address_country,
                'address_state': address_state,
                'address_city': address_city,
                'address_postal_code': address_postal_code,
                'address_name': address_name,
                'address_phone': address_phone,
                'address_default': default,
                'address_created_at': now.datetime(),
            }]

            if default == 1:
                datadefault = [{
                    'address_default': 0,
                }]
                Address().update_user_id(datadefault, users_id)

            if Address().update_id_userid(data, address_id, users_id) == True:
                # send message to user concerning account update
                if jquery == "yes":
                    msg = 1
                else:
                    FlashBootstrap.success(
                        description="Address Updated successfully", title="", showin='address')
                    return app.redirect('/address', True)
            else:
                if jquery == "yes":
                    msg = 2
                else:
                    FlashBootstrap.error(
                        "Unable To Proccess this action, Try again later")
                    return app.redirect('/edit/address/{}'.format(address_id), True)

    else:
        if jquery == "yes":
            msg = 0
        else:
            FlashBootstrap.warning(
                description="Invalid Request",  showin="/edit/address")
            return app.redirect('/edit/address/{}'.format(address_id), True)


def get_state_by_country(Request):
    country = ""
    responseArray = []
    response = "States"
    if Request.method == "POST":
        country = Request.post("country_id")
        if country != "":
            result = Region().state_by_country_id(country)
            if result[0] > 0:
                for ls_getlist in result[1]:
                    responseArrayPrint = {}
                    responseArrayPrint["id"] = ls_getlist["state_id"]
                    responseArrayPrint["name"] = ls_getlist["state_name"]
                    responseArray.append(responseArrayPrint)

    JResult = dict({response: responseArray})

    return app.XHreponse(app.Jdumps(JResult))


def get_cities_by_state(Request):
    state, result = "", ""
    responseArray = []
    response = "Cities"
    if Request.method == "POST":
        state = Request.post("state_id")
        if state != "":
            result = Region().city_by_state_id(state)
            for ls_getlist in result[1]:
                responseArrayPrint = {}
                responseArrayPrint["id"] = ls_getlist["city_id"]
                responseArrayPrint["name"] = ls_getlist["city_name"]
                responseArray.append(responseArrayPrint)

    JResult = dict({response: responseArray})

    return app.XHreponse(app.Jdumps(JResult))


def forget_password(Request, Session):

    msg = 0
    jquery = Request.post('jquery')
    if Request.method == "POST":
        email = Request.post('email')

        if email == "":
            if jquery == "yes":
                msg = 6
            else:
                FlashBootstrap.error("Enter Email Address and Password")
                return app.redirect('/forget/password', True)

        elif validate.email(email) != True:
            if jquery == "yes":
                msg = 5
            else:
                FlashBootstrap.error("Invalid Email Address")
                return app.redirect('/forget/password', True)
        else:

            if users.by_email(email)[0] > 0:
                fetch = users.by_email(email)[1][0]

                email = fetch["users_email"]
                if jquery == "yes":
                    msg = 1
                else:
                    FlashBootstrap.success(
                        "Forget Password Submitted, Link has been sent to your mail inbox")
                    return app.redirect('/forget/password', True)

            else:
                if jquery == "yes":
                    msg = 3
                else:
                    FlashBootstrap.warning(
                        "No Account link to this Email Address")
                    return app.redirect('/forget/password', True)
    else:
        if jquery == "yes":
            msg = 0
        else:
            FlashBootstrap.warning("Invalid Request")
            return app.redirect('/forget/password', True)

    return app.XHreponse(msg)


def add_to_cart(Request, Session):
    #/add/cart/
    #happ.header()
    jquery = Request.post("jquery")     
    if Request.method == "POST":
        product_para = Request.params("product_para")
        product_id = Request.params("product_id")
        product_dim_quantity = Request.post("product_quantity")
        items_dict = {
                    'product_para': product_para,
                    'product_id': product_id,
                    'product_dim_quantity': product_dim_quantity,
        }

        if Session.has('shop_to_cart') == True:
            if product_id not in Cart.find('shop_to_cart', 'product_id'):
                
                session_cart = Session.get('shop_to_cart')
                session_cart.append(items_dict)
                Session.set('shop_to_cart', session_cart)
                FlashBootstrap.success(description="Item added to cart successfully", showin='cart')
                return FlashBootstrap.redirect('/cart', True)
            else:
                if jquery == "yes":
                    msg = 0
                else:
                    FlashBootstrap.info(description="Item already added to cart", showin='cart')
                    return FlashBootstrap.redirect('/cart', True)
                    #return app.redirect(app.referer('/cart'))

        else:
            
            Session.set('shop_to_cart', [items_dict])
            if jquery == "yes":
                    msg = 0
            else:
                FlashBootstrap.success(description="Item added to cart successfully", showin='cart')
                return FlashBootstrap.redirect('/cart', True)
    else:
        if jquery == "yes":
            msg = 0
        else:
            FlashBootstrap.warning("Invalid Request")
            return FlashBootstrap.redirect('/', True)

def delete_from_cart(Request):
    
    
    if Request.method == 'GET':
        
        if Request.get('product_id') == "all":
            response = Cart.delete('shop_to_cart', 'product_id')
        else:
            
            response = Cart.delete('shop_to_cart', 'product_id', Request.get('product_id'))
            
        if response is True:
            
            FlashBootstrap.success(description="Item deleted from cart successfully", showin='cart')
            return FlashBootstrap.redirect('/cart', True)
        else:
            FlashBootstrap.error(description="can not delete empty cart", showin='cart')
            return FlashBootstrap.redirect('/cart', True)
    else:
        FlashBootstrap.warning("Invalid Request")
        return FlashBootstrap.redirect('/cart', True)


def update_cart(Request):
    
    if Request.method == "POST":
        product_id = Request.post('product_id')
        product_quantity = Request.post('product_quantity')
        upitem = {'product_dim_quantity': product_quantity}

        response = Cart.update('shop_to_cart', "product_id", product_id, upitem)
        if response is True:
            FlashBootstrap.success(description="Item Updated successfully", showin='cart')
            return FlashBootstrap.redirect('/cart', True)

    else:
        FlashBootstrap.warning("Invalid Request")
        return FlashBootstrap.redirect('/cart', True)



def add_to_wishlist(Request, Session):
    
    if Request.method == "GET":
        product_id = Request.get('product_id')
        if Session.has('users_id') == True and Session.get('users_id') != "":
            if product_id != "":
                check = Products().by_product_id_wishlist(product_id)
                if check[0] < 1:
                    data = [{
                        'products_id': product_id,
                        'users_id': Session.get('users_id'),
                        'wishlist_created_at': now.datetime()
                    }]
                    result = Products().insert_wishlist(data)
                    if result == True:
                        FlashBootstrap.success(description="Item Added to wishlist successfully")
                        return FlashBootstrap.redirect('/cart', True)
                    else:
                        FlashBootstrap.warning(description="Unable to process this action")
                        return FlashBootstrap.redirect('/cart', True)
                else:
                    FlashBootstrap.warning(description="Item Already in your wishlist")
                    return FlashBootstrap.redirect('/cart', True)
            else:
                FlashBootstrap.error(description="Parameter Empty")
                return FlashBootstrap.redirect('/cart', True)
        else:
            
            FlashBootstrap.error(description="Authentication Proccess needed, <strong><a href='{url}'>Login</a></strong> and try agin".format(url=url('/login', True)))
            
            return FlashBootstrap.redirect('/cart', True)

    else:
        FlashBootstrap.warning(description="Invalid Request")
        return FlashBootstrap.redirect('/cart', True)