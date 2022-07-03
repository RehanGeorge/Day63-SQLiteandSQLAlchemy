from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
Bootstrap(app)
db = SQLAlchemy(app)

# all_books = []

#Create Table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f"<Book {self.title}>"

#Create Database - One Time
# db.create_all()

class BookForm(FlaskForm):
    name = StringField("Book Name", validators=[DataRequired()])
    author = StringField("Book Author", validators=[DataRequired()])
    rating = SelectField("Rating", choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", data=all_books)

@app.route("/add", methods=["GET", "POST"])
def add():
    add_book = BookForm()
    if add_book.validate_on_submit():
        # new_book = {"title": add_book.name.data, "author": add_book.author.data, "rating": add_book.rating.data}
        # all_books.append(new_book)
        # print(all_books)
        new_book = Book(title=add_book.name.data, author=add_book.author.data, rating=add_book.rating.data)
        db.session.add(new_book)
        db.session.commit()
        all_books = db.session.query(Book).all()
        print(all_books)
        return redirect(url_for('home'))
    return render_template("add.html", form=add_book)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        #UPDATE RECORD
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit_rating.html", book=book_selected)

@app.route("/delete")
def delete():
    book_id = request.args.get("id")
    print(book_id)

    #DELETE RECORD BY ID
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)