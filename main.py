from flask import Flask,render_template,url_for,redirect,flash,request
from flask_login import login_user,LoginManager,login_required,current_user,logout_user,UserMixin
from flask_wtf import FlaskForm
from wtforms import Form,StringField,PasswordField,SubmitField,IntegerField,SelectField,DecimalField
from wtforms.validators import DataRequired
login_manager=LoginManager()
app=Flask(__name__)
login_manager.init_app(app)
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
db=SQLAlchemy(app)
login2=False
app.config['SECRET_KEY'] = "vaibhavbhai9599"
# engine=SQLAlchemy.create_engine('sqlite:///cafes.sqlite')
# connection = engine.connect()
metadata = db.MetaData()
# census = db.Table('cafe', metadata, autoload=True, autoload_with=engine)
current_id=None
class RegisterForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password - Minimum 8 characters")
    submit=SubmitField("Register")
class LoginForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password")
    submit=SubmitField("Login")
class Tasks(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,nullable=True)
    u_tasks = db.Column(db.String(500), nullable=True)
    c_tasks=db.Column(db.String(500),nullable=True)
db.create_all()

class Users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(200),nullable=False)
db.create_all()
@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)

new_task=Tasks(id=1,user_id=0,u_tasks='',c_tasks='')
# db.session.add(new_task)

@app.route("/",methods=["GET","POST"])
def main():
    if request.method=="GET":
        if current_user.is_authenticated:
            print(current_user.id)
            current_tasks=Tasks.query.filter_by(user_id=current_user.id).first()
            tasks_list=current_tasks.u_tasks.split(",")
            c_tasks_list=current_tasks.c_tasks.split(",")

            print("Current user id is ",current_user.id)
            return render_template("index.html",ut=tasks_list[:],l=len(tasks_list),ct=c_tasks_list,l2=len(c_tasks_list))
        else:
            t=Tasks.query.filter_by(user_id=0).first()
            tasks_list=t.u_tasks.split(',')
            c_tasks_list=t.c_tasks.split(",")
            return render_template("index.html",ut=tasks_list[:],l=len(tasks_list),ct=c_tasks_list,l2=len(c_tasks_list))
    else:
        if current_user.is_authenticated:
            all_tasks=db.session.query(Tasks).all()
            print(len(all_tasks))
            tt=Tasks.query.filter_by(user_id=current_user.id).first()
            ttt=str(tt.u_tasks)+ f',{request.form.get("task")}'
            tt.u_tasks=ttt
            db.session.commit()
            current_tasks = Tasks.query.filter_by(user_id=current_user.id).first()
            tasks_list = current_tasks.u_tasks.split(',')
            c_tasks_list=current_tasks.c_tasks.split(",")
            print("Current user id is ", current_user.id)
            print(tasks_list)
            return render_template("index.html", ut=tasks_list[:],l=len(tasks_list),ct=c_tasks_list,l2=len(c_tasks_list))
        else:
            task=Tasks.query.filter_by(user_id=0).first()
            taskk=str(task.u_tasks)
            new=taskk + f',{request.form.get("task")}'
            task.u_tasks=new
            db.session.commit()
            task=str(Tasks.query.filter_by(user_id=0).first().u_tasks)
            current_tasks = Tasks.query.filter_by(user_id=0).first()
            tasks_list = current_tasks.u_tasks.split(',')
            c_tasks_list=current_tasks.c_tasks.split(",")
            return render_template('index.html',ut=tasks_list[:],l=len(tasks_list),ct=c_tasks_list,l2=len(c_tasks_list))
usernames=[]

@app.route('/<int:index>')
def check(index):
    if current_user.is_authenticated:
        tasks = Tasks.query.filter_by(user_id=current_user.id).first()
    else:
        tasks = Tasks.query.filter_by(user_id=0).first()
    tt = tasks.u_tasks.split(",")
    checked=tt[index]
    del tt[index]
    ttt=''
    for i in tt[1:]:
        ttt = ttt + f',{i}'
    print("previous", tasks.u_tasks)
    print(tasks.u_tasks == ttt)
    print('ttt',ttt)
    tasks.u_tasks = ttt
    db.session.commit()
    ch=tasks.c_tasks
    tasks.c_tasks=f"{ch},{checked}"
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/c/<int:index3>')
def uncheck(index3):
    if current_user.is_authenticated:
        tasks = Tasks.query.filter_by(user_id=current_user.id).first()
    else:
        tasks = Tasks.query.filter_by(user_id=0).first()
    tt = tasks.c_tasks.split(",")
    checked=tt[index3]
    del tt[index3]
    ttt=''
    for i in tt[1:]:
        ttt = ttt + f',{i}'
    print("previous", tasks.u_tasks)
    print('ttt',ttt)
    tasks.c_tasks = ttt
    db.session.commit()
    ch=tasks.u_tasks
    tasks.u_tasks=f"{ch},{checked}"
    db.session.commit()
    return redirect(url_for('main'))




