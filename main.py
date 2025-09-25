from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

products=[Product(id=1,name="phone",description="budget",price=99,quantity=10),
          Product(id=2,name="laptop",description="gaming",price=999,quantity=6)]


@app.get('/')
def greet():
    return 'Welcome to Praveen Track'

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db=session()
    count=db.query(database_models.Product).count
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
init_db()

@app.get('/products')
def get_all_products(db:Session=Depends(get_db)):
    db_products=db.query(database_models.Product).all()
    return db_products

@app.get('/products/{id}')
def get_product_by_id(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    return 'Product not found'

@app.post('/products')
def add_products(product:Product,db:Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put('/products/{id}')
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "Product added"
    else:    
        return "No product found"

@app.delete('/products')
def delete_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    else:
        return "product Not found"
    