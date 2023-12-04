from flask import Flask, render_template, jsonify, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship, sessionmaker, joinedload
from sqlalchemy.orm.exc import NoResultFound

DATABASE_URL = "sqlite:///./cart.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)

    # Establish a relationship with the CartItem model
    items = relationship('CartItem', back_populates='cart')

    def calculate_sum(self):
        return sum(item.product.price * item.quantity for item in self.items)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    price = Column(Float, nullable=False)

    # Establish a relationship with the CartItem model
    cart_items = relationship("CartItem", back_populates="product")

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    
    # Establish a relationship with the Product model
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="cart_items")

    # Establish a relationship with the Cart model
    cart_id = Column(Integer, ForeignKey('cart.id'))
    cart = relationship('Cart', back_populates='items')

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


# Populate the database with dummy data
def seed_database():
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a dummy user and cart
    cart_id = 1
    dummy_cart = Cart(user_id=cart_id)
    session.add(dummy_cart)
    session.commit()
    session.refresh(dummy_cart)

    # Create dummy products and add them to the cart
    apple = Product(name="apple", price=5)
    orange = Product(name="orange", price=6)

    session.add(apple)
    session.add(orange)
    session.commit()
    session.refresh(apple)
    session.refresh(orange)

    # Create dummy cart items and add them to the cart
    cart_apple = CartItem(quantity=2, product=apple, cart=dummy_cart)
    cart_orange = CartItem(quantity=1, product=orange, cart=dummy_cart)

    session.add(cart_apple)
    session.add(cart_orange)
    session.commit()
    session.close()


app = Flask(__name__)


@app.route('/cart/<int:cart_id>')
def display_cart(cart_id):
    session = Session()
    cart = session.query(Cart).filter(Cart.user_id == cart_id).options(joinedload(Cart.items).joinedload(CartItem.product)).first()
    session.close()

    if cart:
        cart_items = cart.items
        return render_template('shopping_cart.html', cart_items=cart_items, cart=cart)
    else:
        return "Cart not found", 404


@app.route('/add_item/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    session = Session()
    item = session.query(CartItem).filter_by(id = item_id).options(joinedload(CartItem.cart)).first()

    if item:
        product_name = item.product.name
        item.quantity += 1
        session.refresh(item.cart)
        session.commit()
        session.refresh(item)
        session.close()
        return render_template('item_added.html', product_name=product_name, cart_id=item.cart.id)
    else:
        return "Item not found", 404


@app.route('/remove_item/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    session = Session()
    try:
        item = session.query(CartItem).filter_by(id=item_id).one()
        product_name = item.product.name
        cart = item.cart
        item.quantity -= 1

        if item.quantity == 0:
            session.delete(item)

        session.refresh(cart)
        session.commit()
        return render_template('item_removed.html', product_name=product_name, cart_id=cart.id)
    except NoResultFound:
        session.rollback()
        return "Item not found", 404
    finally:
        session.close()


if __name__ == '__main__':
    seed_database()
    app.run(debug=True)
