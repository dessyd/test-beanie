
from typing import Optional
from pydantic import BaseModel
from beanie import Document, Indexed, init_beanie
import asyncio, motor

from config import settings

class Category(BaseModel):
    name: str
    description: str

class Product(Document):
    name: str                          # You can use normal types just like in pydantic
    description: Optional[str] = None
    price: Indexed(float)              # You can also specify that a field should correspond to an index
    category: Category                 # You can include pydantic models as well

# Beanie is fully asynchronous, so we will access it from an async function
async def example():
    MONGO_DETAILS = f'{settings.database_driver}://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}'
    MONGO_DATABASE = f'{settings.database_name}'
    # Beanie uses Motor under the hood 
    print('Connecting ...')
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    mongo_database = client[MONGO_DATABASE]

    print('Initializing ...')
    print(mongo_database)

    # Init beanie with the Product document class
    await init_beanie(database=mongo_database, document_models=[Product])

    print('Creating items')
    chocolate = Category(name="Chocolate", description="A preparation of roasted and ground cacao seeds.")
    # Beanie documents work just like pydantic models
    tonybar = Product(name="Tony's", price=5.95, category=chocolate)
    # And can be inserted into the database
    print('Inserting ...')
    await tonybar.insert() 

    print('Finding ...')
    # You can find documents with pythonic syntax
    product = await Product.find_one(Product.price < 10)

    print('Updating ...')
    # And update them
    await product.set({Product.name:"Gold bar"})

asyncio.run(example())