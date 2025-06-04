# to run, in terminal run: uvicorn [filename]:[appname] --reload
    # uvicorn main:app --reload
# press link
# can also test at: http://127.0.0.1:8000/docs

# note anytime changes are made to the file, the app refreshes
# routes will be through the url when something is entered after the /

# import fastapi and error handler
from fastapi import FastAPI, HTTPException
# allows FastAPI to read JSON, convert types, validate data, and return errors
from pydantic import BaseModel

# use it to create a new app
app = FastAPI()

# empty list of items to be populated
items = []

# define model for input
class Item(BaseModel):
    name : str  # required

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
    return {"item added: " : item.name, "current list: " : items}

# retrives item at a specific index
# to test run: curl http://127.0.0.1:8000/items/0
@app.get("/items/{item_id}", response_model = Item)    # {} b/c its a variable
def get_item(item_id : int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code = 404, detail = f"Item {item_id} not found.")
    
    item = items[item_id]
    return {"item at specified index: " : item, "current list: " : items}

# return the entire list in left empty, else return the user-specified number of items starting fromm the top
# to test the whole list returning, run: curl "http://127.0.0.1:8000/items"
# to test returning a specific number: curl "http://127.0.0.1:8000/items?count=1"
@app.get("/items", response_model = list[Item])
def get_list(count : int = None):   # None tells FastAPI that count is optional and that the programmer will handle it if not provided
    if count == None:   # return the whole list
        return items
    if count < 0 or count > len(items):
        raise HTTPException(status_code=404, detail = f"Out of bounds.")
    return items[0:count]