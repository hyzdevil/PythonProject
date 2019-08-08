from FlaskDirtory.main import models

db = models.session

class BaseModel(models.Model):
    __abstract__ = True
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db.add(self)
        db.commit()

    def delete_obj(self):
        db.delete(self)
        db.commit()

class User(BaseModel):
    __tablename__ = "user"
    username = models.Column(models.String(32))
    password = models.Column(models.Integer)
    identify = models.Column(models.Integer)
    identify_id = models.Column(models.Integer,default=0)

class Students(BaseModel):
    """学员表"""
    __tablename__ = "students"
    name = models.Column(models.String(32))
    gender = models.Column(models.Integer)

    to_attendance = models.relationship(
        "Attendance",
        backref="to_students"
    )

class Sorce(BaseModel):
    """成绩表"""
    __tablename__ = "sorce"
    course = models.Column(models.Float,default=0)

    stu_id = models.Column(models.Integer,models.ForeignKey('students.id'))
    course_id = models.Column(models.Integer,models.ForeignKey('course.id'))

Stu_Cou = models.Table(
    "stu_cou",
    models.Column("id", models.Integer, primary_key=True, autoincrement=True),
    models.Column("student_id", models.Integer, models.ForeignKey('students.id')),
    models.Column("course_id", models.Integer, models.ForeignKey('course.id'))
)

class Course(BaseModel):
    """课程表"""
    __tablename__ = "course"
    name = models.Column(models.String(32))

    to_teacher = models.relationship(
        "Teachers",
        backref = "to_course"
    )
    to_student = models.relationship(
        "Students",
        secondary = Stu_Cou,
        backref = models.backref("to_course", lazy = "dynamic"),
        lazy = "dynamic",
    )

class Attendance(BaseModel):
    """考勤表"""
    __tablename__ = "attendance"
    att_time = models.Column(models.Date)
    status = models.Column(models.Integer, default=1)

    stu_id = models.Column(models.Integer, models.ForeignKey('students.id'))

class Teachers(BaseModel):
    """教师表"""
    __tablename__ = "teachers"
    name = models.Column(models.String(32))
    gender = models.Column(models.Integer)

    course_id = models.Column(models.Integer,models.ForeignKey('course.id'))

# models.drop_all()
# models.create_all()