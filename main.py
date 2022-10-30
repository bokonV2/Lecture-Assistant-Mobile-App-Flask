from flask import Flask, render_template, redirect, send_from_directory, request, session
from utils import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img/'
app.secret_key = "sdfery54er4yehr5ye4gd4d"

@app.route("/")
def hello_world():
    if not session.get('id'):
        return redirect('/login')
    try:
        user = getUserInfoById(session['id'])
    except:
        session['id'] = False
    return redirect('/disciplines')


@app.route("/login", methods=["POST"])
def postLogin():
    user = checkLoginUser(request.form.get('login'), request.form.get('password'))
    print(type(user))
    if user:
        session['id'] = user
        return redirect('/disciplines')
    return redirect('/login')

@app.route("/login", methods=["GET"])
def getLogin():
    return render_template('login.html')


@app.route("/register/<int:step>", methods=["POST"])
def postRegister(step):
    if step == 0:
        session['fio'] = request.form.get('fio')
        session['login'] = request.form.get('login')
        session['password'] = request.form.get('password')
        # setUserInfo1(request.form.get('fio'),request.form.get('password'))
        return render_template('register-end.html')
    else:
        print(session['fio'], session['login'], session['password'])
        print(request.form.get('person') ,request.form.get('spec'), request.form.get('group'))
        # setUserInfo2(request.form.get('spec'), request.form.get('group'))
        session['id'] = registerUser(
            session['fio'], session['login'], session['password'],
            request.form.get('spec'), request.form.get('group'), 
            int(request.form.get('person'))
        )
        return redirect('/disciplines')

@app.route("/register", methods=["GET"])
def getRegister():
    return render_template('register-start.html')

@app.route("/unLogin", methods=["GET"])
def getUnLogin():
    session['id'] = 0
    return redirect('/login')

@app.route("/disciplines", methods=["POST"])
def postAddDisciplines():
    addDiscipline(request.form.get('name'))
    return redirect('/disciplines')

@app.route("/disciplines", methods=["GET"])
def getDisciplines():
    if not session.get('id'):
        return redirect('/login')
    user = getUserInfoById(session['id'])
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
    if not session.get('id'):
        return redirect('/login')
    user = getUserInfoById(session['id'])
    lectures = getLecturesByIdDiscipline(id)
    return render_template('lecture.html', id=id, lectures=lectures, user=user)

@app.route("/<int:disId>/lectureDel/<int:id>", methods=["GET"])
def deleteLecture(id, disId):
    delLecture(id)
    return redirect(f'/{disId}/lecture')

@app.route("/<int:disId>/lectureInner/<int:id>", methods=['GET'])
def getLectureInner(disId, id):
    if not session.get('id'):
        return redirect('/login')
    user = getUserInfoById(session['id'])
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