from flask import Flask, render_template, request, redirect
import sqlite3
from models.blog_post import BlogPost
import os

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
print(f"Absolute path to the script's directory: {base_dir}")

db_folder = os.path.join(base_dir, "database")
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

db_path = os.path.join(db_folder, "blogpost.db")


db_connection = sqlite3.connect(db_path, check_same_thread=False)
db_cursor = db_connection.cursor()

def __create_blog_table():
    db_connection.execute('''
    CREATE TABLE BLOGS
        (NAME TEXT NOT NULL,
        TITLE TEXT NOT NULL,
        CONTENT TEXT NOT NULL);
    ''')
    db_connection.commit()


def __add_blogpost(name, title, content):
    db_connection.execute(f"""INSERT INTO BLOG(NAME,TITLE,CONTENT)
                        VALUES('{name}', '{title}', '{content}')""")
    db_connection.commit()


def __get_all_blogs():
    return list(db_connection.execute("""SELECT * FROM BLOGS"""))


@app.route('/')
@app.route('/index')
def default_route():
    list_blogs = __get_all_blogs()
    print(list_blogs)
    return render_template('index.html', result=list_blogs)

@app.route('/add-blog', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        if db_connection is not None:
            try:
                __add_blogpost(request.form['name'], request.form['title'], request.form['content'])
                list_blogs = __get_all_blogs()
                return render_template('index.html', result=list_blogs)
            except Exception as e:
                print(e)
                print("Error while inserting information")
        else:
            return redirect('/')
    else:
        list_blogs = __get_all_blogs()
        return render_template('index.html', result=list_blogs)
    return redirect('/')



if __name__ == '__main__':
    try:
        __create_blog_table()
    except Exception:
        print("Table already exists")
    app.run(debug=True)