@app.route('/delete/<int:index2>')
def delete(index2):
    print(index2)
    if current_user.is_authenticated:
        tasks=Tasks.query.filter_by(user_id=current_user.id).first()
    else:
        tasks = Tasks.query.filter_by(user_id=0).first()
    tt=tasks.u_tasks.split(",")
    del tt[index2]
    ttt=''
    for i in tt[1:]:
        ttt=ttt+f',{i}'
    print("previous",tasks.u_tasks)
    print(tasks.u_tasks==ttt)
    print('ttt',ttt)
    tasks.u_tasks=ttt
    db.session.commit()
    print(tasks.u_tasks.split(","))
    return redirect(url_for('main'))


@app.route('/delete/c/<int:index4>')
def delete_checked(index4):
    print(index4)
    if current_user.is_authenticated:
        tasks=Tasks.query.filter_by(user_id=current_user.id).first()
    else:
        tasks = Tasks.query.filter_by(user_id=0).first()
    tt=tasks.c_tasks.split(",")
    del tt[index4]
    ttt=''
    for i in tt[1:]:
        ttt=ttt+f',{i}'
    print("previous",tasks.c_tasks)
    print(tasks.c_tasks==ttt)
    print('ttt',ttt)
    tasks.c_tasks=ttt
    db.session.commit()
    print(tasks.c_tasks.split(","))
    return redirect(url_for('main'))




all_users=db.session.query(Users).all()
@app.route("/register",methods=['GET','POST'])
def register():
    global login2
    R=RegisterForm()
    if R.validate_on_submit():
        print("Validated")

        if len(R.password.data)>7:
            print("Length is ok")

            all_users2 = db.session.query(Users).all()
            try:
                for i in range(len(all_users2)-1):
                    # user = Users.query.filter_by(id=i)
                    usernames.append(all_users[i].username)
            except:
                pass
            try:
                for i in range(len(all_users2)-2):
                    # user = Users.query.filter_by(id=i)
                    usernames.append(all_users[i].username)
            except:
                pass
            if R.username.data in usernames:
                        print("Username Matched")
                        flash("Username already taken !")
                        return redirect(url_for('register'))
            else:
                        print("Submitted")
                        print(R.username.data)
                        print(R.password.data)
                        print(usernames)
                        print(len(all_users))
                        all_users2 = db.session.query(Users).all()
                        new_user = Users(id=len(all_users2) + 1, username=R.username.data, password=R.password.data)
                        db.session.add(new_user)
                        db.session.commit()
                            # new_user = Users(id=len(all_users) + 2, username=R.username.data, password=R.password.data)
                            # db.session.add(new_user)
                            # db.session.commit()
                        print("Not recorded")
                       # pass
                        # try:
                        #     new_user2 = Users(id=len(all_users) + 2, username=R.username.data, password=R.password.data)
                        #     db.session.add(new_user2)
                        #     db.session.commit()
                        # except:
                        #     pass
                        # usernames.append(R.username.data)
                        usernames.append(R.username.data)
                        us=Users.query.filter_by(id=len(all_users2)+1).first()
                        login_user(us,remember=True)
                        all_tasks=db.session.query(Tasks).all()
                        new_user=Tasks(id=len(all_tasks)+1,user_id=current_user.id,u_tasks='',c_tasks='')
                        db.session.add(new_user)
                        db.session.commit()
                        global current_id
                        current_id=current_user.id
                        print('current id: ',current_user.id)
                        print('us.id : ',us.id)
                        print()
                        login2=True
                        print(current_user.is_authenticated)
                        return redirect(url_for('main'))
        else:
            print("flash")
            flash('Password must contain atleast 8 characters!')
            return redirect(url_for("register"))

    else:
        print("not vaidated")
        return render_template('register.html', form=R, err=0)
    return render_template('register.html',form=R,err=0)


usernames=[]
passwords=[]
ids=[]
@app.route("/login",methods=['GET','POST'])
def login():
    global login2
    global usernames
    global passwords
    l=LoginForm()
    if request.method=="POST":
        print("Submitted")
        all_users2 = db.session.query(Users).all()
        for i in range(len(all_users2)):
            usernames.append(all_users2[i].username)
            passwords.append(all_users2[i].password)
            ids.append(all_users2[i].id)
        if l.username.data in usernames:
            print("correct username")
            ind=usernames.index(l.username.data)
            if l.password.data==passwords[ind]:
                print("Password Matched")
                user=Users.query.filter_by(id=ids[ind]).first()
                print("USER ID: ",ids[ind])
                login_user(user,remember=True)
                login2=True
                global current_user
                print(current_user.id)

                print(current_user.is_authenticated)
                return redirect(url_for('main'))
            else:
                flash("Wrong Password !")
                return render_template("login.html",form=l)
        else:
            flash("Username not Found")
            return render_template("login.html", form=l)
    return render_template("login.html",form=l)


@app.route("/logout")
def logout():
    global login2
    logout_user()
    login2=False
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)
