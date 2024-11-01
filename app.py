from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from api import AmazonScraper

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # Using product ID from URL
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    review_count = db.Column(db.Integer, nullable=True)
    availability = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    explore_link = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('test.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    product_url = request.form.get('product_link')
    scraper = AmazonScraper()
    product_info = scraper.get_product_details(product_url)

    if product_info:
        new_product = Product(
            id=product_info.get('id'),
            name=product_info.get('name'),
            price=product_info.get('price'),
            rating=product_info.get('rating'),
            review_count=product_info.get('review_count'),
            availability=product_info.get('availability'),
            description=product_info.get('description'),
            image_url=product_info.get('image_url'),
            explore_link=product_url
        )
        db.session.add(new_product)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_product/<string:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
