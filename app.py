from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    intro = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/news')
def news():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('news.html', posts=posts)

@app.route('/news/<int:id>')
def post_detail(id):
    post = Post.query.get(id)
    return render_template('post-detail.html', post=post)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/create-post', methods=['POST', 'GET'])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        post = Post(title=title, intro=intro, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/news')
        except:
            return "Unexcepted error"
    else:
        return render_template('create-post.html')


@app.route('/news/<int:id>/delete')
def post_delete(id):
    post = Post.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/news')
    except:
        return "unexcepted error"

@app.route('/news/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    post = Post.query.get(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.intro = request.form['intro']
        post.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/news')
        except:
            return "Unexcepted error"
    else:
        return render_template('update-post.html')






if __name__ == "__main__":
    app.run(debug=True)