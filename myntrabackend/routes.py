from flask import Blueprint, jsonify, request
from .models import db, User, Pin, Board,Product
from datetime import datetime

bp = Blueprint('api2', __name__)

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.username for user in users])

@bp.route('/users/search', methods=['GET'])
def get_user_by_email():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter is required'}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'user_id': user.id, 'username': user.username})
    else:
        return jsonify({'error': 'User not found'}), 404



@bp.route('/createusers', methods=['POST'])
def create_user():
    data = request.json
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/pins', methods=['GET'])
def get_pins():
    pins = Pin.query.all()
    return jsonify([pin.title for pin in pins])

from flask import abort

@bp.route('/createpins', methods=['POST'])
def create_pin():
    data = request.json
    board_id = data.get('board_id')

    # Check if the board exists
    board = Board.query.get(board_id)
    if not board:
        return jsonify({'error': 'Board not found'}), 404
   
    # Create the pin if board exists
    pin = Pin(
       
        title=data['title'],
        image_url=data['image_url'],
        description=data.get('description'),
        user_id=data['user_id'],
        board_id=board_id,
        myntra=1,
        myntraid=data["myntraid"]
    )

    db.session.add(pin)
    db.session.commit()

    return jsonify({'message': 'Pin created successfully'}), 201


@bp.route('/boards', methods=['GET'])
def get_boards():
    boards = Board.query.all()
    boards_data = []
    for board in boards:
        board_pins = Pin.query.filter_by(board_id=board.id).all()
        board_data = {
            'id':board.id,
            'board_name': board.name,
            'pins': [{'id':pin.id,'title': pin.title, 'image_url': pin.image_url,'myntra':pin.myntra,'myntraid':pin.myntraid} for pin in board_pins]
        }
        boards_data.append(board_data)
    return jsonify(boards_data)




@bp.route('/createboards', methods=['POST'])
def create_board():
    data = request.json
    board = Board(name=data['name'], user_id=data['user_id'])
    db.session.add(board)
    db.session.commit()
    return jsonify({'message': 'Board created successfully'}), 201

@bp.route('/users/<int:user_id>/pins', methods=['GET'])
def get_user_pins(user_id):
    user = User.query.get_or_404(user_id)
    pins = Pin.query.filter_by(user_id=user.id).all()
    return jsonify([{"id":pin.id,'title': pin.title, 'image_url': pin.image_url,'myntra':pin.myntra,'myntraid':pin.myntraid} for pin in pins])



@bp.route('/users/<int:user_id>/boardsuser', methods=['GET'])
def get_user_boards(user_id):
    user = User.query.get_or_404(user_id)
    boards = Board.query.filter_by(user_id=user.id).all()
    
    boards_data = []
    for board in boards:
        board_pins = Pin.query.filter_by(board_id=board.id).all()
        board_data = {
            'id':board.id,
            'board_name': board.name,
            'pins': [{'title': pin.title, 'image_url': pin.image_url,'myntra':pin.myntra,'myntraid':pin.myntraid} for pin in board_pins]
        }
        boards_data.append(board_data)
    
    return jsonify(boards_data)

@bp.route('/products', methods=['GET'])
def get_products():
    pins = Product.query.all()
    return jsonify([{"id":pin.id,'price':pin.price,'title': pin.name, 'image_url': pin.image_url,"desc":pin.description} for pin in pins])

@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    # Query the product with the specified ID
    pin = Product.query.get_or_404(id)
    # Return the product as JSON
    return jsonify({
        "id": pin.id,
        "price": pin.price,
        "title": pin.name,
        "image_url": pin.image_url,
        "desc": pin.description
    })

@bp.route('/search/products', methods=['GET'])
def search_products():
    search_term = request.args.get('query', '')
    products = Product.query.filter(Product.name.ilike(f'%{search_term}%')).all()
    products_data = [{'id': product.id, 'title': product.name, 'image_url': product.image_url, 'price': product.price} for product in products]
    return jsonify(products_data)
