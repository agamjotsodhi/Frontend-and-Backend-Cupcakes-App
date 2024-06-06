# """Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

PLACEHOLDER_IMG = "https://static.vecteezy.com/system/resources/previews/007/634/579/original/cupcake-logo-icon-design-template-free-vector.jpg"

"Cupcake model guidelines, id - auto incr. id's, flavor - mandatory text, size - mandatory text, rating - mandatory text, image - mandatory text "

class Cupcake(db.Model):
    """Cupcake db model"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=PLACEHOLDER_IMG)


    def to_dict(self):
        """Serialize/make cupcake to a dict of cupcake info"""
        
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }
    

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
    
    
