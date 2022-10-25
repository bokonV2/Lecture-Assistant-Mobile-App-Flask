from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/login", methods=["POST"])
def postLogin():
    return redirect('/')

@app.route("/login", methods=["GET"])
def getLogin():
    return redirect('/')

@app.route("/register", methods=["POST"])
def postRegister():
    return redirect('/')

@app.route("/register", methods=["GET"])
def getRegister():
    return redirect('/')


@app.route("/disciplines", methods=["POST"])
def postAddDisciplines():
    return redirect('/')

@app.route("/disciplines", methods=["GET"])
def getDisciplines():
    return redirect('/')

@app.route("/<int:id>/disciplines", methods=["DELETE"])
def deleteDisciplines(id):
    return redirect('/')


@app.route("/<int:id>/lecture", methods=["POST"])
def postLecture(id):
    return redirect('/')

@app.route("/<int:id>/lecture", methods=["GET"])
def getlecture(id):
    return redirect('/')

@app.route("/<int:id>/lecture", methods=["DELETE"])
def deleteLecture(id):
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)