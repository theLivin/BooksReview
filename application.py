import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Index page
@app.route("/")
def index():
    # # User already logged in
    if session.get("users_id"):
        books = db.execute("SELECT * FROM books").fetchall()
        return render_template("books.html", books=books)
    return render_template("index.html")

# Submit registration
@app.route("/completeregistration", methods=["POST","GET"])
def register():
    # User already logged in
    if session.get("users_id"):
        books = db.execute("SELECT * FROM books").fetchall()
        return render_template("books.html", books=books)

    if request.method == "POST":
        # Get registration details
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")

        # Check if username already exists
        user_exists = db.execute("SELECT * FROM users WHERE username=:username", {"username": username}).fetchone();
        if user_exists:
            return render_template("index.html", rmsg="username has already been taken.")

        # Check if passwords match
        elif password != cpassword:
            return render_template("index.html", rmsg="passwords do no match.")
            
        # Add new user
        if db.execute("INSERT INTO users(username,email,password) VALUES(:username,:email,:password)", {"username": username, "email": email, "password": password}):
            # Commit insert query
            db.commit()
            return render_template("success.html")

    # If error/ making GET request
    return render_template("error.html",msg="An Error Has Occured. Please try again later")

# Log user in and display books
@app.route('/allbooks',methods=["POST","GET"])
def login():
    # If request is post
    if request.method == "POST":
        # Get form inputs
        username = request.form.get("username")
        password = request.form.get("password")

        # Get user id with database
        user_id = db.execute("SELECT user_id FROM users WHERE username=:username AND password=:password", {"username": username, "password": password}).fetchone()

        # User does not exist
        if not user_id:
            return render_template("index.html", lmsg="invalid username or password.")

        # Log user in if user exists
        #if session["users_id"] is None:
        #    session["users_id"].append(user_id)
        session["users_id"] = user_id

    if session.get("users_id"):
        books = db.execute("SELECT * FROM books").fetchall()
        return render_template("books.html", books=books)

    # If user is not logged in
    return render_template("index.html",lmsg="Problem logging in")

@app.route('/logout')
def logout():
    if session.pop("users_id",None):
        return render_template('index.html')
    return "Logout Unsucessful"

    
# View book details
@app.route('/book/<string:isbn>')
def book(isbn):
    # User not logged in
    if session.get("users_id") is None:
        return render_template("index.html", lmsg="user authentication required")
    
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    if book is None:
        return render_template("error.html", msg="No book with such ISBN")
    reviews = db.execute("SELECT * FROM reviews ").fetchall()
    users = db.execute("SELECT username,email FROM users").fetchall()
    return render_template("book.html", book=book, reviews=reviews, users=users)

@app.route('/search')
def search():
    # Get search query string
    search = str(request.args.get('search'))
    books = db.execute("SELECT * FROM books WHERE isbn=:isbn OR title LIKE :title OR author LIKE :author OR  year =:year",{"isbn":search, "title":search, "author":search, "year":search}).fetchall()
    return render_template('books.html',books=books)

if __name__ == "__main__":
    app.run(debug=True)
