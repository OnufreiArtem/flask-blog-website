from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import session

import datetime

from blogger import app
from .models import User, Post, db

'''
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404_page.html'), 404

app.register_error_handler(404, page_not_found)
'''
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    
    if session.get('user') == None:
        if request.method == 'POST':
            user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
            if not user: 
                return render_template('signin.html', failed=True)
            else:
                session['user'] = user.to_json()
                return redirect('home')
        elif request.method == 'GET':
            return render_template('signin.html')
    else:
        return redirect('home')
        
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if session.get('user') == None:
        if request.method == 'POST':
            wrong_username = User.query.filter_by(username=request.form['username']).first() != None
            wrong_password = len(request.form['password']) < 8

            if wrong_username or wrong_password:
                return render_template('signup.html', username_failed=wrong_username, password_failed=wrong_password)
            else:
                new_user = User(request.form['name'], request.form['surname'], request.form['username'], request.form['password'])
                db.session.add(new_user)
                db.session.commit()
                session['user'] = new_user.to_json()
                return redirect('home')
        elif request.method == 'GET':
            return render_template('signup.html')
    else:
        return redirect('home')
    
    return render_template('signup.html')


@app.route('/addPost', methods=['GET', 'POST'])
def add_post():
    current_user = session.get('user')
    if current_user != None:
        if request.method == 'POST':
            db.session.add(Post(current_user['id'], request.form['post_title'], request.form['post_content']))
            db.session.commit()
            return redirect('home')
        elif request.method == 'GET':
            return render_template('post_base.html', user=current_user, form_action="addPost", post=None, form_title="Add Post", form_submit_text="Add")
    else:
        return redirect('signin')


@app.route('/', methods=['GET'])
def move_home():
    return redirect('home')
    
@app.route('/home', methods=['GET'])
def home():
    current_user = session.get('user')
    return render_template('home.html', user=current_user, posts=Post.query.order_by(Post.date_of_post.desc()).all())

@app.route('/delete/<int:postid>', methods=['GET'])
def delete_post(postid):
    user = session.get('user')
    post = Post.query.filter_by(id=postid).first()
    if user != None and post != None and user['id'] == post.author_id:
        db.session.delete(post)
        db.session.commit()
    return redirect('/home')   



@app.route('/edit/<int:postid>', methods=['GET', 'POST'])
def post_edit(postid):
    current_user = session.get('user')
    post = Post.query.filter_by(id=postid).first()
    if current_user != None and post.author_id == current_user['id']:
        if request.method == "GET":
            return render_template('post_edit.html', user=session.get('user'), post=post, form_action="edit/%s" % str(postid), form_title="Add Post", form_submit_text="Edit")
        elif request.method == "POST":
            post.title = request.form['post_title']
            post.content = request.form['post_content']
            post.date_of_post = datetime.datetime.now()
            db.session.commit()
            return redirect('/home')
    else:
        return redirect('/posts/%s' % str(postid))


@app.route('/posts/<int:postid>', methods=['GET'])
def post_view(postid):
    return render_template('post_view.html', user=session.get('user'), post=Post.query.filter_by(id=postid).first())