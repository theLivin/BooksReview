import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#setup database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#insert books in books.csv into books table
def insert_books():
    books = csv.reader(open('books.csv'))
    for isbn, title, author, year in books:
        db.execute("INSERT INTO books(ISBN, TITLE, AUTHOR, YEAR) VALUES(:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()
 
#create tables
def create():
    db.execute("CREATE TABLE users( USER_ID SERIAL PRIMARY KEY, USERNAME VARCHAR NOT NULL, EMAIL VARCHAR NOT NULL, PASSWORD VARCHAR NOT NULL) ")
    
    db.execute("CREATE TABLE books( ISBN VARCHAR PRIMARY KEY, TITLE VARCHAR NOT NULL, AUTHOR VARCHAR NOT NULL, YEAR VARCHAR NOT NULL) ")
    
    db.execute("CREATE TABLE reviews( REVIEW_ID SERIAL PRIMARY KEY, BOOK_ISBN VARCHAR NOT NULL REFERENCES books, USER_ID INTEGER NOT NULL REFERENCES users, REVIEW VARCHAR, RATING INTEGER) ")
    db.commit();

if __name__ == '__main__':
    #create()
    #insert_books()