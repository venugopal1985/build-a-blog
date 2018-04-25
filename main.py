from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:3306/buildblog'
app.config['SQLALCHEMY_ECHO']=True
db=SQLAlchemy(app)

class Blog(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120))
    blogpost=db.Column(db.String(255))

    def __init__(self, title, blogpost):
        self.title=title
        self.blogpost=blogpost

def get_allblogs():
    return Blog.query.all()

@app.route('/', methods=['POST', 'GET'])
def index():

    title_error=''
    blogpost_error=''
    title=''
    blogpost=''

    if request.method == 'POST':
        title=request.form['title']
        blogpost=request.form['blogpost']
        if title=='':
            title_error='<------Title cannot be blank.  Please enter a title'
        if blogpost=='':
            blogpost_error='<-----this cannot be blank.  Try again!'
        if not title_error and not blogpost_error:
            new_blog=Blog(title, blogpost)
            db.session.add(new_blog)
            db.session.commit()
            new_id=new_blog.id
            return redirect('/single_blog?id={0}'.format(new_id))

    return render_template('index.html', ptitle='Venublogpage', title=title, blogpost=blogpost, title_error=title_error, blogpost_error=blogpost_error)

@app.route('/allblogs', methods=['POST', 'GET'])
def blog():

    return render_template('allblogs.html',title="venublog - All Entries", allblogs=get_allblogs())

@app.route('/single_blog', methods=['POST', 'GET'])
def singleblog():
    b_id=request.args.get('id')
    spost = Blog.query.filter_by(id=b_id).first()
    return render_template('single_blog.html',pagetitle="Single Blog Details", title=spost.title, post=spost.blogpost)

if __name__=='__main__':
    app.run()
