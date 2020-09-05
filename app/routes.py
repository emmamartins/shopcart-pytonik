from pytonik.Router import Router

route = Router()

route.any("/", "indexController@index:id")

route.get('index/login', route.args(
    params=['para', 'type', 'action'], to = "login"

))
route.get('index/register', route.args(
    params=['para', 'type', 'action'], to = "register"

))
route.get('index/cart', route.args(
    params=['para', 'type', 'action'], to = "cart"

))

route.get('index/dashboard', route.args(
    params=['para', 'type', 'action'], to = "dashboard"

))

route.get('index/address', route.args(
    params=['id', 'type'], to = "address"

))

route.get('index/product', route.args(
    params=['para', 'type', 'action'], to = "product"

))

route.get('index/product_detail', route.args(
    params=['product_para', 'action'], to = "detail"

))

route.get('index/order_history', route.args(
    params=['para', 'type', 'action'], to = "order"

))
route.get('index/add_address', route.args(
    params=['country_id', 'state_id'], to = "add/address"

))

route.get('index/forget_password', route.args(
    params=['para', 'type', 'action'], to = "forget/password"

))

route.get('index/edit_profile', route.args(
    params=['para', 'type', 'action'], to = "edit/profile"

))

route.get('index/edit_address', route.args(
    params=['address_id'], to = "edit/address"

))

route.post('ajax/add_to_cart', route.args(
    params=['product_para', 'product_id'], to = "add/cart"

))

route.get('index/cart', route.args(
    params=['product_para', 'product_id'], to = "cart"

))
#delete/cart

route.get('ajax/delete_from_cart', route.args(
    params=['product_id', 'product_para'], to = "delete/cart"

))

#/add/wishlist/
route.get('ajax/add_to_wishlist', route.args(
    params=['product_id'], to = "add/wishlist"

))

#update/cart
route.post('ajax/update_cart', route.args(
    params=['product_id'], to = "update/cart"

))

#proccess-cart
route.get('index/proccess_cart', route.args(
     to = "proccess-cart"

))

route.get('logout', 'IndexController@logout')

# Admin Routings settings 
route.get('admin/add_products', route.args(
    params=['product_id'], to = "admin/add/products"

))


route.get('admin/list_products', route.args(
    params=['page'], to = "admin/products"

))


#list_users
route.get('admin/list_users', route.args(
    params=['page_on', 'status'], to = "admin/users"

))
route.get('admin/add_users', route.args( 
    to = "admin/add/users"

))
route.get('admin/edit_users', route.args(
    params=['users_id'], to = "admin/edit/users"

))
route.get('admin/list_products', route.args(
    params=['address_id'], to = "admin/products"

))