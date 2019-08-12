import wtforms
from flask_wtf import FlaskForm
from wtforms import validators

class TeachersForm(FlaskForm):
    name = wtforms.StringField(
        "姓名",
        render_kw={"class":"form-control"},
        validators=[
            validators.DataRequired("姓名不能为空")
        ]
    )
    gender = wtforms.SelectField(
        "性别",
        choices=[
            ("1", "男"),
            ("2", "女")
        ],
        render_kw={"class":"form-control"}
    )
    birthday = wtforms.DateField(
        "出生日期",
        render_kw={"class": "form-control"},
        validators=[
            validators.DataRequired("出生日期不能为空")
        ]
    )

class StudentsForm(FlaskForm):
    name = wtforms.StringField(
        "姓名",
        render_kw={"class":"form-control"},
        validators=[
            validators.DataRequired("姓名不能为空")
        ]
    )
    gender = wtforms.SelectField(
        "性别",
        choices=[
            ("1", "男"),
            ("2", "女")
        ],
        render_kw={"class":"form-control"}
    )
    birthday = wtforms.DateField(
        "出生日期",
        render_kw={"class": "form-control"},
        validators=[
            validators.DataRequired("出生日期不能为空")
        ]
    )