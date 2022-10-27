from flask import Flask, render_template, redirect,send_from_directory, request
from utils import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img/'
app.secret_key = "as2t4y532uyd"

@app.route("/")
def hello_world():
    user = getUserInfo()
    if user.fio == "1":
        return redirect('/login')
    return redirect('/disciplines')


@app.route("/login", methods=["POST"])
def postLogin():
    user = getUserInfo()
    if user.password == request.form.get('password'):
        return redirect('/disciplines')
    return redirect('/login')

@app.route("/login", methods=["GET"])
def getLogin():
    return render_template('login.html')


@app.route("/register/<int:step>", methods=["POST"])
def postRegister(step):
    if step == 0:
        setUserInfo1(request.form.get('fio'),request.form.get('password'))
        return render_template('register-end.html')
    else:
        setUserInfo2(request.form.get('spec'), request.form.get('group'))
        return redirect('/disciplines')

@app.route("/register", methods=["GET"])
def getRegister():
    return render_template('register-start.html')


@app.route("/disciplines", methods=["POST"])
def postAddDisciplines():
    addDiscipline(request.form.get('name'))
    return redirect('/disciplines')

@app.route("/disciplines", methods=["GET"])
def getDisciplines():
    user = getUserInfo()
    if user.fio == "1":
        return redirect('/login')
    disciplines = getDiscipline()
    return render_template('disciplines.html', disciplines=disciplines, user=user)

@app.route("/disciplinesDel/<int:id>", methods=["GET"])
def deleteDisciplines(id):
    delDiscipline(id)
    return redirect('/disciplines')


@app.route("/<int:id>/lecture", methods=["POST"])
def postLecture(id):
    addLecture(id,request.form.get('name'),request.form.get('content'),request.files['file'].filename)
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save(app.config['UPLOAD_FOLDER'] + filename)
    return redirect(f'/{id}/lecture')

@app.route("/<int:id>/lecture", methods=["GET"])
def getlecture(id):
    user = getUserInfo()
    if user.fio == "1":
        return redirect('/login')
    lectures = getLectureById(id)
    return render_template('lecture.html', id=id, lectures=lectures, user=user)

@app.route("/<int:disId>/lectureDel/<int:id>", methods=["GET"])
def deleteLecture(id, disId):
    delLecture(id)
    return redirect(f'/{disId}/lecture')

@app.route("/<int:disId>/lectureInner/<int:id>", methods=['GET'])
def getLectureInner(disId, id):
    user = getUserInfo()
    if user.fio == "1":
        return redirect('/login')
    lecture = getLecture(id)
    return render_template('lectureInner.html', disId=disId, id=id, lecture=lecture)


@app.route("/upload/<string:filename>", methods=['GET', 'POST'])
def upload(filename):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
                               path=filename)

@app.route("/addMaterial/<int:type>", methods=['GET'])
@app.route("/addMaterial/<int:type>/<int:disId>", methods=['GET'])
def gwtAddMaterial(type, disId = 0):
    back = '/disciplines'
    if (disId):
        back = f'/{disId}/lecture'
    return render_template('addContent.html', type=type, back=back, disId=disId)

@app.route("/addMaterial/<int:type>", methods=['POST'])
@app.route("/addMaterial/<int:type>/<int:disId>", methods=['POST'])
def postAddMaterial(type, disId = 0):
    if (disId):
        return redirect(f'/{disId}/lecture')
    return redirect('/disciplines')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)