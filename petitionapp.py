from flask import Flask 
from flask import render_template 
from flask import request
from flask.helpers import url_for 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Count():
    counter = 0
increase = Count()

class UsersData(db.Model):
    __tablename__ = 'UsersData'
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(30),index=True,unique=True)
    sur_name = db.Column(db.String(30),index=True)

@app.route('/')
def story_home():
    user = UsersData.query.all()
    return render_template('home.html',userinfo = user,signs=increase.counter)

@app.route('/sign',methods = ["POST","GET"])
def story_sign():
    if request.method == "POST": 
        new_users = UsersData(user_name=request.form["nm"],sur_name=request.form["sname"])
        db.session.add(new_users)
        db.session.commit()
        if new_users:
            increase.counter+=1
        return redirect(url_for('story_home'))
    else:
        return render_template('sign_page.html')

@app.route("/remove/<int:data_id>")
def delete(data_id):
    tdata = UsersData.query.filter_by(id=data_id).first()
    db.session.delete(tdata)
    db.session.commit()
    if tdata:
        increase.counter-=1
    return redirect(url_for("story_home"))


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)