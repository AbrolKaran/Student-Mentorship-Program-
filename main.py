from app import app
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1') 

db=SQLAlchemy(app)