import os

from flask import Flask, session, render_template, request
#from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#index page
@app.route("/")
def index():
    return render_template("index.html")

#submit registration
@app.route("/login", methods=["POST"])
def register():
    username = request.form.get("username")
    return render_template("success.html")

#logged in - show all books page
@app.route('/books')
def books():
    #search = str(request.args.get('search'))  #get search query string
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", books=books)
    
#view book details
@app.route('/book/<string:isbn>')
def book(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    if book is None:
        return render_template("error.html", msg="No book with such ISBN")
    reviews = db.execute("SELECT * FROM reviews").fetchall()
    users = db.execute("SELECT username,email FROM users").fetchall()
    return render_template("book.html", book=book, reviews=reviews, users=users)

if __name__ == "__main__":
    app.run(debug=True)