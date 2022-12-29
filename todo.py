
from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/Mihriban Ezgi Kaya/Desktop/TodoApp/todo.db"
db.init_app(app)
#aradaki köprüyü yani ORM yi kurdum

@app.route("/")
def index():
    todos = Todo.query.all() #todoları çektik
    return render_template("index.html", todos = todos)

@app.route("/complete/<string:id>") #dinamik url adresi oldu
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    """if todo.complete == True:
        todo.complete= False
    else:
        todo.complete=True"""
    todo.complete =not todo.complete  #true ise false false ise true olacak
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))





@app.route("/add", methods=["POST"]) #todo oluşturup ekle butonuna tıkladığımda post olur
def addTodo():
    title= request.form.get("title")
    newTodo= Todo(title = title,complete =False)
    #classımdan formumdan bir obje oluşturdum
    db.session.add(newTodo) #oluşturduğum objemi databaseime ekledim 
    db.session.commit()
    return redirect(url_for("index"))




class Todo(db.Model): #tablo oluşturdum
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean) #her todo tamamlanmamış bir iş ve her seferinde false ile başlıyor tamamlandıysa true oluyor 0 false 1 true boolean


if __name__=="__main__": #flaskda serverımı ayağa kaldırdım 

 with app.app_context(): 
    db.create_all()  
    app.run(debug=True)

