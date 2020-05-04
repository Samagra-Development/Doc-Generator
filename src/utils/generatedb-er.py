from eralchemy import render_er
from db.config import Config
import os.path

image_path = os.path.dirname(__file__)+'/../db/docs/'
## Draw from SQLAlchemy base
render_er(Config.SQLALCHEMY_DATABASE_URI, image_path+'erd_from_sqlalchemy.png')