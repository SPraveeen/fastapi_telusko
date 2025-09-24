from fastapi import FastAPI
from models import Product

app=FastAPI()

products=[Product(id=1,name="phone",description="budget",price=99,quantity=10),
          Product(id=2,name="laptop",description="gaming",price=999,quantity=6)]

@app.get('/')
def greet():
    return 'Welcome to Praveen Track'

@app.get('/products')
def get_all_products():
    return products

@app.get('/product/{id}')
def get_product_by_id(id:int):
    for product in products:
        if product.id==id:
            return product
    return 'Product not found'

@app.post('/product')
def add_products(product:Product):
    products.append(product)
    return product

