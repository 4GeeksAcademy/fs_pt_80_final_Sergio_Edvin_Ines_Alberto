"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Products, Orders, ProductsInOrder, Checkout, Followers, Users, Favorites, Reviews,ShoppingCart
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import datetime
import stripe
import os
import datetime
import cloudinary
import cloudinary.uploader
import json

api = Blueprint('api', __name__)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Allow CORS requests to this API
CORS(api)


## ······················································· Cómo USER (profile):

@api.route('/register', methods=['POST'])
def register():
    try:
        # Aquí extraemos los datos del JSON
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        userName = request.json.get('userName', None)

        if not email or not password or not userName:
            return jsonify({'msg': 'Missing data'}), 400

        # Verificamos si el usuario ya existe
        check_user = Users.query.filter_by(email=email).first()

        if check_user:  # Si el usuario ya existe, devolvemos un error
            return jsonify({"msg": "User already registered"}), 400

        new_user = Users(email=email, password=password, userName=userName)

        db.session.add(new_user)
        db.session.commit()

        # Creamos un token para el nuevo usuario
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=str(new_user.id), expires_delta=expires)

      
        return {"msg": "okey", 'token': access_token, 'user': new_user.serialize()}, 201

    except Exception as error:
  
        db.session.rollback()
        return jsonify({'error': str(error)}), 400
    

@api.route('/user/<int:user_id>', methods=['PUT'])       
@jwt_required()
def update_user(user_id):
    try:
        # Obtener el usuario autenticado
        id = get_jwt_identity()
        user = Users.query.get(id)
        if not user:
            return jsonify({'msg': 'Unauthorized: User not found'}), 401

        # Extraer datos del cuerpo de la solicitud
        userName = request.json.get('userName')
        description = request.json.get('description')
        city = request.json.get('city')
        address = request.json.get('address')
        postalCode = request.json.get('postalCode')
        avatar = request.json.get('avatar')

        # Asegurarse de que al menos un campo está presente
        if not (userName or description or city or avatar or address or postalCode):
            return jsonify({'msg': 'No data provided to update'}), 400

        # Obtener el usuario que se desea actualizar
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404

        # Actualizar solo los campos proporcionados
        if userName is not None:
            user.userName = userName
        if description is not None:
            user.description = description
        if city is not None:
            user.city = city
        if address is not None:
            user.address = address
        if postalCode is not None:
            user.postalCode = postalCode
        if avatar is not None:
            user.avatar = avatar

        # Guardar los cambios en la base de datos
        db.session.commit()
        return jsonify({'msg': 'User updated successfully'}), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400
   
@api.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()      
def delete_user(user_id):
    try:
        id = get_jwt_identity()
        user = Users.query.get(id)
        if not user:
            return jsonify({'msg':'Unauthorized: User not found'}), 401
        #retrieve the user by id
        if user.id != user_id:
            return jsonify({'msg': 'Unauthorized: You can only delete your own account'}), 404
        
        #delete user
        db.session.delete(user)
        db.session.commit()

        return jsonify({'msg': 'User deleted successfully'}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400
    
#funciona!!!
@api.route('/users', methods=['GET'])  #para ver otros user
def get_users():
    try:
        # retrieve all users
        users = Users.query.all()
        users_list = [user.serialize() for user in users]

        return jsonify(users_list), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 400

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Retrieve a single user by ID
        user = Users.query.get(user_id)

        # Check if the user exists
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify(user.serialize()), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 400
  

##........................................................ COMO USER LOGIN 

@api.route('/login', methods=['POST'])  
def login():
    try: 
        # aqui extraemos info
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        # aqui chequeamos que toda la info este
        if not email or not password:
            return jsonify({'msg': 'Missing data'}), 400
        
        # aqui chequeamos si usuario existe
        check_user= Users.query.filter_by(email=email).first()

        if check_user.password == password:
             expires = datetime.timedelta(days=1)
            
             access_token = create_access_token(identity=str(check_user.id), expires_delta=expires)
             return ({"msg": "ok", "token": access_token, "user":check_user.serialize()}), 201
        return jsonify({"msg": "Contraseña incorrecta"}), 400
    
    except Exception as error:
            db.session.rollback()
            return jsonify({'error': str(error)}), 400


##·······················································  Cómo USER(buy/sell):

@api.route('/product', methods=['POST']) 
@jwt_required()     
def create_product():
    print(request.json)
    try:
        id = get_jwt_identity()
        user = Users.query.get(id)
        if not user:
            return jsonify({'msg':'Unauthorized: User not found'}), 401
        #extract product details from the request
        name = request.json.get('name', None)
        description = request.json.get('description', None)
        img = request.json.get('img', None)
        year = request.json.get('year', None)
        brand = request.json.get('brand', None)
        platform = request.json.get('platform', None)
        type = request.json.get('type', None)
        category = request.json.get('category', None)
        state = request.json.get('state', None)
        #promoted = request.json.get('promoted', None) 
        price = request.json.get('price', None)
        
        

        #validate required fields
        if not name or not description or not img or not year or not brand or not platform or not category or not type or not state  or not price:
            return jsonify({'msg': 'Please fill all the data'}), 400
        
        #create a new product
        new_product = Products(name=name, description=description, img=img, year=year, brand=brand, platform=platform, category=category, type=type, state=state, price=price, seller_id = id)
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'msg': 'Product created successfully', 'product': new_product.serialize()}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400
    
