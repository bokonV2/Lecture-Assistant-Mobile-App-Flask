from object import *



def checkLoginUser(email, password):
    try:
        user = User.select().where(User.email == email and User.password == password).get()
    except:
        user = False
    if user:
        print(user)
        return user.id
    return False

def registerUser(fio, login, password, spec, group, is_teacher):
    return User.create(
        fio=fio, email=login, 
        password=password, spec=spec, 
        group=group, is_teacher=is_teacher
    ).id

def getUserInfoById(id):
    user =  User.select().where(User.id == id).get()
    return user

def setUserInfo1(fio, password):
    user = User.select().where(User.id == 1).get()
    user.fio = fio
    user.password = password
    user.save()

def setUserInfo2(spec, group):
    user = User.select().where(User.id == 1).get()
    user.spec = spec
    user.group = group
    user.save()

def getUserInfo():
    user = User.select().where(User.id == 1).get()
    return user

def addDiscipline(name):
    Disciplines.create(name=name)

def addLecture(dis_id, name, content, file):
    Lectures.create(dis_id=dis_id, content=content, file=file, name=name)

def getDiscipline():
    return Disciplines.select()

def getLecturesByIdDiscipline(id):
    return Lectures.select().where(Lectures.dis_id == id)

def getLecture(id):
    return Lectures.select().where(Lectures.id == id).get()


def delDiscipline(id):
    dis = Disciplines.select().where(Disciplines.id == id).get()
    dis.delete_instance()

def delLecture(id):
    dis = Lectures.select().where(Lectures.id == id).get()
    dis.delete_instance()