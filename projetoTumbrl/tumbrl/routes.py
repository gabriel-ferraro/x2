from tumbrl import app
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, login_user, current_user
from tumbrl.models import load_user
from tumbrl.forms import FormLogin, FormCreateNewAccount, FormCreateNewPost
from tumbrl import bcrypt
from tumbrl.models import User, Posts, Like, Comment
from tumbrl import database


import os
from werkzeug.utils import secure_filename


# @app.route('/home')
@app.route('/', methods=['POST', 'GET'])
def homepage():
    _formLogin = FormLogin()
    if _formLogin.validate_on_submit():
        userToLogin = User.query.filter_by(email=_formLogin.email.data).first()
        if userToLogin and bcrypt.check_password_hash(userToLogin.password, _formLogin.password.data):
            login_user(userToLogin)
            return redirect(url_for("profile", user_id=userToLogin.id))

    return render_template('home.html', textinho='TOP', form=_formLogin)


@app.route('/new', methods=['POST', 'GET'])
def createAccount():
    _formCreateNewAccount = FormCreateNewAccount()

    if _formCreateNewAccount.validate_on_submit():
        password = _formCreateNewAccount.password.data
        password_cr = bcrypt.generate_password_hash(password)
        # print(password)
        # print(password_cr)

        newUser = User(
            username=_formCreateNewAccount.usarname.data,
            email=_formCreateNewAccount.email.data,
            password=password_cr
        )

        database.session.add(newUser)
        database.session.commit()

        login_user(newUser, remember=True)
        return redirect(url_for('profile', user_id=newUser.id))

    return render_template('new.html', form=_formCreateNewAccount)


@app.route('/perry')
def perry():
    return render_template('perry.html')


@app.route('/teste')
def teste():
    return render_template('teste.html')


@app.route('/profile/<user_id>', methods=['POST', 'GET'])
@login_required
def profile(user_id):
    if int(user_id) == int(current_user.id):
        _formCreateNewPost = FormCreateNewPost()

        if _formCreateNewPost.validate_on_submit():
            photo_file = _formCreateNewPost.photo.data
            photo_name = secure_filename(photo_file.filename)

            photo_path = f'{os.path.abspath(os.path.dirname(__file__))}/{app.config["UPLOAD_FOLDER"]}/{photo_name}'
            photo_file.save(photo_path)

            _postText = _formCreateNewPost.text.data

            newPost = Posts(post_text=_postText, post_img=photo_name, user_id=int(current_user.id))
            database.session.add(newPost)
            database.session.commit()

        return render_template('profile.html', user=current_user, form=_formCreateNewPost)

    else:
        _user = User.query.get(int(user_id))
        reposts = _user.reposts
        return render_template('profile.html', user=_user, reposts=reposts, form=None)


@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Posts.query.get(post_id)
    if post is None:
        flash('Post não encontrado.')

    if Like.query.filter_by(user_id=current_user.id, post_id=post.id).first():
        """
        """

    else:
        like = Like(user_id=current_user.id, post_id=post.id)
        database.session.add(like)
        post.likes += 1  # Incrementa o número de likes no post
        database.session.commit()
    return redirect(url_for('profile', user_id=post.user_id))


@app.route('/repost/<int:post_id>', methods=['POST'])
@login_required
def repost(post_id):
    post = Posts.query.get(post_id)
    if post is None:
        flash('Post não encontrado.')
    # Verifique se o usuário já fez repost do post
    if current_user in post.reposted_by:
        flash('Você já repostou este post.')
    else:
        # Adicione o usuário à lista de reposts do post
        post.reposted_by.append(current_user)
        database.session.commit()
    return redirect(url_for('profile', user_id=post.user_id))


@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Posts.query.get(post_id)
    if post is None:
        flash('Post não encontrado.')

    text = request.form.get('text')
    if not text:
        flash('O comentário não pode estar vazio')

    comment = Comment(text=text, user_id=current_user.id, post_id=post.id)
    database.session.add(comment)
    database.session.commit()


@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Posts.query.get(post_id)
    if post is None:
        flash('Post não encontrado')


    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'O comentário não pode estar vazio'}), 400

    comment = Comment(text=text, user_id=current_user.id, post_id=post.id)
    database.session.add(comment)
    database.session.commit()

    return jsonify({'success': 'Comentário adicionado com sucesso'}), 200
