from flask import Flask, render_template, \
    request, redirect, flash, url_for
import sqlite3
import datetime
# create table posts (id integer primary key autoincrement, title varchar(150), description text, date text);


app = Flask(__name__)
app.secret_key = b'h46tvb4yn974ur'


@app.route('/allposts')
def all_posts():
    """shows all the posts from database"""
    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    cursor.execute('select * from posts')
    allposts = cursor.fetchall()
    connection.close()
    return render_template('index.html', allposts=allposts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    """adds new post to database"""
    if request.method == 'POST':
        connection = sqlite3.connect('blog.sqlite')
        cursor = connection.cursor()
        date = datetime.datetime.now()
        new_title = request.form['title']
        new_description = request.form['description']
        cursor.execute('insert into posts (title, description, date) values (?, ?, ?)',
                       [new_title, new_description, date])
        connection.commit()
        connection.close()
        flash("WOW! You added new post. It's amazing!")
        return redirect(url_for('all_posts'))
    else:
        return render_template('add.html')


@app.route('/update', methods=['GET', 'POST'])
def update_post():
    """updates post in database"""
    if request.method == 'POST':
        connection = sqlite3.connect('blog.sqlite')
        cursor = connection.cursor()
        id = request.form['id']
        new_title = request.form['title']
        new_description = request.form['description']
        cursor.execute('update posts set title = ?, description = ? where id = ?', [new_title, new_description, id])
        connection.commit()
        connection.close()
        return redirect(url_for('all_posts'))
    else:
        return render_template('edit.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_post():
    """deletes post from database"""
    if request.method == 'POST':
        connection = sqlite3.connect('blog.sqlite')
        cursor = connection.cursor()
        id = request.form['id']
        cursor.execute('delete from posts where id = ?', [id])
        connection.commit()
        connection.close()
        return redirect(url_for('all_posts'))
    else:
        return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)
