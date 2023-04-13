import random
import smtplib
from email.mime.text import MIMEText

import demjson
from flask import Flask, render_template, request, redirect, session, url_for,jsonify
import datetime
from Dbconnection import Db

app = Flask(__name__)

app.secret_key="alzh"
# systempath=r"..................\photos\\"

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/',methods=['get','post'])
def login():
    if request.method=="POST":
        n=request.form['textfield']
        p=request.form['textfield2']
        obj=Db()
        result=obj.selectOne("select * from login where username='"+n+"' and password='"+p+"'")
        if result:
            c=obj.selectOne("select count(login_id) as v from login where usertype='caretaker'")
            u=obj.selectOne("select count(login_id) as v from login where usertype='user'")
            session['c']=c['v']
            session['u']=u['v']
            session['lid']=result['login_id']
            session['lin']="1"
            k=datetime.datetime.now().strftime("%B %d %Y")
            session['mnth']=k
            typ=result['usertype']
            if typ=='admin':
                return redirect('/adminhome')
            elif typ=="caretaker":
                q=obj.selectOne("select * from  caretaker where staffid='"+str(result['login_id'])+"'")
                session['sname']=q['sname']
                session['simg']=q['sphoto']
                return redirect('/chome')
            else:
                return '''<script>alert("invalid user");window.location="/"</script>'''
        else:
            return  '''<script>alert("invalid user");window.location="/"</script>'''
    else:
        return render_template("index.html")

@app.route('/logout')
def logout():
    session['lin']="0"
    return redirect('/')

@app.route('/adminhome')
def adminhome():
    if session['lin']=="1":
        obj=Db()
        c = obj.selectOne("select count(noteid) as v from notes")
        u = obj.selectOne("select count(login_id) as v from login where usertype='user'")
        session['c'] = c['v']
        session['u'] = u['v']
        return render_template('ADMIN/index.html')
    return redirect('/')


@app.route('/change_pass',methods=['get','post'])
def change_pass():
    if session['lin']=="1":
        if request.method == "POST":
            old = request.form['textfield']
            new = request.form['textfield2']
            con = request.form['textfield3']
            db = Db()
            res = db.selectOne("select * from Login where Password='" + old + "' and usertype='admin'")
            if res is not None:
                if new == con:
                    db.update("update Login set Password='" + con + "' where usertype='admin'")
                    return '<script>alert("Changed Password");window.location="/"</script>'
                else:
                    return '<script>alert("Password miss match");window.location="/change_pass"</script>'
            else:
                return '<script>alert("Password incorrect");window.location="/change_pass"</script>'

        return render_template('ADMIN/change_password.html')
    return redirect('/')


@app.route('/users')
def users():
    if session['lin']=="1":
        obj=Db()
        a1 = obj.select("select * from user")
        return render_template('ADMIN/users.html',data=a1)
    return redirect('/')


@app.route('/note_add')
def note_add():
    if session['lin']=="1":
        session['head'] = "Add Tips"
        return render_template("admin/Tips-add.html")
    else:
        return redirect('/')

@app.route('/Tips_addpost',methods=['post'])
def Tips_addpost():
    if session['lin']=="1":
        tips=request.form['Tips']
        db=Db()
        q1 = db.selectOne("select * from `notes` where note='"+tips+"'")
        if q1 is None:
            q=db.insert("INSERT INTO `notes`(`note`,`date`)VALUES('"+tips+"',curdate())")
            c = db.selectOne("select count(noteid) as v from notes")
            session['c'] = c['v']
            return "<script>alert('Insert sucessfully');window.location='/Tips_view#service'</script>"
        else:
            return "<script>alert('Already Inserted ');window.location='/Tips_view#service'</script>"

    else:
        return redirect('/')

@app.route('/Tips_view')
def Tips_view():
    if session['lin']=="1":
        db = Db()
        session['head'] = "View Tips"
        q = db.select("select * from `notes`")
        return render_template("admin/Tips-view.html",data=q)
    else:
        return redirect('/')

@app.route('/deletetips/<i>')
def deletetips(i):
    if session['lin']=="1":
        db = Db()
        q = db.delete("delete from `notes`where noteid='"+i+"'")
        return "<script>alert('Deleted successfully ');window.location='/Tips_view#service'</script>"
    else:
        return redirect('/')


@app.route('/patient')
def patient():
    if session['lin']=="1":
        obj=Db()
        a1 = obj.select("select * from user,result where uid=User_id and result='yes'")
        return render_template('ADMIN/patient.html',data=a1)
    return redirect('/')
# ======================================================================================================================
if __name__ == '__main__':
    app.run(host="0.0.0.0")
