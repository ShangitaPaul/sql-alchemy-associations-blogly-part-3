from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

# Create Flask app
app = Flask(__name__)

# Configure SQLAlchemy to use PostgreSQL database named 'blogly'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

# Uncomment this line to turn Debug toolbar OFF
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""
    
    # Query and retrieve recent posts, ordered by creation date
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    
    return render_template('404.html'), 404


##############################################################################
# User routes

@app.route('/users')
def users_index():
    """Show a page with info on all users"""
    
    # Query and retrieve all users, ordered by last name and first name
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""
    
    return render_template('users/new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""
    
    # Create a new User object from form data
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    # Add new user to the database and commit changes
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""
    
    # Query and retrieve user by user ID, or return 404 if not found
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""
    
    # Query and retrieve user by user ID, or return 404 if not found
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""
    
    # Query and retrieve user by user ID, or return 404 if not found
    user = User.query.get_or_404(user_id)
    
    # Update user information based on form data
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    # Commit changes to the database
    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""
    
    # Query and retrieve user by user ID, or return 404 if not found
    user = User.query.get_or_404(user_id)
    
    # Delete user from the database and commit changes
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/users")


##############################################################################
# Post routes

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""
    
    # Query and retrieve user by user ID, or return 404 if not found
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""
    
    # Query and retrieve user by user ID, or return 404 if not found
    user = User.query.get_or_404(user_id)
    
    # Create a new Post object from form data
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    # Add new post to the database and commit changes
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""
    
    # Query and retrieve post by post ID, or return 404 if not found
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Shows a form to edit an existing post"""
    
    # Query and retrieve post by post ID, or return 404 if not found
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""
    
    # Query and retrieve post by post ID, or return 404 if not found
    post = Post.query.get_or_404(post_id)
    
    # Update post information based on form data
    post.title = request.form['title']
    post.content = request.form['content']

    # Commit changes to the database
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""
    
    # Query and retrieve post by post ID, or return 404 if not found
    post = Post.query.get_or_404(post_id)
    
    # Delete post from the database and commit changes
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")