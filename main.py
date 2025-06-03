# to run, in terminal run: uvicorn [filename]:[appname] --reload
    # uvicorn main:app --reload
# press link

# note anytime changes are made to the file, the app refreshes
# routes will be through the url when something is entered after the /

# import fastapi
from fastapi import FastAPI
# allows FastAPI to read JSON, convert types, validate data, and return errors
from pydantic import BaseModel

# use it to create a new app
app = FastAPI()

# empty list of items to be populated
items = []

# define model for input
class Item(BaseModel):
    name : str

@app.get("/")   # and app decorator that defines a path for the http get method
def root():     # when someone calls line above, this function is called
    return {"Hello" : "World"}

# routes are used to define different urls the app should respond to
# routes handle different interactions

# new endpoint to add to item list, using an http post request to the /items path
# to test run: curl -X POST -H "Content-Type: application/json" -d '{"name": "apple"}' http://127.0.0.1:8000/items
@app.post("/items")
def create_item(item : Item): # item is the input
    items.append(item.name)
    return {"item added: " : item.name, "current items: " : items}

# retrives item at a specific index
# to test run: curl http://127.0.0.1:8000/items/0
@app.get("/items/{item_id}")    # {} b/c its a variable
def get_item(item_id : int):
    if item_id < 0 or item_id >= len(items):
        return {"Error: \"Invalid item_id\""}
    item = items[item_id]
    return item