@api.route('/product/<int:product_id>', methods=['PUT'])  
@jwt_required()
def update_product(product_id):
    try:
        id = get_jwt_identity()
        user = Users.query.get(id)
        if not user:
            return jsonify({'msg':'Unauthorized: User not found'}), 401
        # extract user_id from the request
        # user_id = request.json.get('user_id', None)

        # find the product by id
        product = Products.query.get(product_id)
        if not product:
            return jsonify({'msg': 'Product not found '}), 404
        print(product.seller_id)

        if product.seller_id != int(id):
            return jsonify({'msg': 'not owned by the user', 'id': id, "seller_id": product.seller_id}), 404
        print(id)
        
        #update product details
        product.name = request.json.get('name', product.name)
        product.description = request.json.get('description', product.description)
        product.img = request.json.get('img', product.img)
        product.year = request.json.get('year', product.year)
        product.brand = request.json.get('brand', product.brand)
        product.platform = request.json.get('platform', product.platform)
        product.type = request.json.get('type', product.type)
        product.state = request.json.get('state', product.state)
        product.price = request.json.get('price', product.price)

        db.session.commit()
        return jsonify({'msg': 'Product updated successfully'}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400
    
@api.route('/product/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        id = get_jwt_identity()
        user = Users.query.get(id)
        if not user:
            return jsonify({'msg':'Unauthorized: User not found'}), 401

        #find product id
        product =  Products.query.get(product_id)
        if not product_id or product.seller_id != int(id):
            return jsonify({'msg': 'Product not found'}), 404
        
        #delete product
        db.session.delete(product)
        db.session.commit()
        return jsonify({'msg': 'Product deleted successfully'}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400


@api.route('/products', methods=['GET'])
def get_products():
    try:
        # bring all products
        products = Products.query.all()
        products_list = [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'img': product.img,
                'year': product.year,
                'brand': product.brand,
                'category': product.category,
                'platform': product.platform,
                'type': product.type,
                'state': product.state,
                'promoted': product.promoted,
                'price': product.price,
                'stock': product.stock

            } for product in products
        ]
        return jsonify(products_list), 200
    except Exception as error:
        return jsonify({'error': str(error)})
    

@api.route('/product/<int:product_id>', methods=['GET'])  
def get_product(product_id):
    try:
        # bring one product with id
        product = Products.query.get(product_id)

        if not product:
            return jsonify({'error': 'Product not found'}), 404
        product_data = [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'img': product.img,
                'year': product.year,
                'brand': product.brand,
                'category': product.category,
                'platform': product.platform,
                'type': product.type,
                'state': product.state,
                'promoted': product.promoted,
                'price': product.price,
                'stock': product.stock

            } 
        ]
        return jsonify(product_data), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 400
    

    ##······················································· Cómo USER favs. 

@api.route('/favorites', methods=['POST'])
@jwt_required()
def add_to_favorites():
    try:
        id = get_jwt_identity()
        user = Users.query.get(id)
        if not user:
            return jsonify({'msg':'Unauthorized: User not found'}), 403
        #extractproduct_id from the request  
        product_id = request.json.get('product_id', None)

        #validate required fields
        if not product_id:
            return jsonify({'msg': 'Product ID are required'}), 400
        
        # check if favorite already exist
        existing_favorite = Favorites.query.filter_by(user_id=id, product_id=product_id).first()
        if existing_favorite:
            db.session.delete(existing_favorite)
            db.session.commit()
            updated_favorites = [fav.product_id for fav in user.favorites] 
            return jsonify({'msg': 'Product deleted', 'updatedFavorites': updated_favorites}), 200
        else:
        # add to favorites
            new_favorite = Favorites(user_id=id, product_id=product_id)
            db.session.add(new_favorite)
            db.session.commit()

        updated_favorites = [fav.product_id for fav in user.favorites]
        return jsonify({'msg': 'Added to favorites successfully', 'updatedFavorites': updated_favorites}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400
    
@api.route('/favorite/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_favorite(product_id):
    try:
        id = get_jwt_identity()
        user = Users.query.get(id)
        if not user:
            return jsonify({'msg': 'Unauthorized: User not found'}), 401

        if not id:
            return jsonify({'msg': 'User ID is required'}), 400
        
        favorite = Favorites.query.filter_by(user_id=id, product_id=product_id).first()
        if not favorite:
            return jsonify({'msg': 'Favorite not found'}), 404
        
        db.session.delete(favorite)
        db.session.commit()

    
        updated_favorites = Favorites.query.filter_by(user_id=id).all()
        updated_favorites_list = [{'product_id': fav.product_id} for fav in updated_favorites]

        return jsonify({'msg': 'Removed from favorites successfully', 'updatedFavorites': updated_favorites_list}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400
    
@api.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    try:
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)

        if not user:
            return jsonify({'msg': 'User not found'}), 404

        favorites = Favorites.query.filter_by(user_id=user_id).all()
        favorite_product_ids = [favorite.product_id for favorite in favorites]

        favorite_products = Products.query.filter(Products.id.in_(favorite_product_ids)).all()
        favorite_products_list = [product.serialize() for product in favorite_products]

        return jsonify({'favorite_products': favorite_products_list}), 200

    except Exception as error:
        return jsonify({'error': str(error)}), 500

    



##··········································································Cómo USER en CHECKOUT:

@api.route('/checkout', methods=['POST'])
@jwt_required()
def add_to_checkout():
    try:
        
        user_id = get_jwt_identity()
        product_id = request.json.get('product_id', None)

        #validate required fields
        if not user_id or not product_id:
            return jsonify({'msg': 'User ID and Product ID are required'}), 400

        #check if the product is already in checkout
        existing_checkout_item = Checkout.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing_checkout_item:
            return jsonify({'msg': 'Product already in checkout'}), 400
        
        #add product to the users checkout
        new_checkout_item = Checkout(user_id=user_id, product_id=product_id)
        db.session.add(new_checkout_item)
        db.session.commit()

        return jsonify({'msg': 'Product added to the checkout successfully'}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400
    

@api.route('/users/following', methods=['GET'])
@jwt_required()
def get_following():
    try:
        id = get_jwt_identity()
        following = Followers.query.filter_by(follower_id=id).all()
        
        return jsonify([f.serialize() for f in following]), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 400

@api.route('/users/follow', methods=['POST'])
@jwt_required()
def follow_user():
    try:
        id = get_jwt_identity()
        followed_id = request.json.get('followed_id', None)

        if not followed_id:
            return jsonify({'error':'Followed ID is required'}), 400

        new_follower = Followers(follower_id= id, followed_id=followed_id)
        db.session.add(new_follower)
        db.session.commit()

        return jsonify({'msg':'User followed successfully'}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400
        
@api.route('/users/unfollow/<int:followed_id>', methods=['DELETE'])
@jwt_required()
def unfollow_user(followed_id):
    try:
        id = get_jwt_identity()
        follow = Followers.query.filter_by(follower_id=id, followed_id=followed_id).first()

        if not follow:
            return jsonify({'error': 'Follow relationship not found'}), 404

        db.session.delete(follow)
        db.session.commit()
        return jsonify({'msg': 'Unfollowed user successfully'}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400


@api.route('/reviews', methods=['GET'])
def get_all_reviews():
    try:
        reviews = Reviews.query.all()  
        return jsonify([r.serialize() for r in reviews]), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 400


    ##nuevo STRIPE! pago para productos y suscripcion

def getPrice(products):
    try:
        total = 0
        product_ids = [product["id"] for product in products]
        
        db_products = Products.query.filter(Products.id.in_(product_ids)).all() # Query all products from database 
        
        price_map = {str(product.id): product.price for product in db_products}  # Create a map of product id to price for faster lookup
        
        # Sum prices
        for product in products:
            product_id = str(product["id"])
            if product_id in price_map:
                
                price_in_cents = int(float(price_map[product_id]) * 100)   # Convert price to cents for Stripe and to make sure to be integer
                total += price_in_cents
            
        return total

    except Exception as e:
        print(f"Error in getPrice: {str(e)}")
        raise e

@api.route('/create-payment', methods=['POST'])
@jwt_required()
def create_payment():
    try:
        id = get_jwt_identity()
        user = Users.query.get(id)

        if not user:
            return jsonify({'msg': 'Unauthorized: User not found'}), 401
        
        data = request.json

        # total_amount = 0  # initialize the total

        # if data.get("products"):                    #if in a cart -> calculate total products 
        #     print(data.get('products'))
        #     total_amount = getPrice(data["products"])

        # if data.get("suscripcion"):                 #add subscr. cost if selected
        #     suscription_amount = int(9.99 * 100)
        #     total_amount += suscription_amount



        intent = stripe.PaymentIntent.create(
            amount=data.get('amount'),
            currency="eur",
            automatic_payment_methods={
                'enabled': True
            }
        )

        return jsonify({'success': True, 'clientSecret': intent.client_secret})

    except Exception as e:
         return jsonify({'success': False, 'error': str(e)})

    
##---------------------------------------------------MERGING LOCAL STORE TO BACK---------------------------------------------    

@api.route('/merge-data', methods=['POST'])
@jwt_required()
def merge_data():
    try:
        user_id = get_jwt_identity()  # Obtiene el user_id del token
        user = Users.query.get(user_id)

        if not user:
            return jsonify({'msg': 'Usuario no encontrado'}), 404

        data = request.json
        local_favorites = data.get('localFavorites', [])
        local_shopping_cart = data.get('localShoppingCart', [])

        # Fusionar favoritos sin duplicados
        for fav in local_favorites:
            exists = Favorites.query.filter_by(user_id=user_id, product_id=fav['product_id']).first()
            if not exists:
                new_fav = Favorites(user_id=user_id, product_id=fav['product_id'])
                db.session.add(new_fav)

        # Fusionar carrito sin duplicados
        for item in local_shopping_cart:
            exists = ShoppingCart.query.filter_by(user_id=user_id, product_id=item['product_id']).first()
            if not exists:
                new_cart_item = ShoppingCart(user_id=user_id, product_id=item['product_id'])
                db.session.add(new_cart_item)

        db.session.commit()

        return jsonify({'msg': 'Datos fusionados correctamente', 'success': True}), 200

    except Exception as e:
        return jsonify({'msg': 'Error en la fusión de datos', 'error': str(e)}), 500


@api.route('/payment-succeeded', methods=['POST'])
@jwt_required()
def payment_succeeded():
        try:
            id = get_jwt_identity()
            user = Users.query.get(id)
            data = request.json
            print(data)
            payment_intent = data['payment_intent']
            # payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            # if payment_intent.status != 'succeeded':
            #     return jsonify({'msg': 'Pago sin exito'}), 400
            
            
            # getting items from the cart
            cart_items = ShoppingCart.query.filter_by(user_id=id).all() 
            shopping_cart_product_ids = [item.product_id for item in cart_items]
            print(shopping_cart_product_ids) 
            print(cart_items)
            # print(data['amount']-700 if user.subscription else data['amount'])
            print(user.serialize())

            #creating the order
            new_order = Orders(
                date= datetime.datetime.now(),
                subtotal_amount=float(data['amount']),
                total_amount=float(data['amount']),
                
                discount= user.subscription,
                
                status = 'confirmed',
                address = user.address,
                city=user.city,
                postal_code=user.postalCode,
                buyer_id=id
            )

            db.session.add(new_order)
            db.session.commit()


            #from shopping cart to order table
            for item in cart_items:
                new_products_order = ProductsInOrder(order_id = new_order.id, product_id=item.id)
                db.session.add(new_products_order)
                db.session.commit()
            
            #from order to checkout table
            checkout = Checkout(payment_method = 'stripe', status='Paid', order_id= new_order.id, user_id = user.id, stripe_id=payment_intent['id'])
            db.session.add(checkout)
            db.session.commit()
            
            
            # clearing cart after the order has been successful
            for item in cart_items:
                db.session.delete(item)
                db.session.commit()

            return jsonify({'msg': 'Pago realizado con exito y order ha sido creado', 'order': new_order.serialize()}), 200
        
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return jsonify({'msg': 'Error al procesar el pago'}), 500
        

        #buscar en el carrito los productos del usuario. 
        #crear orden(tabla back) (llama) (con los productos que estan en carrito)
        #y llamar todos los elementos de orders

        #__tablename__ = 'orders'
    # id = db.Column(db.Integer, primary_key=True)
    # date = db.Column(db.Date, nullable=False)
    # subtotal_amount = db.Column(db.Float, nullable=False)
    # total_amount = db.Column(db.Float, nullable=False)
    # discount = db.Column(db.Boolean, default=False)
    # status = db.Column(db.String)
    # address = db.Column(db.String, nullable=False)
    # city = db.Column(db.String, nullable=False)
    # postal_code = db.Column(db.Integer, nullable=False)
    # country = db.Column(db.String, nullable=False)
    # buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # crear 2 vistas (success, fail)
    # nuevo endpoint POST para almacenar orden
    # despues del compra -> vaciar el carrito

     

    
            
    
    
#     ## pago de subscricpion con stripe

# @api.route('/suscripcion-payment', methods=['POST'])
# def suscripcion():
#     try:
#         data = request.json
#         #PODEMOS PASAR TODOS LOS ELEMENTOS QUE PERMITA EL OBJETO DE PAYMENTINTENT.CREATE 
#         intent = stripe.PaymentIntent.create(
#             #amount=getPrice(data['products']), # se deberia de calcular el precio en el back, no recibirse del front
#             amount= 9.99, 
#             currency=data['eur'],
#             automatic_payment_methods={
#                 'enabled': True
#             }
#         )
#         return jsonify({
#             'clientSecret': intent['client_secret']
#         })
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})


#products = (urls)

# @api.route('/products', methods=['GET'])
# def get_products():
#     try:
#         return jsonify(products), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


#Shopping Cart
@api.route('/shopping-cart', methods=['GET'])
@jwt_required()
def get_shopping_cart():
    try:
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)

        if not user:
            return jsonify({'msg': 'User not found'}), 404

        shopping_cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()
        shopping_cart_product_ids = [item.product_id for item in shopping_cart_items]

        shopping_cart_products = Products.query.filter(Products.id.in_(shopping_cart_product_ids)).all()
        shopping_cart_products_list = [product.serialize() for product in shopping_cart_products]

        return jsonify({'shopping_cart_products': shopping_cart_products_list}), 200

    except Exception as error:
        return jsonify({'error': str(error)}), 500
    
@api.route('/shopping_cart', methods=['POST'])
@jwt_required()
def add_to_shopping_cart():
    try:
        id = get_jwt_identity()
        user = Users.query.get(id)
        if not user:
            return jsonify({'msg':'Unauthorized: User not found'}), 403
        
        # Extraer product_id 
        product_id = request.json.get('product_id', None)
        if not product_id:
            return jsonify({'msg': 'Product ID is required'}), 400
        
        # Verificar si el producto ya está en el carrito
        existing_item = ShoppingCart.query.filter_by(user_id=id, product_id=product_id).first()
        if existing_item:
            db.session.delete(existing_item)
            db.session.commit()

            db.session.refresh(user)

            updated_cart = [item.product_id for item in user.shoppingCart]
            return jsonify({'msg': 'Product removed from shopping cart' , 'updatedCart': updated_cart}), 200
        else:
        
            new_item = ShoppingCart(user_id=id, product_id=product_id)
            db.session.add(new_item)
            db.session.commit()

        # Actualizar la lista del carrito
        updated_cart = [item.product_id for item in user.shoppingCart]
        return jsonify({'msg': 'Added to shopping cart successfully', 'updatedCart': updated_cart}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400
    
    
@api.route('/shopping_cart/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_shopping_cart(product_id):
    try:
        id = get_jwt_identity()
        user = Users.query.get(id)
        if not user:
            return jsonify({'msg':'Unauthorized: User not found'}), 401 
        if not id:
            return jsonify({'msg': 'User ID is required'}), 400
        
        item = ShoppingCart.query.filter_by(user_id=id, product_id=product_id).first()
        if not item:
            return jsonify({'msg': 'Item not found in shopping cart'}), 404
        
        # Eliminar el producto del carrito
        db.session.delete(item)
        db.session.commit()

        return jsonify({'msg': 'Removed from shopping cart successfully'}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 400

# Subimos productos al Cloudinary

@api.route('/upload', methods=['POST'])
def upload():
    try:
        file_to_upload = request.files.get('file')
        if not file_to_upload:
            return jsonify({"error": "No file uploaded"}), 400
        
        upload = cloudinary.uploader.upload(file_to_upload)
        print('----------Url donde está la imagen-----------', upload)
        return jsonify(upload)
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@api.route('/dummy2', methods=['POST']) 
def dummy():
    favorites_data = {
    "favorites": [
        {
            "user_id": 1,
            "product_id": 82
        },
        {
            "user_id": 2,
            "product_id": 2
        },
        {
            "user_id": 3,
            "product_id": 62
        },
        {
            "user_id": 4,
            "product_id": 11
        },
        {
            "user_id": 5,
            "product_id": 56
        },
        {
            "user_id": 6,
            "product_id": 14
        },
        {
            "user_id": 7,
            "product_id": 14
        },
        {
            "user_id": 8,
            "product_id": 18
        },
        {
            "user_id": 9,
            "product_id": 30
        },
        {
            "user_id": 10,
            "product_id": 101
        },
        {
            "user_id": 11,
            "product_id": 18
        },
        {
            "user_id": 12,
            "product_id": 15
        },
        {
            "user_id": 3,
            "product_id": 18
        },
        {
            "user_id": 4,
            "product_id": 98
        },
        {
            "user_id": 5,
            "product_id": 89
        },
        {
            "user_id": 6,
            "product_id": 24
        },
        {
            "user_id": 7,
            "product_id": 34
        },
        {
            "user_id": 8,
            "product_id": 109
        },
        {
            "user_id": 9,
            "product_id": 102
        },
        {
            "user_id": 10,
            "product_id": 1
        },
        {
            "user_id": 11,
            "product_id": 31
        },
        {
            "user_id": 12,
            "product_id": 19
        },
        {
            "user_id": 3,
            "product_id": 43
        },
        {
            "user_id": 4,
            "product_id": 66
        },
        {
            "user_id": 1,
            "product_id": 70
        },
        {
            "user_id": 6,
            "product_id": 54
        },
        {
            "user_id": 7,
            "product_id": 37
        },
        {
            "user_id": 8,
            "product_id": 19
        },
        {
            "user_id": 9,
            "product_id": 94
        },
        {
            "user_id": 3,
            "product_id": 15
        },
        {
            "user_id": 1,
            "product_id": 14
        },
        {
            "user_id": 2,
            "product_id": 48
        },
        {
            "user_id": 3,
            "product_id": 12
        },
        {
            "user_id": 4,
            "product_id": 23
        },
        {
            "user_id": 5,
            "product_id": 36
        },
        {
            "user_id": 6,
            "product_id": 16
        },
        {
            "user_id": 3,
            "product_id": 94
        },
        {
            "user_id": 4,
            "product_id": 103
        },
        {
            "user_id": 6,
            "product_id": 100
        },
        {
            "user_id": 12,
            "product_id": 42
        },
        {
            "user_id": 9,
            "product_id": 47
        },
        {
            "user_id": 2,
            "product_id": 75
        },
        {
            "user_id": 4,
            "product_id": 84
        },
        {
            "user_id": 10,
            "product_id": 72
        },
        {
            "user_id": 5,
            "product_id": 44
        },
        {
            "user_id": 8,
            "product_id": 19
        },
        {
            "user_id": 9,
            "product_id": 72
        },
        {
            "user_id": 2,
            "product_id": 70
        },
        {
            "user_id": 9,
            "product_id": 99
        },
        {
            "user_id": 4,
            "product_id": 59
        }
    ]
}

    shopping_data = {
    "shopping_cart": [
      {"user_id": 12, "product_id": 89},
      {"user_id": 5, "product_id": 77},
      {"user_id": 9, "product_id": 43},
      {"user_id": 3, "product_id": 56},
      {"user_id": 4, "product_id": 20},
      {"user_id": 5, "product_id": 32},
      {"user_id": 11, "product_id": 78},
      {"user_id": 8, "product_id": 12},
      {"user_id": 7, "product_id": 54},
      {"user_id": 1, "product_id": 20},
      {"user_id": 8, "product_id": 98},
      {"user_id": 4, "product_id": 24},
      {"user_id": 6, "product_id": 67},
      {"user_id": 2, "product_id": 45},
      {"user_id": 2, "product_id": 58},
      {"user_id": 10, "product_id": 23},
      {"user_id": 3, "product_id": 13},
      {"user_id": 4, "product_id": 34},
      {"user_id": 9, "product_id": 17},
      {"user_id": 6, "product_id": 9},
      {"user_id": 9, "product_id": 91},
      {"user_id": 2, "product_id": 82},
      {"user_id": 1, "product_id": 15},
      {"user_id": 7, "product_id": 56},
      {"user_id": 8, "product_id": 33},
      {"user_id": 2, "product_id": 77},
      {"user_id": 9, "product_id": 96},
      {"user_id": 5, "product_id": 4},
      {"user_id": 11, "product_id": 44},
      {"user_id": 2, "product_id": 12},
      {"user_id": 10, "product_id": 88},
      {"user_id": 6, "product_id": 79},
      {"user_id": 4, "product_id": 20},
      {"user_id": 7, "product_id": 19},
      {"user_id": 3, "product_id": 13},
      {"user_id": 5, "product_id": 46},
      {"user_id": 8, "product_id": 79},
      {"user_id": 7, "product_id": 67},
      {"user_id": 10, "product_id": 95},
      {"user_id": 6, "product_id": 80},
      {"user_id": 3, "product_id": 39},
      {"user_id": 4, "product_id": 21},
      {"user_id": 1, "product_id": 19},
      {"user_id": 9, "product_id": 50},
      {"user_id": 4, "product_id": 81},
      {"user_id": 1, "product_id": 33},
      {"user_id": 3, "product_id": 73},
      {"user_id": 6, "product_id": 51},
      {"user_id": 3, "product_id": 21},
      {"user_id": 6, "product_id": 38},
      {"user_id": 1, "product_id": 51},
      {"user_id": 5, "product_id": 71},
      {"user_id": 7, "product_id": 23},
      {"user_id": 2, "product_id": 71},
      {"user_id": 10, "product_id": 55},
      {"user_id": 3, "product_id": 14},
      {"user_id": 8, "product_id": 41},
      {"user_id": 9, "product_id": 29},
      {"user_id": 4, "product_id": 50},
      {"user_id": 2, "product_id": 49},
      {"user_id": 7, "product_id": 63},
      {"user_id": 8, "product_id": 59},
      {"user_id": 11, "product_id": 11},
      {"user_id": 5, "product_id": 62},
      {"user_id": 6, "product_id": 24},
      {"user_id": 3, "product_id": 41},
      {"user_id": 11, "product_id": 85},
      {"user_id": 6, "product_id": 22},
      {"user_id": 4, "product_id": 11},
      {"user_id": 3, "product_id": 68},
      {"user_id": 10, "product_id": 22},
      {"user_id": 5, "product_id": 67},
      {"user_id": 1, "product_id": 57},
      {"user_id": 5, "product_id": 89},
      {"user_id": 2, "product_id": 71},
      {"user_id": 3, "product_id": 79},
      {"user_id": 7, "product_id": 69},
      {"user_id": 7, "product_id": 14},
      {"user_id": 2, "product_id": 37},
      {"user_id": 4, "product_id": 65},
      {"user_id": 8, "product_id": 86},
      {"user_id": 9, "product_id": 56},
      {"user_id": 6, "product_id": 30},
      {"user_id": 9, "product_id": 91},
      {"user_id": 3, "product_id": 89},
      {"user_id": 11, "product_id": 52},
      {"user_id": 4, "product_id": 13},
      {"user_id": 6, "product_id": 63},
      {"user_id": 12, "product_id": 69},
      {"user_id": 5, "product_id": 22},
      {"user_id": 7, "product_id": 11},
      {"user_id": 7, "product_id": 35},
      {"user_id": 9, "product_id": 64},
      {"user_id": 3, "product_id": 96},
      {"user_id": 9, "product_id": 63},
      {"user_id": 5, "product_id": 45},
      {"user_id": 10, "product_id": 103},
      {"user_id": 3, "product_id": 51},
      {"user_id": 5, "product_id": 74},
      {"user_id": 6, "product_id": 86},
      {"user_id": 12, "product_id": 108},
      {"user_id": 4, "product_id": 75},
      {"user_id": 4, "product_id": 45},
      {"user_id": 3, "product_id": 11}
    ]
  } 
      
    reviews_data = {
  "reviews": [
    {
      "rating": 5,
      "comment": "Un juego que siempre emociona. Cada vez que lo juego, descubro algo nuevo. La jugabilidad es excelente, y siempre te mantiene en tensión.",
      "user_id": 10,
      "product_id": 56
    },
    {
      "rating": 4,
      "comment": "Funciona bastante bien, aunque me gustaría que tuviera un poco más de durabilidad. Aun así, cumple con lo que prometen y es bastante útil.",
      "user_id": 2,
      "product_id": 100
    },
    {
      "rating": 4,
      "comment": "El producto tiene una calidad excelente, aunque la entrega tardó un poco más de lo esperado. De todos modos, el tiempo de espera valió la pena.",
      "user_id": 5,
      "product_id": 35
    },
    {
      "rating": 5,
      "comment": "La historia me atrapó desde el primer minuto. Una experiencia impresionante que sigue siendo relevante hoy en día. Todo en el juego es de altísima calidad.",
      "user_id": 1,
      "product_id": 18
    },
    {
      "rating": 4,
      "comment": "Los gráficos son impresionantes, y la jugabilidad es dinámica. Aunque algunos personajes adicionales hubieran sido geniales, el juego sigue siendo muy entretenido.",
      "user_id": 4,
      "product_id": 22
    },
    {
      "rating": 5,
      "comment": "Increíblemente hermoso. La historia te toca el corazón, y los gráficos son impresionantes. La atmósfera es perfecta para una experiencia inolvidable.",
      "user_id": 3,
      "product_id": 78
    },
    {
      "rating": 3,
      "comment": "Un clásico que no ha perdido su toque, pero las mecánicas pueden sentirse algo anticuadas si lo comparas con títulos más recientes.",
      "user_id": 10,
      "product_id": 66
    },
    {
      "rating": 4,
      "comment": "Aún siendo un dispositivo portátil antiguo, sigue ofreciendo una experiencia de juego encantadora. Ideal para nostálgicos y para disfrutar de los clásicos.",
      "user_id": 8,
      "product_id": 12
    },
    {
      "rating": 5,
      "comment": "La libertad de exploración es fantástica. Cada rincón del mundo está lleno de vida y sorpresas. Un imprescindible para cualquier amante de la aventura.",
      "user_id": 8,
      "product_id": 44
    },
    {
      "rating": 4,
      "comment": "Acción sin descanso y una jugabilidad fluida, aunque la dificultad puede ser algo elevada para los menos experimentados. Aún así, muy divertido.",
      "user_id": 6,
      "product_id": 78
    },
    {
      "rating": 3,
      "comment": "Un pedazo de historia en el mundo de los videojuegos, aunque al día de hoy se nota la limitación técnica si lo comparas con consolas modernas.",
      "user_id": 3,
      "product_id": 90
    },
    {
      "rating": 4,
      "comment": "Una obra maestra de la estrategia. La historia es fascinante, aunque la curva de aprendizaje puede ser algo empinada para los novatos del género.",
      "user_id": 9,
      "product_id": 33
    },
    {
      "rating": 5,
      "comment": "No hay nada mejor que tener más espacio. Este producto mejora significativamente la experiencia de juego, sin necesidad de preocuparte por el almacenamiento.",
      "user_id": 7,
      "product_id": 22
    },
    {
      "rating": 4,
      "comment": "Un mundo abierto impresionante, pero algunas misiones pueden sentirse algo repetitivas. Aún así, es un juego que te atrapa por su historia y su atmósfera.",
      "user_id": 8,
      "product_id": 77
    },
    {
      "rating": 5,
      "comment": "Una de las experiencias más profundas que he jugado. Las decisiones realmente impactan el curso de la historia, lo que hace que cada partida sea única.",
      "user_id": 9,
      "product_id": 45
    },
    {
      "rating": 4,
      "comment": "Excelente juego de terror, con una atmósfera única. Sin embargo, los puzzles pueden ser difíciles y algunos momentos pueden sentirse algo lentos.",
      "user_id": 6,
      "product_id": 90
    },
    {
      "rating": 5,
      "comment": "Sigue siendo uno de los mejores en su categoría. La jugabilidad sigue siendo sólida, y las expansiones aportan mucha más diversidad al juego.",
      "user_id": 4,
      "product_id": 56
    },
    {
      "rating": 4,
      "comment": "Un juego encantador, pero algunas tareas pueden sentirse repetitivas. Aun así, tiene algo adictivo que hace que quieras seguir jugando.",
      "user_id": 3,
      "product_id": 87
    },
    {
      "rating": 5,
      "comment": "Perfecta para los jugadores que buscan flexibilidad. La capacidad de jugar en cualquier lugar y la calidad de los juegos exclusivos son su mayor atractivo.",
      "user_id": 3,
      "product_id": 22
    },
    {
      "rating": 4,
      "comment": "Es una consola increíble, pero me gustaría ver más exclusivos que realmente hagan la diferencia. Sin embargo, sigue siendo una excelente opción para muchos juegos.",
      "user_id": 9,
      "product_id": 2
    },
    {
      "rating": 4,
      "comment": "Un clásico que sigue siendo tan entretenido hoy en día. Aunque los gráficos ya no son lo mejor, la historia sigue siendo increíble.",
      "user_id": 4,
      "product_id": 14
    },
    {
      "rating": 5,
      "comment": "Una experiencia de juego increíblemente adictiva. Cada vez que juegas, encuentras nuevos desafíos, y el diseño artístico es impecable.",
      "user_id": 8,
      "product_id": 89
    },
    {
      "rating": 4,
      "comment": "El dispositivo ofrece una experiencia increíble. Los juegos son muy envolventes, pero algunos aún necesitan optimización para alcanzar todo su potencial.",
      "user_id": 6,
      "product_id": 63
    },
    {
      "rating": 5,
      "comment": "Un juego fenomenal que te mantiene atrapado desde el primer minuto. El mundo abierto es vasto y lleno de sorpresas. Una joya de la industria.",
      "user_id": 7,
      "product_id": 54
    },
    {
      "rating": 4,
      "comment": "Un clásico que nunca pasa de moda. Aunque los controles pueden parecer simples, sigue siendo muy divertido y una excelente opción para los nostálgicos.",
      "user_id": 2,
      "product_id": 71
    }
  ]
}


    for i in favorites_data['favorites']:
            prod = Favorites()
            prod.user_id = i['user_id']
            prod.product_id = i['product_id']
            db.session.add(prod)
            db.session.commit()    
    for i in shopping_data['shopping_cart']:

            prod = ShoppingCart()
            prod.user_id = i['user_id']
            prod.product_id = i['product_id']
            db.session.add(prod)
            db.session.commit()  
    for i in reviews_data['reviews']:
            prod = Reviews()
            prod.rating = i['rating']
            prod.comment = i['comment']
            prod.user_id = i['user_id']
            prod.product_id = i['product_id']
            db.session.add(prod)
            db.session.commit()   
    return jsonify({'msg': 'ok'})      




@api.route('/dummy', methods=['POST'])
def insert_dummy():
        
        data = {
                "consoles":[ 
                        
                {
                    "name": "Nintendo Entertainment System (NES)",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528372/NES-Console-Set_z672gh-min_ks47w4.png",
                    "year": "1983",
                    "brand": "Nintendo",
                    "platform": "Nintendo",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nLa Nintendo Entertainment System (NES) fue la consola que revolucion\u00f3 el mundo de los videojuegos en la d\u00e9cada de los 80, marcando el inicio de una nueva era para Nintendo.\n\nCaracter\u00edsticas\n- Procesador de 8 bits\n- Biblioteca ic\u00f3nica con t\u00edtulos como Super Mario Bros y The Legend of Zelda\n- Dise\u00f1o compacto y resistente\n\nIdeal para\nColeccionistas y fan\u00e1ticos de los videojuegos retro que buscan revivir la nostalgia de los cl\u00e1sicos.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 149.00
                },
                {
                    "name": "Sega Master System",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528369/segamaster-sistem_zpjjlc-min_owwqp4.jpg",
                    "year": "1985",
                    "brand": "Sega",
                    "platform": "Sega Master System",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nLa Sega Master System es una consola cl\u00e1sica de 8 bits que ofreci\u00f3 una experiencia de juego alternativa frente a la competencia de la \u00e9poca.\n\nCaracter\u00edsticas\n- Gr\u00e1ficos avanzados para su generaci\u00f3n\n- Compatibilidad con juegos mediante tarjetas Sega\n- Incluye t\u00edtulos populares como Sonic y Alex Kidd\n\nIdeal para\nFans de Sega que quieran explorar las ra\u00edces de esta ic\u00f3nica marca.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 199.99
                },
                {
                    "name": "Atari 7800",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528369/1920px-Atari-7800-Console-Set_nqtvf5-min_ptdyho.jpg",
                    "year": "1986",
                    "brand": "Atari",
                    "platform": "Atari Corporation",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nEl Atari 7800 fue dise\u00f1ado para ofrecer compatibilidad retro con juegos de la 2600 y gr\u00e1ficos mejorados para los nuevos t\u00edtulos.\n\nCaracter\u00edsticas\n- Compatibilidad con m\u00e1s de 500 juegos del Atari 2600\n- Mejores capacidades gr\u00e1ficas y de sonido frente a su predecesor\n- Dise\u00f1o robusto y compacto\n\nIdeal para\nAmantes de los videojuegos cl\u00e1sicos que buscan una consola retro con una amplia biblioteca de juegos.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 140.00
                },
                {
                    "name": "Game & Watch",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528565/Game-and-watch-ball_veid2n-min_zvywkx.png",
                    "year": "1980",
                    "brand": "Nintendo",
                    "platform": "Game & Watch",
                    "type": "Portable",
                    "category":"consolas",
                    "description": "\nEl Game & Watch de Nintendo es una serie de consolas port\u00e1tiles con pantalla LCD que introdujeron el concepto de juegos port\u00e1tiles.\n\nCaracter\u00edsticas\n- Pantalla LCD monocrom\u00e1tica\n- Dise\u00f1o ligero y port\u00e1til\n- Juegos integrados espec\u00edficos para cada modelo\n\nIdeal para\nColeccionistas y fan\u00e1ticos de los primeros pasos de Nintendo en el mundo de los videojuegos.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 40.00
                },
                {
                    "name": "Super Nintendo Entertainment System (SNES)",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528369/SNES-Mod1-Console-Set_upozmm-min_a8xdub.jpg",
                    "year": "1990",
                    "brand": "Nintendo",
                    "platform": "Nintendo",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nLa Super Nintendo Entertainment System (SNES) es una consola de 16 bits que consolid\u00f3 el liderazgo de Nintendo en los videojuegos.\n\nCaracter\u00edsticas\n- Biblioteca ic\u00f3nica con juegos como Super Mario World y The Legend of Zelda: A Link to the Past\n- Procesador de 16 bits para gr\u00e1ficos y sonido avanzados\n- Dise\u00f1o ergon\u00f3mico de los controles\n\nIdeal para\nAmantes de los videojuegos retro que buscan revivir los a\u00f1os dorados de los 90.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 199.00
                },
                {
                    "name": "PlayStation (PS1)",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528368/PlayStation-SCPH-1000-with-Controller_eolbsi-min_pdpvbk.jpg",
                    "year": "1994",
                    "brand": "Sony",
                    "platform": "PlayStation",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nLa primera PlayStation marc\u00f3 el ingreso triunfal de Sony al mundo de las consolas de videojuegos, cambiando para siempre la industria.\n\nCaracter\u00edsticas\n- Juegos en CD con capacidad para videos y audio de alta calidad\n- Biblioteca extensa con cl\u00e1sicos como Final Fantasy VII y Metal Gear Solid\n- Primer control con sticks anal\u00f3gicos opcionales\n\nIdeal para\nJugadores que buscan experimentar los t\u00edtulos revolucionarios de los a\u00f1os 90.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 180.50
                },
                {
                    "name": "Nintendo 64",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528372/1920px-Nintendo-64-wController-L_fbcwaa-min_rpc91j.jpg",
                    "year": "1996",
                    "brand": "Nintendo",
                    "platform": "Nintendo",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nLa Nintendo 64 fue la primera consola de Nintendo en ofrecer gr\u00e1ficos en 3D, llevando los videojuegos a una nueva dimens\u00edn.\n\nCaracter\u00edsticas\n- Gr\u00e1ficos en 3D y soporte para cuatro jugadores\n- Juegos ic\u00f3nicos como Super Mario 64, The Legend of Zelda: Ocarina of Time y GoldenEye 007\n- Control con stick anal\u00f3gico y gatillo Z\n\nIdeal para\nAquellos que buscan revivir las innovaciones de los videojuegos de los 90.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 160.50
                },
                {
                    "name": "Game Boy",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528372/1920px-Nintendo-64-wController-L_fbcwaa-min_rpc91j.jpg",
                    "year": "1989",
                    "brand": "Nintendo",
                    "platform": "Nintendo",
                    "type": "Portable",
                    "category":"consolas",
                    "description": "\nLa Game Boy fue la primera consola portátil de Nintendo, marcando el comienzo de una nueva era en los videojuegos móviles.\n\nCaracterísticas\n- Pantalla monocromática\n- Jueguetes como Tetris, Super Mario Land y Pokémon\n- Batería de larga duración\n\nIdeal para\nColeccionistas de consolas portátiles y aquellos que disfrutan de los primeros juegos de Pokémon.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 30.00
                },
                {
                    "name": "Sega Saturn",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528369/Sega-Saturn-Console-Set-Mk2_je8f1k-min_llzsbr.png",
                    "year": "1994",
                    "brand": "Sega",
                    "platform": "Sega",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nLa Sega Saturn fue una consola de 32 bits, famosa por su potencia gráfica y su capacidad para manejar juegos en 2D y 3D.\n\nCaracterísticas\n- Potente procesador y gráficos en 2D y 3D\n- Incluye títulos como Virtua Fighter, Nights into Dreams\n- Amplia biblioteca de juegos\n\nIdeal para\nColeccionistas y fanáticos de las consolas de Sega.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 150.50
                },
                {
                    "name": "PlayStation 2",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528368/PS2-Versions_zzhjnh-min_nufx4o.jpg",
                    "year": "2000",
                    "brand": "Sony",
                    "platform": "PlayStation 2",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nLa PlayStation 2 es una de las consolas más exitosas de todos los tiempos, conocida por su enorme biblioteca de juegos.\n\nCaracterísticas\n- Procesador de 128 bits\n- Compatibilidad con DVDs y juegos clásicos de PS1\n- Títulos icónicos como Grand Theft Auto, Final Fantasy X\n\nIdeal para\nJugadores que buscan disfrutar de los mejores títulos de los años 2000.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 120.00
                },
                {
                    "name": "Nintendo GameCube",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528372/GameCube-Set_vokzkr-min_zu98ho.jpg",
                    "year": "2001",
                    "brand": "Nintendo",
                    "platform": "Nintendo GameCube",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nLa Nintendo GameCube es una consola que destacó por sus juegos exclusivos y su diseño compacto.\n\nCaracterísticas\n- Juegos como Super Smash Bros. Melee y The Legend of Zelda: The Wind Waker\n- Procesador PowerPC Gekko\n- Soporte para cuatro controles\n\nIdeal para\nFans de Nintendo que quieren revivir una consola muy querida.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 90.00
                },
                {
                    "name": "Game Boy Advance",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528367/Nintendo-Game-Boy-Advance-Purple-FL_yfp2ph-min_hs1ip1.jpg",
                    "year": "2001",
                    "brand": "Nintendo",
                    "platform": "Nintendo",
                    "type": "Portable",
                    "category":"consolas",
                    "description": "\nEl Game Boy Advance ofrece una gran biblioteca de juegos en 2D en una pantalla retroiluminada.\n\nCaracterísticas\n- Pantalla a color de 2.9 pulgadas\n- Juegos populares como Pokémon Ruby/Sapphire, Metroid Fusion\n- Batería de larga duración\n\nIdeal para\nFans de los juegos portátiles y los títulos clásicos de Nintendo.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 60.00
                },
                {
                    "name": "Nintendo DS",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528368/Nintendo-DS-Fat-Blue_b9dl11-min_uqvgad.jpg",
                    "year": "2004",
                    "brand": "Nintendo",
                    "category":"consolas",
                    "description": "\nLa Nintendo DS es una consola portátil con dos pantallas, una de ellas táctil. Fue una de las primeras en incorporar el control táctil como mecanismo de interacción en los juegos.\n\nCaracterísticas\n- Pantalla táctil dual\n- Juegos como Mario Kart DS y The Legend of Zelda: Phantom Hourglass\n- Conectividad Wi-Fi\n\nIdeal para\nJugadores que buscan una experiencia portátil innovadora y una gran variedad de juegos.",
                    "platform": "",
                    "type": "Portable",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 79.99
                },
                {
                    "name": "PlayStation Portable (PSP)",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528369/Sony-PSP-1000-Body_b66nxd-min_dibzyl.png",
                    "year": "2004",
                    "brand": "Sony",
                    "category":"consolas",
                    "description": "\nLa PSP fue una consola portátil de Sony que revolucionó el mercado, destacando por sus gráficos de alta calidad y su capacidad multimedia.\n\nCaracterísticas\n- Pantalla LCD de 4.3 pulgadas\n- Reproducción de video y música\n- Conectividad Wi-Fi\n\nIdeal para\nJugadores que buscan una consola portátil para juegos en 3D y entretenimiento multimedia.",
                    "platform": "",
                    "type": "Portable",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 100.00
                },
                {
                    "name": "Xbox 360",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528370/Xbox-360-Pro-wController_mgdupa-min_lluue2.jpg",
                    "year": "2005",
                    "brand": "Microsoft",
                    "category":"consolas",
                    "description": "\nLa Xbox 360 fue una consola de nueva generación, destacando por sus potentes gráficos y su integración con Xbox Live para el juego en línea.\n\nCaracterísticas\n- Soporte para HD 1080p\n- Amplia librería de juegos exclusivos\n- Xbox Live para juego en línea\n\nIdeal para\nJugadores que buscan una experiencia de juego fluida y la mejor calidad en juegos en línea.",
                    "platform": "",
                    "type": "Portable",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 110.00,
                    "seller_id": 4
                },
                {
                    "name": "PlayStation 3",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528368/PS3-slim-console_mevjhi-min_dpieo2.png",
                    "year": "2006",
                    "brand": "Sony",
                    "category":"consolas",
                    "description": "\nLa PS3 fue una consola de nueva generación que ofreció gráficos impresionantes y la capacidad de reproducir discos Blu-ray, posicionándose como un centro de entretenimiento.\n\nCaracterísticas\n- Soporte para Blu-ray\n- Gráficos de alta definición\n- Juegos como Uncharted y The Last of Us\n\nIdeal para\nJugadores que buscan una consola potente con un excelente catálogo de juegos exclusivos.",
                    "platform": "",
                    "type": "Sobremesa",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 130.00
                },
                {
                    "name": "Nintendo Wii",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528369/1200px-Wii-console_kttpqx-min_uh1jat.jpg",
                    "year": "2006",
                    "brand": "Nintendo",
                    "category":"consolas",
                    "description": "\nLa Wii fue una consola que revolucionó el mercado con su control de movimiento, permitiendo una experiencia de juego completamente nueva.\n\nCaracterísticas\n- Control de movimiento Wii Remote\n- Juegos como Super Mario Galaxy y The Legend of Zelda: Twilight Princess\n- Interfaz sencilla y accesible\n\nIdeal para\nJugadores casuales y familias que buscan diversión interactiva y fácil acceso a los juegos.",
                    "platform": "",
                    "type": "Sobremesa",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 70.00
                },
                {
                    "name": "PlayStation VR",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528372/Playstation_VR2-min_o7uyc4.jpg",
                    "year": "2016",
                    "brand": "Sony",
                    "category":"consolas",
                    "description": "\nPlayStation VR es el sistema de realidad virtual de Sony para PlayStation 4, ofreciendo una experiencia inmersiva con una amplia gama de juegos exclusivos.\n\nCaracterísticas\n- Compatible con PlayStation 4\n- Juegos como Resident Evil 7 y Beat Saber\n- Pantalla OLED y seguimiento de movimiento\n\nIdeal para\nJugadores que buscan una experiencia de realidad virtual accesible en consolas.",
                    "platform": "PlayStation VR",
                    "type": "Portable",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 250.00
                },
                {
                    "name": "Oculus Rift",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528374/Oculus-Rift-CV1-Headset-Front_with_transparent_background_z4yjjv-min_tutz0b.png",
                    "year": "2016",
                    "brand": "Meta Platforms",
                    "category":"consolas",
                    "description": "\nEl Oculus Rift es uno de los pioneros en el mercado de la realidad virtual, ofreciendo una experiencia inmersiva en PC.\n\nCaracterísticas\n- Resolución 1080x1200\n- Juegos y aplicaciones de VR compatibles\n- Requiere PC para funcionamiento\n\nIdeal para\nEntusiastas de la realidad virtual que buscan un dispositivo avanzado para PC.",
                    "platform": "Oculus VR",
                    "type": "Portable",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 530.00
                },
                {
                    "name": "Playstation 4",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528368/PS4-Console-wDS4_vpu1mn-min_jmm8yh.jpg",
                    "year": "2013",
                    "brand": "Sony",
                    "category":"consolas",
                    "description": "\nLa PS4 es la consola que definió la nueva generación de Sony, ofreciendo un potente rendimiento gráfico y un catálogo de juegos exclusivos.\n\nCaracterísticas\n- Juegos como The Last of Us Part II y God of War\n- Soporte para streaming y multimedia\n- Conectividad online mejorada\n\nIdeal para\nJugadores que buscan una experiencia de juego increíble con una amplia selección de títulos exclusivos.",
                    "platform": "PlayStation 4",
                    "type": "Sobremesa",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 399.99
                },
                {
                    "name": "Xbox One",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528372/2880px-Microsoft-Xbox-One-S-Console-FL_llmazk-min_cdhizu.jpg",
                    "year": "2013",
                    "brand": "Microsoft",
                    "category":"consolas",
                    "description": "\nLa Xbox One de Microsoft fue un avance en los juegos, con un potente rendimiento y la integración de entretenimiento multimedia en una sola consola.\n\nCaracterísticas\n- Juegos como Halo 5 y Gears of War 4\n- Integración con Xbox Live y servicios multimedia\n- Compatibilidad con juegos de generaciones anteriores\n\nIdeal para\nJugadores que desean un sistema todo-en-uno para juegos y entretenimiento.",
                    "platform": "Xbox One",
                    "type": "Sobremesa",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 499.00
                },
                {
                    "name": "Nintendo Switch",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528372/Nintendo-Switch-Console-Docked-wJoyConRB_lyfkw1-min_kl40g5.jpg",
                    "year": "2017",
                    "brand": "Nintendo",
                    "category":"consolas",
                    "description": "\nLa Nintendo Switch es una consola híbrida que puede ser usada como portátil o como consola de sobremesa, ofreciendo gran versatilidad y una excelente librería de juegos.\n\nCaracterísticas\n- Juegos como The Legend of Zelda: Breath of the Wild y Super Mario Odyssey\n- Pantalla táctil de 6.2 pulgadas\n- Modo de juego portátil y en el hogar\n\nIdeal para\nJugadores que buscan una consola flexible, adecuada tanto para jugar en casa como sobre la marcha.",
                    "platform": "Nintendo Switch",
                    "type": "Hibrida",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 329.50
                },
                {
                    "name": "Nintendo 3DS",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528372/Nintendo-3DS-AquaOpen_vib6fh-min_uxyt6a.png",
                    "year": "2011",
                    "brand": "Nintendo",
                    "category":"consolas",
                    "description": "\nLa Nintendo 3DS introdujo una pantalla 3D sin gafas, junto con una potente librería de juegos y la compatibilidad con títulos clásicos de DS.\n\nCaracterísticas\n- Pantalla superior 3D\n- Juegos como Mario Kart 7 y Animal Crossing: New Leaf\n- Cámara 3D\n\nIdeal para\nFanáticos de Nintendo que buscan una experiencia de juego portátil innovadora con tecnología 3D.",
                    "platform": "Nintendo 3DS",
                    "type": "Sobremesa",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 219.00
                },
                {
                    "name": "Wii U",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528369/Wii_U_Console_and_Gamepad_muqqhh-min_qkdma3.png",
                    "year": "2012",
                    "brand": "Nintendo",
                    "platform": "Nintendo Wii U",
                    "type": "Hibrida",
                    "category":"consolas",
                    "description": "\nLa Wii U es una consola híbrida que permite jugar tanto en el televisor como en su GamePad, una pantalla táctil independiente.\n\nCaracterísticas\n- Juego en la televisión y en pantalla táctil\n- Juegos como Super Mario 3D World y The Legend of Zelda: The Wind Waker HD\n- Retrocompatibilidad con juegos de Wii\n\nIdeal para\nJugadores que buscan una consola versátil, con la posibilidad de jugar tanto de forma tradicional como portátil.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 349.00
                },
                {
                    "name": "Playstation VR2",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528372/Playstation_VR2-min_o7uyc4.jpg",
                    "year": "2023",
                    "brand": "Sony",
                    "platform": "PlayStation VR2",
                    "type": "Portable",
                    "category":"consolas",
                    "description": "\nEl PlayStation VR2 ofrece una experiencia de realidad virtual más inmersiva para PlayStation 5, con un rendimiento gráfico mejorado y controles innovadores.\n\nCaracterísticas\n- Pantalla OLED 4K HDR\n- Sensores avanzados para inmersión total\n- Compatible con PlayStation 5\n\nIdeal para\nJugadores que buscan una experiencia de realidad virtual de nueva generación con gráficos impresionantes y una jugabilidad envolvente.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 599.99
                },
                {
                    "name": "Meta Quest 3",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528369/alquiler-meta-quest-3-min_mjesvo.jpg",
                    "year": "2023",
                    "brand": "Meta",
                    "platform": "Meta Quest 3",
                    "type": "Portable",
                    "category":"consolas",
                    "description": "\nMeta Quest 3 es un sistema de realidad virtual independiente que no necesita un PC o consola para funcionar, ofreciendo una experiencia inmersiva con gráficos mejorados y mayor comodidad.\n\nCaracterísticas\n- Resolución mejorada y pantallas de alta calidad\n- Juega sin cables ni dispositivos adicionales\n- Gran variedad de títulos en VR\n\nIdeal para\nEntusiastas de la VR que buscan un sistema todo-en-uno fácil de usar y de alta calidad, sin necesidad de conectarse a otros dispositivos.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 569.99
                },
                {
                    "name": "PlayStation 5 Pro",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528369/ps5-min_jeed44.png",
                    "year": "2024",
                    "brand": "Sony",
                    "platform": "PlatStation 5 Pro",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nLa PlayStation 5 Pro es la versión mejorada de la PlayStation 5, con un mayor rendimiento gráfico, soporte para 8K y nuevas funciones para mejorar la experiencia de juego.\n\nCaracterísticas\n- Potente rendimiento gráfico en 8K\n- Juegos exclusivos de alta calidad\n- Mejoras en la velocidad de carga y en la experiencia de juego\n\nIdeal para\nJugadores que buscan una consola de nueva generación con el mejor rendimiento y una experiencia visual de vanguardia.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 690.50
                },
                {
                    "name": "Xbox Series X",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528371/consola-xbox-series-x-digital-edition-1tb-min_dclzwr.jpg",
                    "year": "2020",
                    "brand": "Microsoft",
                    "platform": "Xbox Series X",
                    "type": "Sobremesa",
                    "category":"consolas",
                    "description": "\nLa Xbox Series X es la consola más poderosa de Microsoft, con un rendimiento gráfico increíble y tiempos de carga ultrarrápidos, ideal para juegos de última generación.\n\nCaracterísticas\n- Soporte para 4K y hasta 120 FPS\n- Amplia biblioteca de juegos exclusivos\n- Compatible con juegos de Xbox One y Xbox 360\n\nIdeal para\nJugadores que buscan una experiencia de juego rápida, fluida y con gráficos excepcionales.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 499.00
                },
                {
                    "name": "Steam Deck",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528370/Steam-Deck-OLED-blanco-001_l-min_mhxvfy.jpg",
                    "year": "2022",
                    "brand": "Valve",
                    "platform": "Steam Deck",
                    "type": "Portable",
                    "category":"consolas",
                    "description": "\nEl Steam Deck es una consola portátil que te permite jugar a la mayoría de tus juegos de PC desde Steam en cualquier lugar, con una interfaz intuitiva y controles cómodos.\n\nCaracterísticas\n- Gran compatibilidad con juegos de Steam\n- Pantalla táctil y controles de alta calidad\n- Soporte para juegos AAA y títulos indie\n\nIdeal para\nJugadores que buscan una experiencia de juegos de PC portátil, sin comprometer el rendimiento o la calidad gráfica.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 419.00
                },
                {
                    "name": "Nintendo Switch OLED",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738531388/HEG-S-KABAA_Switch_OLED_7__azul-rojo_Joy-Con_64_GB_mhbjud.jpg",
                    "year": "2021",
                    "brand": "Nintendo",
                    "platform": "Nintendo Switch",
                    "type": "Hibrida",
                    "category":"consolas",
                    "description": "\nLa Nintendo Switch OLED es una versión mejorada de la consola híbrida Nintendo Switch, con una pantalla OLED más vibrante y otras mejoras en el diseño.\n\nCaracterísticas\n- Pantalla OLED de 7 pulgadas\n- Juegos como Super Mario Odyssey y The Legend of Zelda: Breath of the Wild\n- Modo portátil y en casa\n\nIdeal para\nJugadores que buscan una consola híbrida con una pantalla de calidad superior para juegos tanto en casa como sobre la marcha.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 349.99
                },
                {
                    "name": "Pico 4",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738531388/HEG-S-KABAA_Switch_OLED_7__azul-rojo_Joy-Con_64_GB_mhbjud.jpg",
                    "year": "2022",
                    "brand": "Pico Interactive",
                    "platform": "Pico 4",
                    "type": "VR",
                    "category":"consolas",
                    "description": "\nPico 4 es un dispositivo de realidad virtual autónomo que no requiere conexión a un PC, con una excelente calidad gráfica y una amplia variedad de títulos VR.\n\nCaracterísticas\n- Resolución de 4K\n- Seguimiento avanzado de la cabeza y los ojos\n- Amplia biblioteca de juegos VR\n\nIdeal para\nUsuarios que buscan un sistema VR independiente, con gráficos de alta calidad y facilidad de uso.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 429.50
                },
                {
                    "name": "ROG Ally",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738528371/71SzrV6I5-L-min_ys2atq.jpg",
                    "year": "2023",
                    "brand": "ASUS",
                    "platform": "ROG Ally",
                    "type": "Portable",
                    "category":"consolas",
                    "description": "\nEl ROG Ally es una consola portátil de ASUS que permite jugar a los juegos de PC de manera portátil con un potente rendimiento gráfico y un diseño ergonómico.\n\nCaracterísticas\n- Pantalla de alta tasa de refresco\n- Compatible con juegos de PC y Steam\n- Gran rendimiento en juegos AAA\n\nIdeal para\nJugadores que buscan una consola portátil potente, capaz de manejar juegos de PC en cualquier lugar.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 799.00
                }      



                ],
                "videogames":[ 
                {
                    "name": "Metal Gear Solid",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529839/Metal_Gear_Solid_cover_art_ieem5w-min_bbyyyn.png",
                    "year": "1998",
                    "brand": "Konami",
                    "platform": "PlayStation",
                    "type": "Accion",
                    "category":"videojuegos",
                    "description": "\nMetal Gear Solid es un innovador juego de sigilo que revolucionó el género, con una narrativa cinematográfica que sumergió a los jugadores en una historia de espionaje y traición.\n\nCaracterísticas\n- Juego de sigilo con mecánicas complejas\n- Personajes memorables y trama profunda\n- Gráficos avanzados para su época\n\nIdeal para\nAquellos que disfrutan de juegos de sigilo con una narrativa inmersiva y profunda.",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 24.99
                },
                {
                    "name": "Grand Theft Auto: Vice City",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529841/1200px-GTAViceCityBoxArtwork_c5gnxa-min_sqipw6.jpg",
                    "year": "2002",
                    "brand": "Rockstar Games",
                    "platform": "PlayStation 2",
                    "type": "Accion",
                    "category":"videojuegos",
                    "description": "\nGrand Theft Auto: Vice City es un juego de mundo abierto que transporta a los jugadores a los años 80, con una atmósfera vibrante y una historia llena de acción y crimen.\n\nCaracterísticas\n- Mundo abierto con libertad total para explorar\n- Banda sonora icónica de los 80\n- Historia profunda y personajes memorables\n\nIdeal para\nJugadores que disfrutan de la acción, el crimen y una narrativa clásica ambientada en los años 80.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 20.50
                },
                {
                    "name": "God of War II",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529849/God_of_War_II_cover_bbe38d-min_x8stxc.jpg",
                    "year": "2007",
                    "brand": "Santa Monica Studio",
                    "platform": "PlayStation 2",
                    "type": "Accion",
                    "category":"videojuegos",
                    "description": "\nGod of War II es un juego de acción mitológica donde Kratos, el dios de la guerra, se enfrenta a los dioses del Olimpo. Con combates épicos y una narrativa que mantiene a los jugadores al borde de sus asientos.\n\nCaracterísticas\n- Combate brutal y espectacular\n- Historia basada en la mitología griega\n- Gráficos avanzados para la PlayStation 2\n\nIdeal para\nFans de la mitología y la acción intensa, que buscan un desafío en su experiencia de juego.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 15.00
                },
                {
                    "name": "Uncharted 2: Among Thieves",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529849/among_thieves-min_dsjvdh.jpg",
                    "year": "2009",
                    "brand": "Naughty Dog",
                    "platform": "PlayStation 3",
                    "type": "Accion",
                    "category":"videojuegos",
                    "description": "\nUncharted 2: Among Thieves es un juego de acción y aventuras que sigue al cazador de tesoros Nathan Drake. Con gráficos espectaculares y una narrativa inmersiva, los jugadores se embarcan en una peligrosa búsqueda a través del mundo.\n\nCaracterísticas\n- Gráficos impresionantes para la época\n- Historia cautivadora con giros inesperados\n- Secuencias de acción de alto nivel\n\nIdeal para\nJugadores que buscan una aventura épica llena de acción y misterio, con una historia intrigante.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 10.00
                },
                {
                    "name": "Dark Souls",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529852/dark_souls-min_yfatdv.jpg",
                    "year": "2011",
                    "brand": "FromSoftware",
                    "platform": "PlayStation 3",
                    "type": "Accion",
                    "category":"videojuegos",
                    "description": "\nDark Souls es un RPG desafiante que ofrece una experiencia de juego única con un combate profundo y un mundo interconectado lleno de peligros. Conocido por su dificultad y su atmósfera oscura.\n\nCaracterísticas\n- Mundo interconectado y sin interrupciones\n- Desafío de combate con una curva de dificultad elevada\n- Narrativa ambiental que el jugador debe descubrir\n\nIdeal para\nJugadores que buscan un desafío intenso y disfrutan de explorar un mundo sombrío lleno de misterios.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 15.00
                },
                {
                    "name": "The Last of Us",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529847/images_v9cec2-min_xsaufs.jpg",
                    "year": "2013",
                    "brand": "Naughty Dog",
                    "platform": "PlayStation 3",
                    "type": "Accion",
                    "category":"videojuegos",
                    "description": "\nThe Last of Us es un juego de supervivencia que sigue la historia de Joel y Ellie mientras navegan por un mundo postapocalíptico. Con una narrativa emocional, es uno de los títulos más aclamados de la PlayStation 3.\n\nCaracterísticas\n- Historia profundamente emocional\n- Mundo postapocalíptico inmersivo\n- Jugabilidad de supervivencia tensa\n\nIdeal para\nJugadores que disfrutan de una narrativa emocionalmente cargada y una jugabilidad de supervivencia desafiante.",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 14.99
                },
                {
                    "name": "Doom Eternal",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529843/doom-eternal-box-image_okyq4z-min_vozucc.jpg",
                    "year": "2020",
                    "brand": "Bethesda Softworks",
                    "platform": "PC",
                    "type": "Accion",
                    "category":"videojuegos",
                    "description": "\nDoom Eternal es la continuación de la famosa franquicia de disparos en primera persona. Este título ofrece una jugabilidad frenética, combates intensos y una experiencia visual impresionante.\n\nCaracterísticas\n- Acción ininterrumpida y combates rápidos\n- Gráficos impresionantes con diseño detallado\n- Desafío alto para jugadores experimentados\n\nIdeal para\nJugadores que disfrutan de la acción sin descanso y de un desafío continuo en un mundo apocalíptico.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 9.99
                },
                {
                    "name": "The Legend of Zelda",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529841/81U-DS7w_CL_wlrzxo-min_dhdfx8.jpg",
                    "year": "1986",
                    "brand": "Nintendo",
                    "platform": "Nintendo",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nThe Legend of Zelda es un clásico juego de aventura que introdujo a los jugadores en un mundo de fantasía lleno de exploración, acertijos y batallas épicas. Este título es considerado un pilar en la historia de los videojuegos.\n\nCaracterísticas\n- Introducción a la fórmula de exploración y aventura\n- Mundo abierto con mazmorras y secretos\n- Jugabilidad innovadora para su época\n\nIdeal para\nAquellos que quieren experimentar uno de los videojuegos más influyentes de la historia y explorar sus orígenes.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 4.99
                },
                {
                    "name": "Monkey Island 2: LeChuck’s Revenge",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529848/LeChuck_s_Revenge_artwork_drrdzz-min_snjukt.jpg",
                    "year": "1991",
                    "brand": "LucasArts",
                    "platform": "PC",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nMonkey Island 2: LeChuck's Revenge es una aventura gráfica que sigue las desventuras de Guybrush Threepwood, un aspirante a pirata que se enfrenta a su mayor enemigo: el temido pirata LeChuck.\n\nCaracterísticas\n- Aventura gráfica con puzzles ingeniosos\n- Humor único y personajes memorables\n- Mundo colorido y bien diseñado\n\nIdeal para\nFans de las aventuras gráficas clásicas con humor, rompecabezas desafiantes y personajes carismáticos.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 2.50
                },
                {
                    "name": "Shadow of the Colossus",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529841/4317156-shadow-of-the-colossus-playstation-2-front-cover_gfq11c-min_fkp69n.jpg",
                    "year": "2005",
                    "brand": "Sony Computer Entertainment",
                    "platform": "PlayStation 2",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nShadow of the Colossus es un juego de acción y aventura donde los jugadores deben derrotar a gigantes colosos para revivir a una joven mujer. Su mundo vasto y vacío está lleno de belleza y misterio.\n\nCaracterísticas\n- Batallas épicas contra gigantes\n- Mundo abierto impresionante y atmosférico\n- Historia mínima pero profunda\n\nIdeal para\nJugadores que buscan una experiencia única con un enfoque en la belleza visual y desafíos masivos.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 10.00
                },
                {
                    "name": "Journey",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529841/81kyHuFWLRL._SL1500__uumdzo-min_no50lh.jpg",
                    "year": "2012",
                    "brand": "Thatgamecompany",
                    "platform": "PlayStation 3",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nJourney es una experiencia única de aventura interactiva, donde los jugadores exploran un vasto desierto en busca de la cima de una montaña. Con un enfoque en la interacción emocional y el descubrimiento, es una obra maestra visual y sonora.\n\nCaracterísticas\n- Gráficos impresionantes y música evocadora\n- Juego multijugador asimétrico sin palabras\n- Enfoque en la exploración y la conexión emocional\n\nIdeal para\nJugadores que buscan una experiencia introspectiva y emocionalmente rica, donde la narrativa se construye a través de la experiencia compartida.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 15.00
                },
                {
                    "name": "The Legend of Zelda: Tears of the Kingdom",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738531978/totkj_jijdff.jpg", 
                    "year": "2023",
                    "brand": "Nintendo",
                    "platform": "Nintendo Switch",
                    "type": "Aventura",
                    "category": "videojuegos",
                    "description": "\nTears of the Kingdom es un juego de aventura de mundo abierto que lleva la experiencia de Zelda a nuevos niveles, con una narrativa épica, nuevas mecánicas de exploración y una gran expansión del mundo conocido de Hyrule.\n\nCaracterísticas\n- Mundo abierto con nuevas formas de exploración como el vuelo y la manipulación de objetos\n- Combate mejorado con habilidades y poderes únicos\n- Gráficos impresionantes y un mundo aún más detallado\n\nIdeal para\nJugadores que buscan una experiencia profunda, un mundo expansivo para explorar, y una historia emocionante llena de misterio y aventura.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 59.50
                },
                {
                "name": "Cult of the Lamb",
                "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738532217/878840117929_ey2g3u.jpg",
                "year": "2022",
                "brand": "Devolver Digital",
                "platform": "Nintendo Switch",
                "type": "Indie",
                "category": "videojuegos",
                "description": "\nCult of the Lamb es un juego de acción y gestión donde lideras un culto en un mundo oscuro y encantador. Explora mazmorras, recluta seguidores y construye tu comunidad mientras enfrentas amenazas místicas.\n\nCaracterísticas\n- Mezcla de acción roguelike y gestión de recursos\n- Estética única con un tono oscuro y adorable\n- Personalización de tu culto y decisiones estratégicas\n\nIdeal para\nJugadores que disfrutan de experiencias únicas, con un balance entre combate desafiante y construcción de comunidad.",
                "stock": 1,
                "state": True,
                "promoted": True,
                "price": 24.99
                },
                {
                "name": "Hogwarts Legacy",
                "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738532218/714QOvdGrBL_isq92d.jpg",
                "year": "2023",
                "brand": "Warner Bros. Games",
                "platform": "Nintendo Switch",
                "type": "RPG, Aventura",
                "category": "videojuegos",
                "description": "\nHogwarts Legacy es un RPG de mundo abierto ambientado en el universo de Harry Potter. Vive tu propia aventura en el siglo XIX, explora Hogwarts y aprende magia mientras enfrentas misterios y criaturas mágicas.\n\nCaracterísticas\n- Mundo abierto con Hogwarts, Hogsmeade y más\n- Personalización de personaje y clases de magia\n- Historia original ambientada en el universo de Harry Potter\n\nIdeal para\nFans de Harry Potter y jugadores que buscan una experiencia inmersiva en un RPG mágico lleno de exploración y aventura.",
                "stock": 1,
                "state": True,
                "promoted": True,
                "price": 59.99
                },
                {
                    "name": "Life is Strange",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529852/life_is_strange-3561963_dujjqi-min_ee48el.jpg",
                    "year": "2015",
                    "brand": "Dontnod Entertainment & Square Enix",
                    "platform": "PC",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nLife is Strange es un juego de aventura interactivo que sigue a Max Caulfield, una joven con la habilidad de retroceder en el tiempo. El juego explora temas de amistad, destino y consecuencias.\n\nCaracterísticas\n- Historia emocional y de decisiones\n- Mecánica de retroceder el tiempo\n- Personajes bien desarrollados y conmovedores\n\nIdeal para\nJugadores que disfrutan de una narrativa emocional con decisiones significativas que afectan el curso de la historia.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 20.00
                },
                {
                    "name": "Disco Elysium",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529847/producto-disco-elysium-ps4-1145_xonio4-min_huttkq.jpg",
                    "year": "2019",
                    "brand": "ZA/UM",
                    "platform": "PC",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nDisco Elysium es un RPG de aventura interactiva con un enfoque en la narrativa, donde los jugadores toman el rol de un detective con amnesia mientras investigan un crimen. El juego está lleno de diálogos profundos y decisiones que afectan al mundo y a los personajes.\n\nCaracterísticas\n- Narrativa profunda y diálogos extensos\n- Sistema de habilidades único que afecta las interacciones\n- Exploración y resolución de misterios\n\nIdeal para\nJugadores que disfrutan de una historia profunda, decisiones que importan y una jugabilidad centrada en el diálogo y la interacción.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 20.00
                },
                {
                    "name": "Metroid Prime Remastered",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529841/71HNuRb_orL._AC_UF894_1000_QL80__oqoxxo-min_ebeeo8.jpg",
                    "year": "2023",
                    "brand": "Nintendo",
                    "platform": "Nintendo Switch",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nMetroid Prime Remastered es una versión remasterizada del clásico juego de acción y exploración. Los jugadores toman el control de Samus Aran en una misión para explorar un planeta alienígena lleno de misterios y peligros.\n\nCaracterísticas\n- Gráficos remasterizados y gameplay mejorado\n- Elementos clásicos de la serie Metroid\n- Exploración y combate intensos\n\nIdeal para\nFans de los juegos de acción y aventura, especialmente aquellos que disfrutaron de las entregas clásicas de Metroid.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 39.99
                },
                {
                    "name": "Final Fantasy VII Remake",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738532537/81W8CAno24L_vqulry.jpg",
                    "year": "2019",
                    "brand": "Square Enix",
                    "platform": "PlayStation 5",
                    "type": "RPG",
                    "category":"videojuegos",
                    "description": "\nFinal Fantasy VII Remake es una versión moderna y rediseñada del clásico RPG de 1997, con gráficos de última generación y un sistema de combate actualizado. La historia sigue a Cloud Strife mientras lucha contra la megacorporación Shinra y sus peligrosos planes para el planeta.\n\nCaracterísticas\n- Gráficos impresionantes y personajes detallados\n- Combate en tiempo real combinado con elementos tácticos\n- Profunda historia con giros emocionales\n\nIdeal para\nJugadores que buscan revivir uno de los RPG más icónicos de todos los tiempos con una experiencia visual y jugable completamente renovada.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 40.50
                },
                {
                    "name": "Chrono Trigger",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/chronotrigger-switch-1-768x1024_kb4krd-min_f5ulah.png",
                    "year": "1995",
                    "brand": "Square Enix",
                    "platform": "Nintendo Switch",
                    "type": "RPG",
                    "category":"videojuegos",
                    "description": "\nChrono Trigger es un RPG clásico con una historia de viajes en el tiempo, donde los jugadores controlan a un grupo de héroes que deben salvar al mundo de una amenaza apocalíptica. Este título es reconocido por su narrativa, personajes y sistema de combate.\n\nCaracterísticas\n- Sistema de combate innovador y fluido\n- Múltiples finales dependiendo de las decisiones del jugador\n- Historia rica y personajes memorables\n\nIdeal para\nAmantes de los RPGs clásicos que disfrutan de una historia épica de aventuras y viajes temporales.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 40.00
                },
                {
                    "name": "Diablo III",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/diablo_III_ktyrsc-min_lgpsq9.jpg",
                    "year": "2000",
                    "brand": "Blizzard Entertainment",
                    "platform": "PC",
                    "type": "RPG",
                    "category":"videojuegos",
                    "description": "\nDiablo III es un RPG de acción donde los jugadores exploran mazmorras oscuras y luchan contra hordas de demonios. Con un enfoque en el loot y el progreso de personaje, es una de las entregas más populares de la saga Diablo.\n\nCaracterísticas\n- Jugabilidad adictiva y dinámica\n- Gran variedad de clases y habilidades\n- Acción en tiempo real con gráficos impresionantes para su época\n\nIdeal para\nJugadores que disfrutan de un RPG de acción intenso con un enfoque en la recolección de botín y el progreso continuo del personaje.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 20.00
                },
                {
                    "name": "Mass Effect 2",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529852/mass_effect_2_tutidm-min_y6nycv.jpg",
                    "year": "2010",
                    "brand": "BioWare",
                    "platform": "PlayStation 3",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nMass Effect 2 es un RPG de acción con una narrativa envolvente en el espacio exterior. Los jugadores toman el rol del comandante Shepard mientras reclutan un equipo para salvar a la galaxia de una invasión inminente.\n\nCaracterísticas\n- Historia profunda con decisiones que afectan el curso de la trama\n- Sistema de combate táctico y personalización de personajes\n- Enemigos y mundos bien diseñados\n\nIdeal para\nJugadores que disfrutan de una historia épica con decisiones difíciles que tienen un impacto significativo en el mundo del juego.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 15.50
                },
                {
                    "name": "The Witcher 3: Wild Hunt",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529844/the-witcher-3-wild-hunt-201551495951_1_kdwsj2-min_brl0sq.jpg",
                    "year": "2015",
                    "brand": "CD Projekt Red",
                    "platform": "PC",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nThe Witcher 3: Wild Hunt es un RPG de mundo abierto que sigue a Geralt de Rivia, un cazador de monstruos, mientras busca a su hija adoptiva y se enfrenta a una guerra apocalíptica. El juego destaca por su historia envolvente y su mundo vasto y detallado.\n\nCaracterísticas\n- Mundo abierto expansivo y detallado\n- Combate dinámico y habilidades personalizables\n- Decisiones que afectan el mundo y la narrativa\n\nIdeal para\nJugadores que disfrutan de una historia profunda, exploración en un mundo abierto y combates intensos contra monstruos y humanos.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 30.99
                },
                {
                    "name": "Persona 5 Royal",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529839/personasroyal5_wx6re4-min_oxkzos.jpg",
                    "year": "2016",
                    "brand": "Atlus",
                    "platform": "PlayStation 4",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nPersona 5 Royal es una versión ampliada del aclamado juego de rol, donde los jugadores controlan a un grupo de estudiantes de secundaria que tienen la capacidad de entrar en un mundo paralelo y luchar contra los deseos corruptos de la sociedad.\n\nCaracterísticas\n- Combate por turnos y estrategias profundas\n- Estilo visual único y una narrativa emocionalmente compleja\n- Gran cantidad de actividades secundarias y eventos sociales\n\nIdeal para\nJugadores que disfrutan de una historia compleja, personajes carismáticos y una jugabilidad rica con una mezcla de exploración, combate y simulación social.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 50.00
                }, 
                {
                    "name": "Elden Ring",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529849/elden-ring_ppzv2y-min_nxxfwd.jpg",
                    "year": "2022",
                    "brand": "FromSoftware",
                    "platform": "XBOX",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nElden Ring es un RPG de acción desarrollado por FromSoftware, conocido por sus mundos abiertos y su dificultad desafiante. En este juego, los jugadores exploran un vasto mundo lleno de misterios, combates épicos y un sistema de progreso profundo.\n\nCaracterísticas\n- Mundo abierto extenso y detallado\n- Desafiante sistema de combate en tiempo real\n- Historia rica escrita en colaboración con George R.R. Martin\n\nIdeal para\nJugadores que buscan una experiencia desafiante, con exploración abierta y una narrativa envolvente en un mundo de fantasía oscura.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 60.00
                },
                {
                    "name": "Age of Empires III",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529839/ageofempires_zycjst-min_sqose6.jpg",
                    "year": "1999",
                    "brand": "Ensemble Studios",
                    "platform": "PC",
                    "type": "Estrategia",
                    "category":"videojuegos",
                    "description": "\nAge of Empires II es un juego de estrategia en tiempo real que lleva a los jugadores a través de la historia, donde pueden construir imperios y luchar en batallas históricas. Es uno de los títulos más emblemáticos de la serie y es conocido por su jugabilidad profunda.\n\nCaracterísticas\n- Amplia variedad de civilizaciones jugables\n- Modo campaña con misiones históricas\n- Estrategia en tiempo real con énfasis en la gestión de recursos\n\nIdeal para\nAmantes de los juegos de estrategia que disfrutan de la gestión de imperios y la toma de decisiones tácticas.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 25.00
                },
                {
                    "name": "StarCraft",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529845/starcraft_dpcqkr-min_f8g1mb.jpg",
                    "year": "1998",
                    "brand": "Blizzard Entertainment",
                    "platform": "PC",
                    "type": "Estrategia",
                    "category":"videojuegos",
                    "description": "\nStarCraft es un juego de estrategia en tiempo real que ha marcado un antes y un después en el género. Los jugadores controlan tres razas distintas, cada una con su propio estilo de juego, y compiten en un universo futurista lleno de batallas intensas.\n\nCaracterísticas\n- Tres razas únicas con estrategias propias\n- Multijugador altamente competitivo\n- Profundización en el control de unidades y gestión de recursos\n\nIdeal para\nJugadores que disfrutan de una estrategia profunda y de batallas intensas en un mundo futurista.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 20.00
                },
                {
                    "name": "Civilization III",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/civilizationII_wbsvu2-min_zztxba.jpg",
                    "year": "2001",
                    "brand": "Firaxis Games",
                    "platform": "PC",
                    "type": "Estrategia",
                    "category":"videojuegos",
                    "description": "\nCivilization III es un juego de estrategia por turnos donde los jugadores lideran una civilización desde la antigüedad hasta la era moderna. El objetivo es construir un imperio que sea capaz de competir contra otros jugadores o la IA en múltiples frentes.\n\nCaracterísticas\n- Gran enfoque en la gestión de recursos y diplomacia\n- Varias victorias posibles: científica, militar, cultural\n- Amplia cantidad de civilizaciones y líderes históricos\n\nIdeal para\nJugadores que disfrutan de juegos estratégicos complejos y de la simulación de civilizaciones.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 15.50
                },
                {
                    "name": "Crusader Kings III",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529852/crusanders_king-min_yxzkqi.jpg",
                    "year": "2020",
                    "brand": "Paradox Interactive",
                    "platform": "Xbox Series X",
                    "type": "Estrategia",
                    "category":"videojuegos",
                    "description": "\nCrusader Kings III es un juego de gran estrategia donde los jugadores controlan una dinastía y toman decisiones políticas, militares y familiares a lo largo de generaciones. El juego destaca por su complejidad y profundidad en los aspectos de simulación de la nobleza medieval.\n\nCaracterísticas\n- Control total sobre dinastías y relaciones familiares\n- Profundización en las decisiones políticas y diplomáticas\n- Amplias opciones de personalización y estrategia\n\nIdeal para\nJugadores que buscan un desafío en la gestión de imperios y relaciones familiares en un contexto medieval.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 14.99
                },
                {
                    "name": "Total War: Warhammer III",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529849/TW_Warhammer3_t7kjio-min_daecqu.jpg",
                    "year": "2022",
                    "brand": "Sega",
                    "platform": "PlayStation 5",
                    "type": "Estrategia",
                    "category":"videojuegos",
                    "description": "\nTotal War: Warhammer III combina la estrategia por turnos con la táctica en tiempo real, ambientado en el universo de Warhammer. Los jugadores pueden controlar facciones fantásticas y librar batallas épicas mientras gestionan imperios.\n\nCaracterísticas\n- Batallas masivas en tiempo real\n- Facciones y unidades fantásticas inspiradas en el universo Warhammer\n- Juego por turnos en el cual se toman decisiones tácticas y estratégicas\n\nIdeal para\nJugadores que disfrutan de la estrategia a gran escala, con batallas épicas y un rico universo de fantasía.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 39.99
                },
                {
                    "name": "FIFA ‘98",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/15053844395358-min_bdhxau.jpg",
                    "year": "1997",
                    "brand": "EA Sports",
                    "platform": "PlayStation 1",
                    "type": "Deporte",
                    "category":"videojuegos",
                    "description": "\nFIFA ‘98 es una de las entregas más populares de la franquicia FIFA, lanzada para PlayStation 1. Incluye la opción de jugar el Mundial de Fútbol y es conocida por su jugabilidad fluida y su enfoque realista en el fútbol.\n\nCaracterísticas\n- Modo mundialista con todos los equipos de la Copa del Mundo\n- Gráficos avanzados para su época\n- Jugabilidad intuitiva y rápida\n\nIdeal para\nAmantes de los juegos de fútbol y nostálgicos de los primeros títulos de la franquicia FIFA.",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 19.50
                },
                {
                    "name": "Tony Hawk’s Pro Skater 2",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529837/R-26047441-1675973090-8635-min_fg5vke.jpg",
                    "year": "2000",
                    "brand": "Activision",
                    "platform": "PlayStation 1",
                    "type": "Deporte",
                    "category":"videojuegos",
                    "description": "\nTony Hawk’s Pro Skater 2 es un juego de skateboarding que revolucionó el género con su jugabilidad fluida y su extenso repertorio de trucos. El juego permite a los jugadores realizar acrobacias complejas mientras exploran diversos entornos.\n\nCaracterísticas\n- Jugabilidad adictiva y fluida\n- Diversos escenarios con rampas y obstáculos\n- Modo multijugador para disfrutar con amigos\n\nIdeal para\nAficionados al skate y jugadores que buscan un título dinámico y desafiante con un toque clásico de la era dorada del PS1.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 40.00
                },
                {
                    "name": "NBA Street",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529840/NBA_Street_iao7q0-min_s1d289.jpg",
                    "year": "2001",
                    "brand": "EA Sports BIG",
                    "platform": "PlayStation 2",
                    "type": "Deporte",
                    "category":"videojuegos",
                    "description": "\nNBA Street es un juego de baloncesto de estilo arcade con un enfoque en jugadas acrobáticas y jugabilidad rápida. Ofrece partidos de baloncesto urbanos donde los jugadores pueden realizar trucos y movimientos espectaculares.\n\nCaracterísticas\n- Jugabilidad basada en trucos y acrobacias\n- Modos de juego innovadores y divertidos\n- Música dinámica que acompaña la acción\n\nIdeal para\nJugadores que buscan una experiencia de baloncesto arcade rápida y divertida con amigos.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 30.00
                },
                {
                    "name": "Gran Turismo 7",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529852/PS5-Gran-Turismo-7-min_svogdp.jpg",
                    "year": "2022",
                    "brand": "Sony Interactive Entertainment",
                    "platform": "PlayStation 5",
                    "type": "Deporte",
                    "category":"videojuegos",
                    "description": "\nGran Turismo 7 es un simulador de carreras de coches que lleva la experiencia de conducción al siguiente nivel, con gráficos impresionantes y una jugabilidad extremadamente realista.\n\nCaracterísticas\n- Amplia selección de coches y circuitos\n- Gráficos realistas optimizados para PS5\n- Sistema de personalización detallado para coches\n\nIdeal para\nAmantes de las carreras y la simulación que buscan un desafío realista y una experiencia visual impresionante.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 59.99
                },
                {
                    "name": "Mario Kart 8",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529852/Mario_Kart_8_f2feq9-min_xxgsme.jpg",
                    "year": "2014",
                    "brand": "Nintendo",
                    "platform": "Nintendo Switch",
                    "type": "Deporte",
                    "category":"videojuegos",
                    "description": "\nMario Kart 8 es un juego de carreras rápido y colorido donde los personajes de Mario compiten en circuitos llenos de obstáculos y potenciadores. Es uno de los títulos más divertidos de la saga Mario Kart.\n\nCaracterísticas\n- Diversión para toda la familia con multijugador local y online\n- Circuitos llenos de sorpresas y potenciadores\n- Gráficos impresionantes en la Nintendo Switch\n\nIdeal para\nJugadores de todas las edades que buscan una experiencia de carreras divertida y accesible.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 39.99
                },
                {
                    "name": "Street Fighter 30TH Anniversary",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738533179/61LEMlRMEKL._AC_UF894_1000_QL80__1_j59yld.jpg",
                    "year": "2018",
                    "brand": "Capcom",
                    "platform": "PlayStation 4",
                    "type": "Pelea",
                    "category":"videojuegos",
                    "description": "\nStreet Fighter 30th Anniversary es una recopilación que celebra los 30 años de la famosa saga de lucha, ofreciendo los mejores títulos de la serie en una edición definitiva.\n\nCaracterísticas\n- Incluye 12 juegos clásicos de la saga Street Fighter\n- Modo multijugador online para competir con otros jugadores\n- Gráficos remasterizados y opciones de personalización\n\nIdeal para\nFanáticos de los juegos de lucha y aquellos que quieren revivir los clásicos de la saga Street Fighter.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 39.99
                },
                {
                    "name": "Mortal Kombat 1",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529850/mc-min_fux4y9.jpg",
                    "year": "2023",
                    "brand": "Warner Bros.Games",
                    "platform": "PlayStation 5",
                    "type": "Pelea",
                    "category":"videojuegos",
                    "description": "\nMortal Kombat 1 es una nueva entrega de la famosa saga de lucha que se reinicia con una historia fresca y combate brutal. El juego ofrece una jugabilidad fluida y un elenco de personajes icónicos.\n\nCaracterísticas\n- Nuevos personajes y escenarios impactantes\n- Combate brutal y sangriento, fiel a la saga\n- Historia renovada que revitaliza la franquicia\n\nIdeal para\nFanáticos de los juegos de lucha que buscan una experiencia más intensa y con combate sangriento.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 49.50
                },
                {
                    "name": "Tekken 3",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/teken3-min_thks8c.jpg",
                    "year": "1998",
                    "brand": "Namco",
                    "platform": "PlayStation 1",
                    "type": "Pelea",
                    "category":"videojuegos",
                    "description": "\nTekken 3 es uno de los mejores juegos de lucha de todos los tiempos, conocido por su jugabilidad precisa, combos espectaculares y una amplia gama de personajes. Es una de las entregas más queridas de la saga Tekken.\n\nCaracterísticas\n- Amplio elenco de personajes jugables\n- Gráficos impresionantes para su época\n- Sistema de combos fluido y variado\n\nIdeal para\nFanáticos de los juegos de lucha que disfrutan de batallas rápidas y técnicas con una jugabilidad accesible y profunda.",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 60.00
                },
                {
                    "name": "Soulcalibur II",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529853/81732--soulcalibur-ii-min_va3ysp.png",
                    "year": "2002",
                    "brand": "Namco",
                    "platform": "GameCube",
                    "type": "Accion",
                    "category":"videojuegos",
                    "description": "\nSoulcalibur II es un juego de lucha con armas que ofrece combates rápidos, una amplia variedad de personajes y escenarios visualmente impresionantes. La serie es conocida por su jugabilidad accesible y su enfoque en el combate cuerpo a cuerpo.\n\nCaracterísticas\n- Diversos modos de juego, desde historia hasta multijugador\n- Personajes icónicos como Mitsurugi y Nightmare\n- Combate basado en armas, con una jugabilidad técnica\n\nIdeal para\nJugadores que disfrutan de juegos de lucha profundos con personajes únicos y combates emocionantes.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 12.00
                },
                {
                    "name": "Dragon Ball FighterZ",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/DBFZ_cover_art_kqmthb-min_n0bfs0.jpg",
                    "year": "2018",
                    "brand": "Arc System Works",
                    "platform": "GameCube",
                    "type": "Pelea",
                    "category":"videojuegos",
                    "description": "\nDragon Ball FighterZ es un juego de lucha en 2.5D que captura la esencia de la serie Dragon Ball con combates espectaculares y visuales impresionantes. Los jugadores pueden elegir entre una gran variedad de personajes de la saga para luchar en combates dinámicos.\n\nCaracterísticas\n- Combates rápidos y fluidos con movimientos especiales\n- Estilo visual fiel al anime de Dragon Ball\n- Modo multijugador para enfrentamientos épicos\n\nIdeal para\nFanáticos de Dragon Ball que buscan un juego de lucha rápido y con un diseño fiel a la serie.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 20.00
                },
                {
                    "name": "Super Smash Bros. Ultimate",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529844/Super_Smash_Bros._Ultimate_peznet-min_j7k4ja.jpg",
                    "year": "2018",
                    "brand": "Nintendo",
                    "platform": "Nintendo Switch",
                    "type": "Pelea",
                    "category":"videojuegos",
                    "description": "\nSuper Smash Bros. Ultimate es un juego de lucha crossover que reúne a personajes de múltiples franquicias de videojuegos. Ofrece una experiencia de juego única, con acción rápida y diversos modos para disfrutar con amigos o en solitario.\n\nCaracterísticas\n- Amplia selección de personajes jugables\n- Diversos modos de juego y escenarios\n- Multijugador local y online\n\nIdeal para\nJugadores que buscan un juego de lucha accesible pero competitivo con una enorme variedad de personajes y modos.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 50.00
                },
                {
                    "name": "Super Mario Bros.",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529843/Super_Mario_Bros._box_vdrzqu-min_mwbbuj.png",
                    "year": "1985",
                    "brand": "Nintendo",
                    "platform": "NES",
                    "type": "Plataforma",
                    "category":"videojuegos",
                    "description": "\nSuper Mario Bros. es uno de los juegos de plataformas más emblemáticos que definió una era en los videojuegos. Acompaña a Mario en su misión por salvar a la princesa Peach mientras atraviesa diversos niveles llenos de desafíos.\n\nCaracterísticas\n- Niveles de plataformas clásicos\n- Jugabilidad simple pero adictiva\n- Música y efectos icónicos\n\nIdeal para\nJugadores nostálgicos y aquellos que disfrutan de un juego de plataformas clásico.",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 30.50
                },
                {
                    "name": "Sonic the Hedgehog",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529846/Sonic_the_Hedgehog_1_Genesis_box_art_acuubo-min_s5erul.jpg",
                    "year": "1991",
                    "brand": "Sega",
                    "platform": "Genesis",
                    "type": "Plataforma",
                    "category":"videojuegos",
                    "description": "\nSonic the Hedgehog es el juego que introdujo al icónico erizo azul de Sega, conocido por su velocidad y niveles vibrantes. El juego se centra en superar obstáculos a gran velocidad mientras se recoge anillos y se enfrenta a enemigos.\n\nCaracterísticas\n- Velocidad frenética y niveles vibrantes\n- Elementos de plataforma innovadores\n- Personajes carismáticos y enemigos memorables\n\nIdeal para\nJugadores que disfrutan de plataformas rápidas con niveles coloridos y acción vertiginosa.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 24.99
                },
                {
                    "name": "Donkey Kong Country",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/Donkey_Kong_Country_SNES_cover_vxpade-min_bwjaa8.png",
                    "year": "1994",
                    "brand": "Rare",
                    "platform": "SNES",
                    "type": "Plataforma",
                    "category":"videojuegos",
                    "description": "\nDonkey Kong Country es un juego de plataformas innovador para SNES, que destacó por sus gráficos prerenderizados y sus niveles desafiantes. Acompaña a Donkey Kong y Diddy Kong en su aventura para recuperar su tesoro robado.\n\nCaracterísticas\n- Gráficos avanzados para la época\n- Jugabilidad clásica de plataformas con un toque innovador\n- Variedad de niveles y enemigos\n\nIdeal para\nJugadores que buscan un reto clásico de plataformas con una atmósfera única y un diseño visual impresionante para su época.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 20.00
                },
                {
                    "name": "Crash Bandicoot",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/Crash_Bandicoot_Cover_ebenoh-min_nsxf2k.png",
                    "year": "1996",
                    "brand": "Naughty Dog",
                    "platform": "PlayStation",
                    "type": "Plataforma",
                    "category":"videojuegos",
                    "description": "\nCrash Bandicoot es un clásico juego de plataformas en 3D protagonizado por el carismático marsupial Crash. A través de varios niveles desafiantes, los jugadores deben saltar, girar y evitar obstáculos mientras recolectan frutas.\n\nCaracterísticas\n- Niveles en 3D con desafíos dinámicos\n- Protagonista memorable con habilidades únicas\n- Gráficos avanzados para la época\n\nIdeal para\nJugadores que disfrutan de plataformas en 3D con una jugabilidad desafiante y personajes carismáticos.",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 19.99
                },
                {
                    "name": "Spyro Trilogy",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529844/Spyro_Reignited_Trilogy_yfizwo-min_a6udjf.png",
                    "year": "1998",
                    "brand": "Insomniac Games",
                    "platform": "PlayStation",
                    "type": "Plataforma",
                    "category":"videojuegos",
                    "description": "\nLa Spyro Trilogy es una colección de tres juegos de plataformas protagonizados por Spyro, un pequeño dragón morado. Con entornos coloridos y jugabilidad amigable, esta trilogía se ha ganado un lugar especial en los corazones de los jugadores.\n\nCaracterísticas\n- Tres juegos remasterizados con gráficos actualizados\n- Diversión para todas las edades con plataformas y coleccionables\n- Ambientación encantadora y personajes entrañables\n\nIdeal para\nJugadores que buscan un juego de plataformas accesible, con un toque de nostalgia y gráficos mejorados.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 25.00
                },
                {
                    "name": "Hollow Knight",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529849/hollow_knigh-min_qx2sbs.jpg",
                    "year": "2017",
                    "brand": "Team Cherry",
                    "platform": "Nintendo Switch",
                    "type": "Plataforma",
                    "category":"videojuegos",
                    "description": "\nHollow Knight es un juego de plataformas Metroidvania ambientado en un mundo sombrío lleno de misterios y secretos por descubrir.\n\nCaracterísticas\n- Desafiantes combates contra jefes\n- Gran exploración en un vasto mapa interconectado\n- Estilo de arte único y hermoso\n\nIdeal para\nJugadores que disfrutan de la exploración y los combates desafiantes.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 15.50
                },
                {
                    "name": "Red Dead Redemption",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529847/Red_Dead_Redemption_mpug31-min_wnlohn.jpg",
                    "year": "2010",
                    "brand": "Rockstar Games",
                    "platform": "PlayStation 3",
                    "type": "Accion",
                    "category":"videojuegos",
                    "description": "\nRed Dead Redemption es un juego de acción de mundo abierto que te transporta al Lejano Oeste, donde debes enfrentarte a desafíos mientras sigues una narrativa profunda.\n\nCaracterísticas\n- Mundo abierto con una gran libertad de acción\n- Historia rica y profunda\n- Diversas actividades, como cazar, pescar y enfrentarse a otros vaqueros\n\nIdeal para\nLos amantes de los juegos de acción y los fanáticos del Lejano Oeste.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 15.00
                },
                {
                    "name": "Ori and the Blind Forest",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529841/302601-ori-and-the-blind-forest-xbox-one-front-cover_lwpkdm-min_e3a5oc.jpg",
                    "year": "2015",
                    "brand": "Moon Studios & Microsoft Studios",
                    "platform": "XBOX",
                    "type": "Plataforma",
                    "category":"videojuegos",
                    "description": "\nOri and the Blind Forest es un juego de plataformas que destaca por su emotiva historia y sus bellos gráficos, además de sus desafiantes mecánicas de juego.\n\nCaracterísticas\n- Hermosos gráficos en 2D\n- Historia emotiva y profunda\n- Mecánicas de plataformas desafiantes\n\nIdeal para\nJugadores que buscan una experiencia emocional y desafiante.",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 18.50
                },
                {
                    "name": "Resident Evil",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529845/resident-evil.VIII_fkqnyo-min_m5lpqn.jpg",
                    "year": "1996",
                    "brand": "Capcom",
                    "platform": "PlayStation 1",
                    "type": "Horror",
                    "category":"videojuegos",
                    "description": "\nResident Evil es un juego de terror y supervivencia que ha sido pionero en su género, ofreciendo una experiencia de juego llena de suspenso y desafíos.\n\nCaracterísticas\n- Exploración y resolución de acertijos\n- Ambiente tenso y aterrador\n- Primer juego de la serie que introdujo la mecánica de supervivencia en un mundo de zombis\n\nIdeal para\nFanáticos del horror clásico y aquellos que buscan una experiencia de supervivencia desafiante.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 19.99
                },
                {
                    "name": "Silent Hill",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529846/Silent_Hill_video_game_cover_dluar8-min_csl95p.png",
                    "year": "1999",
                    "brand": "Konami",
                    "platform": "PlayStation 1",
                    "type": "Horror",
                    "category":"videojuegos",
                    "description": "\nSilent Hill es un juego de terror psicológico que juega con la mente del jugador, sumergiéndolo en un pueblo lleno de horrores sobrenaturales.\n\nCaracterísticas\n- Ambiente espeluznante y perturbador\n- Enfoque en el terror psicológico más que en el gore\n- Historia que mantiene a los jugadores atrapados con giros sorprendentes\n\nIdeal para\nJugadores que disfrutan del terror psicológico y la tensión constante.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 140.00
                },
                {
                    "name": "Fatal Frame II",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529849/Fatal_Frame_II_-_Crimson_Butterfly_xfzroh-min_mwlurq.jpg",
                    "year": "2003",
                    "brand": "Tecmo",
                    "platform": "PlayStation 2",
                    "type": "Horror",
                    "category":"videojuegos",
                    "description": "\nFatal Frame II: Crimson Butterfly es un juego de survival horror que utiliza una cámara como principal herramienta para enfrentarse a los fantasmas.\n\nCaracterísticas\n- Juega con la tensión y el miedo psicológico\n- Cámara como principal elemento de combate\n- Historia de terror japonesa con un ambiente único\n\nIdeal para\nLos fans de los juegos de terror y quienes disfrutan de mecánicas innovadoras de supervivencia.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 100.00
                },
                {
                    "name": "Amnesia: The Dark Descent",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/Amnesia-The-Dark-Descent-Cover-Art_kcntd2-min_yrvkuh.png",
                    "year": "2010",
                    "brand": "Frictional Games",
                    "platform": "PC",
                    "type": "Horror",
                    "category":"videojuegos",
                    "description": "\nAmnesia: The Dark Descent es un juego de terror en primera persona que se centra en la exploración y la resolución de acertijos en un ambiente oscuro y misterioso.\n\nCaracterísticas\n- Enfoque en el terror psicológico\n- Estilo de juego en primera persona que aumenta la inmersión\n- Resolver acertijos mientras se explora un antiguo castillo\n\nIdeal para\nJugadores que disfrutan de una atmósfera tensa y desafíos mentales en un juego de terror.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 4.99
                },
                {
                    "name": "Resident Evil 7: Biohazard",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529841/91AF0_BXxbL._AC_UF894_1000_QL80__nb79sz-min_vzojds.jpg",
                    "year": "2017",
                    "brand": "Biohazard - Capcom",
                    "platform": "PlayStation 4",
                    "type": "Horror",
                    "category":"videojuegos",
                    "description": "\nResident Evil 7: Biohazard es un juego de terror de supervivencia que se aleja de los elementos de acción y regresa a las raíces del horror psicológico.\n\nCaracterísticas\n- Perspectiva en primera persona para una mayor inmersión\n- Ambiente tenso y aterrador\n- Elementos de supervivencia tradicionales de la serie\n\nIdeal para\nFanáticos del survival horror clásico con un enfoque más psicológico.",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 30.50
                },
                {
                    "name": "Dead Space Remake",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/deadspace_t5mklj-min_hm3msl.jpg",
                    "year": "2023",
                    "brand": "Motive Studio",
                    "platform": "PC",
                    "type": "Aventura",
                    "category":"videojuegos",
                    "description": "\nDead Space Remake es una versión modernizada del clásico juego de terror espacial, mejorando los gráficos y la jugabilidad mientras conserva la atmósfera tensa.\n\nCaracterísticas\n- Gráficos mejorados y sonidos aterradores\n- Historia de terror espacial con giros inesperados\n- Nuevas mecánicas de juego y ajustes en la jugabilidad\n\nIdeal para\nJugadores que buscan revivir el clásico Dead Space con una experiencia visual mejorada y mayor inmersión.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 69.99
                },
                {
                    "name": "Undertale",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529847/undertale_ahffuo-min_dbsbtw.jpg",
                    "year": "2015",
                    "brand": "Toby Fox",
                    "platform": "Nintendo Switch",
                    "type": "Indie",
                    "category":"videojuegos",
                    "description": "\nUndertale es un juego indie que combina humor, acción y decisiones importantes en un mundo de fantasía donde tus elecciones realmente importan.\n\nCaracterísticas\n- Sistema de combate único basado en la negociación\n- Mundo lleno de personajes memorables\n- Varias rutas de juego basadas en las decisiones del jugador\n\nIdeal para\nJugadores que disfrutan de historias profundas y sistemas de combate innovadores.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 10.00
                },
                {
                    "name": "Stardew Valley",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529844/stardewvalley_cv9ogv-min_ljdrgc.png",
                    "year": "2016",
                    "brand": "ConcernedApe",
                    "platform": "Nintendo Switch",
                    "type": "Indie",
                    "category":"videojuegos",
                    "description": "\nStardew Valley es un juego de simulación de granja en el que los jugadores deben cultivar, pescar, y hacer amistades en un pueblo encantador.\n\nCaracterísticas\n- Personalización de la granja y el pueblo\n- Gran énfasis en la interacción social\n- Diversión sin fin con actividades diarias\n\nIdeal para\nJugadores que disfrutan de los juegos relajantes y las simulaciones de vida.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 20.00
                },
                {
                    "name": "Celeste",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/Celeste_Switch_y1c7zp-min_rcoxeu.jpg",
                    "year": "2018",
                    "brand": "Maddy Makes Games",
                    "platform": "Nintendo Switch",
                    "type": "Indie",
                    "category":"videojuegos",
                    "description": "\nCeleste es un juego de plataformas desafiante y emocional que sigue la historia de Madeline mientras escala la montaña Celeste.\n\nCaracterísticas\n- Desafiantes niveles de plataformas\n- Historia que explora temas emocionales profundos\n- Controles precisos y fluidos\n\nIdeal para\nJugadores que buscan un reto en plataformas y una historia conmovedora.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 29.00
                },
                {
                    "name": "Hades",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738529838/hades-min_grxm6u.jpg",
                    "year": "2020",
                    "brand": "Supergiant Games",
                    "platform": "PlayStation 5",
                    "type": "Accion",
                    "category":"videojuegos",
                    "description": "\nHades es un juego de acción rogue-like en el que juegas como Zagreus, el hijo de Hades, tratando de escapar del inframundo mientras enfrentas a enemigos desafiantes.\n\nCaracterísticas\n- Combates rápidos y fluidos\n- Múltiples armas y poderes para personalizar el estilo de juego\n- Historia interactiva con personajes memorables\n\nIdeal para\nJugadores que disfrutan de acción intensa y la rejugabilidad de los rogue-likes.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 19.99
                }

                ],
                "accessory":[ 
                {
                    "name": "Power Glove NES",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530369/NES-Power-Glove_usrmzd_tmxdww.jpg",
                    "year": 1989,
                    "brand": "Mattel",
                    "platform": "Nintendo Entertainment System",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl Power Glove es un accesorio icónico para el NES que permite controlar los juegos mediante movimientos de la mano, introduciendo un concepto único para la época.\n\nCaracterísticas\n- Control mediante sensores de movimiento\n- Diseño futurista para su tiempo\n- Compatible con juegos específicos\n\nIdeal para\nJugadores nostálgicos y coleccionistas de accesorios únicos de Nintendo.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 239.00
                },
                {
                    "name": "Expansion Module Atari 7800",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530373/Expasion_Module_Atari_zw66wh_miaqih.png",
                    "year": "1986",
                    "brand": "Atari Corporation",
                    "platform": "Atari 7800",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl Expansion Module para el Atari 7800 es un accesorio diseñado para ampliar las capacidades de la consola y ofrecer compatibilidad adicional.\n\nCaracterísticas\n- Incrementa las funcionalidades de la consola\n- Fácil de instalar y usar\n- Compatible con ciertos juegos y accesorios\n\nIdeal para\nColeccionistas y usuarios del Atari 7800 que buscan explorar todo el potencial de la consola.",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 694.99
                },
                {
                    "name": "Super Nintendo MultiTap",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530371/Super_Nintendo_MultiTap_zr0myz_pexyzv.jpg",
                    "year": "1993",
                    "brand": "Nintendo",
                    "platform": "Super Nintendo Entertainment System",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl Super Nintendo MultiTap permite conectar hasta 5 jugadores simultáneamente, haciendo los juegos multijugador más accesibles.\n\nCaracterísticas\n- Soporta hasta 5 controladores simultáneamente\n- Compatible con juegos multijugador específicos\n- Diseño compacto y fácil de conectar\n\nIdeal para\nJugadores que disfrutan de experiencias multijugador en la SNES.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 15.00
                },
                {
                    "name": "Joystick AES",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530370/images_sxhpjr_ctypyj.jpg",
                    "year": "1990",
                    "brand": "SNK",
                    "platform": "Neo Geo",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl Joystick AES ofrece una experiencia auténtica de arcade en casa, diseñado específicamente para los juegos de Neo Geo.\n\nCaracterísticas\n- Diseño inspirado en los controles de arcade\n- Construcción robusta para máxima durabilidad\n- Compatible con todos los juegos de Neo Geo AES\n\nIdeal para\nAmantes de los juegos de arcade y fans de Neo Geo que buscan máxima precisión.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 50.50
                },
                {
                    "name": "Memory Card",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530375/1015px-PSX-Memory-Card_n9e6w7_qr6mkk.jpg",
                    "year": "1994",
                    "brand": "Sony",
                    "platform": "PlayStation",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nLa Memory Card para PlayStation permite guardar el progreso de los juegos, ofreciendo comodidad y flexibilidad para los jugadores.\n\nCaracterísticas\n- Almacena datos de guardado para múltiples juegos\n- Diseño compacto y portátil\n- Fácil de usar e intercambiar entre consolas\n\nIdeal para\nJugadores de PlayStation que quieren guardar y reanudar sus partidas de forma sencilla.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 10.00
                },  
                {
                    "name": "Transfer Pak",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530369/Nintendo-64-GB-Transfer-Pak_dyciuw_ucczfo.jpg",
                    "year": "1999",
                    "brand": "Nintendo",
                    "platform": "Nintendo 64",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl Transfer Pak permite conectar juegos de Game Boy a la Nintendo 64, proporcionando funcionalidad adicional y compatibilidad entre plataformas.\n\nCaracterísticas\n- Conexión sencilla entre Game Boy y Nintendo 64\n- Compatible con títulos específicos\n- Expande las posibilidades de juego\n\nIdeal para\nJugadores de Nintendo 64 que buscan mejorar la integración con sus juegos de Game Boy.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 15.00
                },
                {
                    "name": "Game Boy Printer",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530371/Game_Boy_Printer_ojfudf_hiab3f.jpg",
                    "year": "1998",
                    "brand": "Nintendo",
                    "platform": "Game Boy",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nLa Game Boy Printer es una impresora portátil diseñada para funcionar con juegos compatibles de Game Boy, permitiendo imprimir imágenes y contenido del juego.\n\nCaracterísticas\n- Impresión portátil desde Game Boy\n- Compatible con varios juegos\n- Diseño compacto y fácil de usar\n\nIdeal para\nJugadores nostálgicos que buscan personalizar su experiencia de Game Boy.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 25.00
                },
                {
                    "name": "DualShock 2",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530375/1280px-PSX-DualShock-Controller_pdvd9i_mxnaok.jpg",
                    "year": "2000",
                    "brand": "PlayStation",
                    "platform": "PlayStation 2",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl DualShock 2 es el controlador oficial de PlayStation 2, ofreciendo vibración y controles analógicos para una experiencia de juego inmersiva.\n\nCaracterísticas\n- Vibración para mayor inmersión\n- Controles analógicos precisos\n- Diseño ergonómico y familiar\n\nIdeal para\nJugadores de PlayStation 2 que buscan un control confiable y avanzado.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 25.00
                },
                {
                    "name": "Game Boy Player",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738534541/GameCube-Game-Boy-Player_gkbux2.jpg",
                    "year": "2001",
                    "brand": "Nintendo",
                    "platform": "GameCube",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl Game Boy Player permite jugar títulos de Game Boy en la consola GameCube, ampliando la compatibilidad entre plataformas.\n\nCaracterísticas\n- Soporte para juegos de Game Boy, Game Boy Color y Game Boy Advance\n- Fácil de instalar en la GameCube\n- Mejora la experiencia de juego portátil en pantalla grande\n\nIdeal para\nPropietarios de GameCube que quieren disfrutar de su biblioteca de Game Boy en su televisor.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 40.50
                },
                {
                    "name": "GameCube Link Cable",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530374/61kzvuwffPL_ddezuz_slwo66.jpg",
                    "year": "2001",
                    "brand": "Nintendo",
                    "platform": "GameCube",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl GameCube Link Cable conecta la consola GameCube con la Game Boy Advance, desbloqueando características exclusivas en juegos compatibles.\n\nCaracterísticas\n- Conexión sencilla entre dispositivos\n- Compatible con múltiples juegos\n- Expande la interacción entre GameCube y Game Boy Advance\n\nIdeal para\nJugadores que desean disfrutar de experiencias adicionales en juegos compatibles.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 25.00
                },
                {
                    "name": "Stylus",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530372/s-l400_fxwx4w_idyv2x.jpg",
                    "year": "2004",
                    "brand": "Nintendo",
                    "platform": "Nintendo DS",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl Stylus es un accesorio esencial para la Nintendo DS, diseñado para interactuar con la pantalla táctil de la consola de manera precisa y cómoda.\n\nCaracterísticas\n- Diseño ligero y fácil de usar\n- Compatible con todos los modelos de Nintendo DS\n- Construcción duradera para uso prolongado\n\nIdeal para\nUsuarios de Nintendo DS que buscan un accesorio confiable para la interacción táctil.",
                    "stock": 1,
                    "state": True,
                    "promoted": True,
                    "price": 9.99
                },
                {
                    "name": "Camera PSP",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530370/products-894_mlzxgb_dilxb5.jpg",
                    "year": "2004",
                    "brand": "Sony",
                    "platform": "PSP",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nLa Camera PSP es un accesorio que permite capturar fotos y videos directamente desde tu consola PSP, ofreciendo una experiencia multimedia única.\n\nCaracterísticas\n- Resolución compacta ideal para su época\n- Compatible con varios juegos de PSP\n- Diseño ligero y portátil\n\nIdeal para\nUsuarios de PSP que buscan maximizar las capacidades multimedia de su consola.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 10.00
                },
                {
                    "name": "Kinect",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530376/kinetic_fdyyby_xdtuw1.jpg",
                    "year": "2010",
                    "brand": "Microsoft",
                    "platform": "XBOX",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nKinect es un sensor de movimiento que permite a los jugadores interactuar con su consola Xbox sin necesidad de un controlador.\n\nCaracterísticas\n- Captura de movimiento precisa\n- Compatible con juegos y aplicaciones multimedia\n- Control por voz integrado\n\nIdeal para\nJugadores que buscan experiencias inmersivas y control sin contacto.",
                    "stock": 1,
                    "state": False,
                    "promoted": True,
                    "price": 40.00
                },
                {
                    "name": "Bluetooth Headset",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530374/blueheadset_kwgktg_wl314u.jpg",
                    "year": "2006",
                    "brand": "Sony",
                    "platform": "PS3",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl Bluetooth Headset para PS3 ofrece una comunicación clara y manos libres para juegos en línea.\n\nCaracterísticas\n- Tecnología Bluetooth para conexión inalámbrica\n- Diseño ergonómico y ligero\n- Micrófono de alta calidad para conversaciones claras\n\nIdeal para\nJugadores de PS3 que disfrutan de juegos multijugador y necesitan comunicación eficiente.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 25.50
                },
                {
                    "name": "DualShock 4",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530370/71Liv-br3iL._AC_UF894_1000_QL80__ga1xvk.jpg",
                    "year": "2013",
                    "brand": "Sony",
                    "platform": "PS4",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl DualShock 4 es el controlador principal para la consola PS4, ofreciendo una experiencia de juego precisa e inmersiva.\n\nCaracterísticas\n- Sensores de movimiento integrados\n- Panel táctil interactivo\n- Botón Share para capturas y transmisiones instantáneas\n\nIdeal para\nJugadores que buscan un controlador confiable y versátil para sus juegos de PS4.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 40.50
                },
                {
                    "name": "Elite Controller",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530370/EliteController_evcdyd_ujyyog.jpg",
                    "year": "2013",
                    "brand": "Microsoft",
                    "platform": "XBOX",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl Elite Controller es un controlador personalizable diseñado para jugadores competitivos y entusiastas.\n\nCaracterísticas\n- Partes intercambiables para personalización\n- Configuraciones avanzadas de botones\n- Materiales de alta calidad para durabilidad\n\nIdeal para\nJugadores que buscan el máximo rendimiento y personalización en su experiencia de juego.",
                    "stock": 1,
                    "state": True,
                    "promoted": False,
                    "price": 150.00
                },
                {
                    "name": "Amiibo NFC Reader",
                    "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530373/amiibo_tqy9kl_wmpmrm.jpg",
                    "year": "2011",
                    "brand": "Nintendo",
                    "platform": "3DS",
                    "type": "Accesorio",
                    "category":"accesorios",
                    "description": "\nEl Amiibo NFC Reader permite a los usuarios de Nintendo 3DS interactuar con figuras Amiibo para desbloquear contenido exclusivo.\n\nCaracterísticas\n- Compatible con una amplia variedad de Amiibos\n- Fácil de usar con consolas 3DS\n- Añade funcionalidades y contenido extra a los juegos\n\nIdeal para\nJugadores de Nintendo 3DS que desean expandir su experiencia con figuras Amiibo.",
                    "stock": 1,
                    "state": False,
                    "promoted": False,
                    "price": 30.00
                }, {
                "name": "Pulse 3D Headset PS5",
                "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530372/G03_p8a8gz.jpg",
                "year": "2020",
                "brand": "Sony",
                "platform": "PlatStation 5",
                "type": "Accesorio",
                "category":"accesorios",
                "description": "\nEl Pulse 3D Headset para PS5 ofrece una experiencia de audio inmersiva con soporte para audio 3D.\n\nCaracterísticas\n- Audio envolvente 3D\n- Diseño cómodo y elegante\n- Micrófonos duales con cancelación de ruido\n\nIdeal para\nJugadores de PS5 que desean una experiencia auditiva superior y comunicación clara.",
                "stock": 1,
                "state": True,
                "promoted": False,
                "price": 89.99
                },
                {
                "name": "Seagate Storage Expansion Card Xbox Series X/S 1TB",
                "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530370/61MGrHUMWzL_qe6opa.jpg",
                "year": "2020",
                "brand": "Seagate",
                "platform": "Xbox Series X",
                "type": "Accesorio",
                "category":"accesorios",
                "description": "\nLa Seagate Storage Expansion Card ofrece 1TB de almacenamiento adicional optimizado para las consolas Xbox Series X/S.\n\nCaracterísticas\n- Integración perfecta con la consola\n- Velocidades de carga rápidas\n- Diseño compacto y fácil de instalar\n\nIdeal para\nJugadores de Xbox Series X/S que necesitan ampliar su capacidad de almacenamiento sin comprometer el rendimiento.",
                "stock": 1,
                "state": True,
                "promoted": False,
                "price": 239.99
                },
                {
                "name": "Dock Steam Deck",
                "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530372/Sin_t%C3%ADtulo-4_m2qmn7.jpg",
                "year": "2022",
                "brand": "Valve",
                "platform": "Steam Deck",
                "type": "Accesorio",
                "category":"accesorios",
                "description": "\nEl Dock para Steam Deck permite conectar tu consola a una pantalla externa y otros periféricos para una experiencia de juego versátil.\n\nCaracterísticas\n- Puertos múltiples para conectividad\n- Diseño robusto y portátil\n- Compatible con diversas resoluciones de pantalla\n\nIdeal para\nUsuarios de Steam Deck que buscan expandir las posibilidades de su consola con una estación de conexión completa.",
                "stock": 1,
                "state": True,
                "promoted": True,
                "price": 99.99
                },
                {
                "name": "Joy-Con Zelda Skyward Sword",
                "img": "https://res.cloudinary.com/dshjlidcs/image/upload/v1738530369/Nintendo-switch-joy-con-the-legend-of-zelda-skyward-sword-hd_vaqp0a_xm6h77.jpg",
                "year": "2021",
                "brand": "Nintendo",
                "platform": "Nintendo Switch",
                "type": "Accesorio",
                "category":"accesorios",
                "description": "\nLos Joy-Con Zelda Skyward Sword son controles temáticos diseñados especialmente para los fans de la franquicia The Legend of Zelda.\n\nCaracterísticas\n- Diseño inspirado en Skyward Sword\n- Funcionalidades completas de los Joy-Con estándar\n- Conectividad inalámbrica confiable\n\nIdeal para\nJugadores de Nintendo Switch que buscan un toque único y personalizado en sus controles.",
                "stock": 1,
                "state": True,
                "promoted": True,
                "price": 120.00
                }
                ]
                }

        data_user = {"users": [

  {
    "email": "juanmorales@gmail.com",
    "password": "andalusa123",
    "userName": "juanito22",
    "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/premium-user.png",
    "description": "Soy un jugador ocasional que disfruta de juegos divertidos y accesibles. Busco consolas y juegos que me permitan relajarme después de un día largo. Siempre estoy buscando nuevos títulos que me sorprendan y entretengan.",
    "address": "calle Valladolid 54, 3-1",
    "postalCode":"28043",
    "city": "Cartagena",
    "following": [],
    "subscription": True,
    "role": "buyer"
  },
  {
    "email": "carmen.vazguez8@yahoo.com",
    "password": "bichota55.!x",
    "userName": "CarmenEspaña",
    "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/user.png",
    "description": "Soy un visitante ocasional que aún está explorando opciones. No tengo una preferencia clara por consolas o juegos específicos, pero me interesa conocer las opciones disponibles en el mercado. Estoy aquí para descubrir qué puede ofrecerme la plataforma sin comprometerme aún con ninguna compra.",
    "address": "calle Gonzalo Bilbao 8, 5-1",
    "postalCode":"48607",
    "city": "Sevilla",
    "following": [],
    "subscription": False,
    "role": "user"
  },
  {
    "email": "valentin.morreira@gmail.com",
    "password": "kkdad32d",
    "userName": "halamadrid10",
    "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/premium-user.png",
    "description": "Hola soy Valentin y mi pasión es coleccionar consolas y juegos retro. Me encanta descubrir rarezas y piezas únicas para añadir a mi colección. El valor sentimental y la historia detrás de cada consola me motiva a seguir ampliando mi biblioteca.",
    "address": "calle Villanueva 13, 1-2",
    "postalCode":"15297",
    "city": "Madrid",
    "following": [],
    "subscription": True,
    "role": ["buyer", "seller"]
  },
  {
    "email": "aarongarcia@gmail.com",
    "password": "a.garcia@17",
    "userName": "ClassicAaron",
    "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/premium-user.png",
    "description": "Soy Aarón, coleccionista de consolas retro y amante de los videojuegos de RPG. Siempre busco juegos y accesorios raros para ampliar mi colección.",
    "address": "Plaza Mayor 22, 4-A",
    "postalCode":"28040",
    "city": "Sevilla",
    "following": [],
    "subscription": True,
    "role": "buyer"
  },
  {
    "email": "andrea.retrogames@yahoo.com",
    "password": "gamerG1rl99",
    "userName": "PixelAndrea",
    "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/user.png",
    "description": "Holaaa, soy Andrea. Adoro los juegos de aventura y las consolas portátiles. Siempre estoy buscando ediciones especiales y colaboraciones únicas.",
    "address": "Av. Libertad 120, 3-C",
    "postalCode":"28200",
    "city": "Valencia",
    "following": [],
    "subscription": False,
    "role": ["buyer", "seller"]
  },
  {
    "email": "lucas.gamer@gmail.com",
    "password": "p@ssw0rd123",
    "userName": "retroLucas",
    "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/premium-user.png",
    "description": "Soy Lucas, un apasionado de los videojuegos clásicos y las consolas retro. Me encanta jugar y coleccionar piezas icónicas de la historia de los videojuegos.",
    "address": "Calle San Martín 45, 2-B",
    "postalCode":"24007",
    "city": "Barcelona",
    "following": [],
    "subscription": True,
    "role": "buyer"
  },
    {
      "email": "lauragaming@outlook.com",
      "password": "laura123",
      "userName": "LauraPlays",
      "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/premium-user.png",
      "description": "Soy Laura, una fanática de los juegos de simulación y los mundos abiertos. Me encanta perderme en historias envolventes y construir mi propio universo.",
      "address": "Calle Nueva 10, 2-1",
      "postalCode":"28028",
      "city": "Málaga",
      "following": [],
      "subscription": True,
      "role": "buyer"
    },
    {
      "email": "martin.retrogamer@gmail.com",
      "password": "retro1234",
      "userName": "MartinRetro",
      "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/user.png",
      "description": "Hola, soy Martin. Me apasionan los videojuegos arcade y las consolas clásicas. Siempre busco las mejores piezas de colección.",
      "address": "Calle Alhambra 3, 1-B",
      "postalCode":"28069",
      "city": "Granada",
      "following": [],
      "subscription": False,
      "role": ["buyer", "seller"]
    },
    {
      "email": "sofiagames@gmail.com",
      "password": "g4m3rGirl",
      "userName": "SofiaLover",
      "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/premium-user.png",
      "description": "Soy Sofía y amo los juegos indie y de plataformas. Siempre busco nuevas experiencias llenas de creatividad y diversión.",
      "address": "Calle del Sol 7, 4-C",
      "postalCode":"28500",
      "city": "Alicante",
      "following": [],
      "subscription": True,
      "role": "buyer"
    },
    {
      "email": "raul.collector@yahoo.com",
      "password": "collector2022",
      "userName": "RaulCollector",
      "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/premium-user.png",
      "description": "Raúl aquí. Me dedico a coleccionar juegos y accesorios únicos. Siempre estoy en la búsqueda de ediciones limitadas.",
      "address": "Paseo Marítimo 15, 1-A",
      "postalCode":"28672",
      "city": "Valencia",
      "following": [],
      "subscription": True,
      "role": "user"
    },
    {
      "email": "marianagamer@hotmail.com",
      "password": "mariGamer21",
      "userName": "MarianaAdventure",
      "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/user.png",
      "description": "Soy Mariana y me encanta jugar videojuegos cooperativos y explorar aventuras épicas con amigos.",
      "address": "Calle Libertad 22, 3-2",
      "postalCode":"40082",
      "city": "Madrid",
      "following": [],
      "subscription": False,
      "role": "buyer"
    },
    {
      "email": "albertogaming@live.com",
      "password": "gamerAlberto",
      "userName": "AlbertoGamer",
      "avatar": "https://res.cloudinary.com/dr0wlij0c/image/upload/v1736453861/web-illustrations/premium-user.png",
      "description": "Soy Alberto, amante de los juegos de estrategia y los retos mentales. Me encanta probar juegos que desafían mi lógica.",
      "address": "Av. Castilla 5, 1-A",
      "postalCode":"28940",
      "city": "Zaragoza",
      "following": [],
      "subscription": True,
      "role": "buyer"
    }
  ]
}
        for i in data['consoles']:
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
 
        return jsonify({'msg': 'ok'}) 