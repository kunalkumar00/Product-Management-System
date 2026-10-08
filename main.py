from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import session, engine
from models import Products
import database_models
from sqlalchemy.orm import Session
app =FastAPI()
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.11:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = False,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

database_models.Base.metadata.create_all(bind = engine)

@app.get("/")

# def greet():
#     return "Welcome to Kunal Trac"
# products = [
#     Products(id=1,name="Phone",description="budget phone",price=99,quantity=50),
#     Products(id=2,name ="laptop",description="gaming laptop",price=30000,quantity=30),
#     Products(id=5,name="Pen",description="A blue ink pen",price=10,quantity=100),
#     Products(id=6,name="Table",description="Gaming table",price=2000,quantity=20)
# ]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    count = db.query(database_models.Products).count
    
    if count == 0:
        for product in Products:
            db.add(database_models.Products(**product.model_dump()))
        db.commit()
init_db()  
    
@app.get("/products/")
def get_all_products(db : Session = Depends(get_db)):
    db_products = db.query(database_models.Products).all()
    return db_products


    
@app.get("/products/{id}")
def get_product_by_id(id: int, db : Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        return db_product
    return "Product not found"


@app.post("/products/")
def add_product(product: Products, db : Session = Depends(get_db)):
    db.add(database_models.Products(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update(id: int, product : Products, db : Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated"
    else:
        return "No product Found"

@app.delete("/products/{id}")
def delete(id: int, db : Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    else:
        return "Product not found"