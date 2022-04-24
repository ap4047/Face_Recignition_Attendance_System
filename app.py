from flask import Flask,render_template,request,redirect,url_for
import attendance
import pandas as pd
app=Flask(__name__)
from user import routes

@app.route("/")
def hello(): return render_template("home.html")
@app.route("/dashboard",methods=["GET"])
def dashboard():
    return render_template("dashboard.html")
@app.route("/login",methods=["GET"])
def login():
    return render_template("login.html")
@app.route("/attendance",methods=["GET"])
def attendance_taker():
    return render_template("attendance.html")
@app.route("/attendance",methods=["POST"])
def submit():
    if request.method=="POST":
       attendance.attend()
       name=request.form["name"]
       df=pd.read_csv("Attendance.csv")
       report_df=pd.read_csv(df[df[name]]==name)
       result = report_df.to_html()
       print(result)
       return render_template("data.html",data=df.to_html())
     
       #print(marks_pred)
    return render_template("")

@app.route("/dashboard",methods=['GET'])
def dashboard():
    return render_template("dashboard.html ")
@app.route("/back")
def back():
    return redirect(url_for('hello'))
if __name__=="__main__":
       app.run(debug=True)
