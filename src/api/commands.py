
import click
from api.models import db, Users, Products, Orders, ProductsInOrder, Checkout, Followers, Favorites, Reviews, ShoppingCart
import json


"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration 
with youy database, for example: Import the price of bitcoin every night as 12am
"""
def setup_commands(app):
    
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    # @app.cli.command("insert-test-users") # name of our command
    # @click.argument("count") # argument of out command
    # def insert_test_users(count):
    #     print("Creating test users")
    #     for x in range(1, int(count) + 1):
    #         user = Users()
    #         user.email = "test_user" + str(x) + "@test.com"
    #         user.password = "123456"
    #         user.is_active = True
    #         db.session.add(user)
    #         db.session.commit()
    #         print("User: ", user.email, " created.")

    #     print("All test users created")

    @app.cli.command("insert-test-data")
    def insert_test_data():
        pass
    @app.cli.command('dummy')
    def dummy():
        with open('src/api/products.json', 'r') as file:
            data = json.load(file)
        with open('src/api/users.json', 'r') as file_2:
            data_user = json.load(file_2)
        with open('src/api/favorites.json', 'r') as file_3:
            favorites_data = json.load(file_3)
        with open('src/api/shoppingcart.json', 'r') as file_4:
            shopping_data = json.load(file_4)
        with open('src/api/reviews.json', 'r') as file_5:
            reviews_data = json.load(file_5)
        for i in data['consoles']:
            print (i['name'])
            prod = Products()
            prod.name = i['name']
            prod.img = i['img']
            prod.year = i['year']
            prod.brand = i['brand']
            prod.platform = i['platform']
            prod.type = i['type']
            prod.category = i['category']
            prod.description = i['description']
            prod.stock = i['stock']
            prod.state = i['state']
            prod.promoted = i['promoted']
            prod.price = i['price']
            db.session.add(prod)
            db.session.commit()
        for i in data['videogames']:
            print (i['name'])
            prod = Products()
            prod.name = i['name']
            prod.img = i['img']
            prod.year = i['year']
            prod.brand = i['brand']
            prod.platform = i['platform']
            prod.type = i['type']
            prod.category = i['category']
            prod.description = i['description']
            prod.stock = i['stock']
            prod.state = i['state']
            prod.promoted = i['promoted']
            prod.price = i['price']
            db.session.add(prod)
            db.session.commit()
        for i in data['accessory']:
            print (i['name'])
            prod = Products()
            prod.name = i['name']
            prod.img = i['img']
            prod.year = i['year']
            prod.brand = i['brand']
            prod.platform = i['platform']
            prod.type = i['type']
            prod.category = i['category']
            prod.description = i['description']
            prod.stock = i['stock']
            prod.state = i['state']
            prod.promoted = i['promoted']
            prod.price = i['price']
            db.session.add(prod)
            db.session.commit() 
        for i in data_user['users']:
            print (i['userName'])
            prod = Users()
            prod.email = i['email']
            prod.password = i['password']
            prod.userName = i['userName']
            prod.avatar = i['avatar']
            prod.description = i['description']
            prod.address = i['address']
            prod.postalCode = i['postalCode']
            prod.city = i['city']
            prod.following = i['following']
            prod.subscription = i['subscription']
            prod.role = i['role']
            db.session.add(prod)
            db.session.commit()   
        for i in favorites_data['favorites']:
            print (i['user_id'])
            prod = Favorites()
            prod.user_id = i['user_id']
            prod.product_id = i['product_id']
            db.session.add(prod)
            db.session.commit()    
        for i in shopping_data['shopping_cart']:
            print (i['user_id'])
            prod = ShoppingCart()
            prod.user_id = i['user_id']
            prod.product_id = i['product_id']
            db.session.add(prod)
            db.session.commit()  
        for i in reviews_data['reviews']:
            print (i['comment'])
            prod = Reviews()
            prod.rating = i['rating']
            prod.comment = i['comment']
            prod.user_id = i['user_id']
            prod.product_id = i['product_id']
            db.session.add(prod)
            db.session.commit()         
 


      