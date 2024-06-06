"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

# App routes
# Homepage:
@app.route("/")
def root():
    """Homepage render"""
    return render_template("index.html")



# GET request for all cupcakes:
@app.route("/api/cupcakes")
def list_cupcakes():
    "Returns data on all cupcakes from db"
    
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)



# POST request to add/create a cupcake to the database
@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    "Add a new cupcake to db, and return info about it"
    
    data = request.json
    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()
    
    # return HTTP 201 Created Status to every POST request 
    return (jsonify(cupcake=cupcake.to_dict()), 201)



# GET request for cupcake data based off of ID
@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    "Get data in return based on a spcefic cupcake id"
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())



#PATCH request to update a part of a spcefic cupcake considering the cupcake_id
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    #PATCH request to update a cupcake based on passed cupcake_id. Return data on updated cupcake
    
    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())


# DELETE request to delete a cupcake from the db based on cupcake_id
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    "Delate a cupcake from a database and return a confirmation message"
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Cupcake has been Deleted")


    
    

    
    

