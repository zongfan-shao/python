import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

from wtforms import validators

import flask_admin as admin
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin.contrib.sqla.form import InlineModelConverter
from flask_admin.contrib.sqla.fields import InlineModelFormList
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual


# Create application
app = Flask(__name__)

# set optional bootswatch theme
# see http://bootswatch.com/3/ for available swatches
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# Create models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    学生学号 = db.Column(db.String(100))
    学生姓名 = db.Column(db.String(100))
    学生院校 = db.Column(db.String(120))

    def __str__(self):
        return "{}, {}".format(self.学生姓名, self.学生学号)

    def __repr__(self):
        return "{}: {}".format(self.id, self.__str__())

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    教职工号 = db.Column(db.String(100))
    教师姓名 = db.Column(db.String(100))
    教师院校 = db.Column(db.String(120))

    def __str__(self):
        return "{}, {}".format(self.教师姓名, self.教职工号)

    def __repr__(self):
        return "{}: {}".format(self.id, self.__str__())

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    课程号 = db.Column(db.String(100))
    教师信息 = db.Column(db.String(100))
    课程安排 = db.Column(db.String(120))
    是否必修 = db.Column(db.String(120))

    def __str__(self):
        return "{}, {}".format(self.教师信息, self.课程号)

    def __repr__(self):
        return "{}: {}".format(self.id, self.__str__())

class Score_total(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stno  = db.Column(db.String(100))
    required_score  = db.Column(db.String(100))
    option_score   = db.Column(db.String(120))
    total_socre   = db.Column(db.String(120))

    def __str__(self):
        return "{}, {}".format(self.required_score , self.stno )

    def __repr__(self):
        return "{}: {}".format(self.id, self.__str__())
		
class Luntan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ltno  = db.Column(db.String(100))
    teacher  = db.Column(db.String(100))
    course   = db.Column(db.String(100))
    affterClass   = db.Column(db.String(100))

    def __str__(self):
        return "{}, {}".format(self.teacher , self.ltno )

    def __repr__(self):
        return "{}: {}".format(self.id, self.__str__())

class Xuanke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    编号   = db.Column(db.String(100))
    预选  = db.Column(db.String(100))
    正选   = db.Column(db.String(100))
    课程表   = db.Column(db.String(100))
    学期   = db.Column(db.String(100))
    往期汇总   = db.Column(db.String(100))
    本期汇总   = db.Column(db.String(100))

    def __str__(self):
        return "{}, {}".format(self.预选 , self.编号 )

    def __repr__(self):
        return "{}: {}".format(self.id, self.__str__())


class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    parent_id = db.Column(db.Integer, db.ForeignKey('tree.id'))
   

    def __str__(self):
        return "{}".format(self.name)


class Screen(db.Model):
    __tablename__ = 'screen'
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    @hybrid_property
    def number_of_pixels(self):
        return self.width * self.height


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">欢迎进入学生老师信息系统!</a>'


# Customized User model admin
inline_form_options = {
    'form_columns': ['id', 'key', 'value'],
    'form_args': None,
    'form_extra_fields': None,
}

class StudentAdmin(sqla.ModelView):
    action_disallowed_list = ['delete', ]
    column_display_pk = True
    column_list = [
        'id',
        '学生姓名',
        '学生学号',
        '学生院校',
    ]
    column_default_sort = [('学生姓名', False), ('学生学号', False)]  # sort on multiple columns

class TeacherAdmin(sqla.ModelView):
    action_disallowed_list = ['delete', ]
    column_display_pk = True
    column_list = [
        'id',
        '教师姓名',
        '教职工号',
        '教师院校',
    ]
    column_default_sort = [('教师姓名', False), ('教职工号', False)]  # sort on multiple columns

class CourseAdmin(sqla.ModelView):
   action_disallowed_list = ['delete', ]
   column_display_pk = True
   column_list = [
        'id',
        '课程号',
        '教师信息',
        '课程安排',
	'是否必修',
   ]
column_default_sort = [('课程号', False), ('教师信息', False)]  # sort on multiple columns


class Score_totalAdmin(sqla.ModelView):
   action_disallowed_list = ['delete', ]
   column_display_pk = True
   column_list = [
        'id',
        'stno',
        'required_score',
        'option_score',
	'total_socre',
   ]
column_default_sort = [('stno', False), ('required_score', False)]  # sort on multiple columns

class LuntanAdmin(sqla.ModelView):
   action_disallowed_list = ['delete', ]
   column_display_pk = True
   column_list = [
        'id',
        'ltno',
        'teacher',
        'course',
	'affterClass',
   ]
column_default_sort = [('ltno', False), ('teacher', False)]  # sort on multiple columns

class XuankeAdmin(sqla.ModelView):
   action_disallowed_list = ['delete', ]
   column_display_pk = True
   column_list = [
        'id',
        '编号',
        '预选',
        '正选',
	'课程表',
        '学期',
        '往期汇总',
        '本期汇总',
   ]
column_default_sort = [('编号', False), ('预选', False)]  # sort on multiple columns


class TreeView(sqla.ModelView):
    form_excluded_columns = ['children', ]


class ScreenView(sqla.ModelView):
    column_list = ['id', 'width', 'height', 'number_of_pixels']  # not that 'number_of_pixels' is a hybrid property, not a field
    column_sortable_list = ['id', 'width', 'height', 'number_of_pixels']

    # Flask-admin can automatically detect the relevant filters for hybrid properties.
    column_filters = ('number_of_pixels', )

   


# Create admin
admin = admin.Admin(app, name='学生老师信息系统', template_mode='bootstrap3')

# Add views
admin.add_view(StudentAdmin(Student, db.session))
admin.add_view(TeacherAdmin(Teacher, db.session))
admin.add_view(CourseAdmin(Course, db.session))
admin.add_view(Score_totalAdmin(Score_total, db.session))
admin.add_view(LuntanAdmin(Luntan, db.session))
admin.add_view(XuankeAdmin(Xuanke, db.session))

def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import random
    import datetime

    db.drop_all()
    db.create_all()

    # Create sample Users
    学生学号s = [
        'S01', 'S02', 'S03'
    ]
    学生姓名s = [
        '张三', '李四', '王宁'
    ]

    学生院校s = [
        '计算机学院', '数学学院', '外语学院'
    ]

    user_list = []
    for i in range(len(学生学号s)):
        user = Student()
        user.学生学号 = 学生学号s[i]
        user.学生姓名 = 学生姓名s[i]
        user.学生院校 = 学生院校s[i]
        user_list.append(user)
        db.session.add(user)

# Create sample teachers
 
    教职工号s = [
        'T01', 'T02', 'T03'
    ]
    教师姓名s = [
        '秦卓珈', '韩一芳', '刘志宝'
    ]

    教师院校s = [
        '计算机学院', '数学学院', '外语学院'
    ]

    teacher_list = []
    for i in range(len(教职工号s)):
        teacher = Teacher()
        teacher.教职工号 = 教职工号s[i]
        teacher.教师姓名 = 教师姓名s[i]
        teacher.教师院校 = 教师院校s[i]
        teacher_list.append(teacher)
        db.session.add(teacher)

# Create sample course
 
    课程号s = [
        'C01', 'C02', 'C03'
    ]
    教师信息s = [
        'T01', 'T02', 'T03'
    ]

    课程安排s = [
        '语文课201903', '语文课201903', '语文课201903'
    ]
	
    是否必修s = [
        '1', '0', '1'
    ]

    course_list = []
    for i in range(len(课程号s)):
        course = Course()
        course.课程号 = 课程号s[i]
        course.教师信息 = 教师信息s[i]
        course.课程安排 = 课程安排s[i]
        course.是否必修 = 是否必修s[i]
        course_list.append(course)
        db.session.add(course)
# Create sample score_total
 
    stnos = [
        'ST01', 'ST02', 'ST03'
    ]
    required_scores = [
        '50.5', '90', '20'
    ]

    option_scores = [
        '40', '90', '20'
    ]
	
    total_socres = [
        '50.5', '90', '20'
    ]

    score_total_list = []
    for i in range(len(stnos)):
        score_total = Score_total()
        score_total.stno = stnos[i]
        score_total.required_score = required_scores[i]
        score_total.option_score = option_scores[i]
        score_total.total_socre  =total_socres[i]
        course_list.append(score_total)
        db.session.add(score_total)
# Create sample luntan
 
    ltnos= [
        'lt01', 'lt02', 'lt03'
    ]
    teachers= [
        '教师讨论作业一', '教师讨论作业二', '教师讨论作业三'
    ]

    courses= [
        '语文课讨论', '数孔课讨论', '法语课讨论'
    ]
	
    affterClasss= [
        '课后活动讨论一', '课后活动讨论二', '课后活动讨论三'
    ]

    luntan_list = []
    for i in range(len(ltnos)):
        luntan = Luntan()
        luntan.ltno = ltnos[i]
        luntan.teacher = teachers[i]
        luntan.course = courses[i]
        luntan.affterClass = affterClasss[i]
        luntan_list.append(luntan)
        db.session.add(luntan)
		
		
# Create sample xuanke
 
    编号s= [
        'X01', 'X02', 'X03'
    ]
    预选s= [
        'C01', 'C02', 'C03'
    ]

    正选s= [
        'C01', 'C02', 'C03'
    ]
	
    课程表s= [
        '星期三', '星期三', '星期三'
    ]
	
    学期s= [
        '201903', '201909', '201903'
    ]
	
    往期汇总s= [
        'null', 'null', 'null'
    ]
	
    本期汇总s= [
         'null', 'null', 'null'
    ]

    xuanke_list = []
    for i in range(len(编号s)):
        xuanke = Xuanke()
        xuanke.编号 = 编号s[i]
        xuanke.预选 = 预选s[i]
        xuanke.正选 = 正选s[i]
        xuanke.课程表 = 课程表s[i]
        xuanke.学期 = 学期s[i]
        xuanke.往期汇总 = 往期汇总s[i]
        xuanke.本期汇总 = 本期汇总s[i]
        luntan_list.append(xuanke)
        db.session.add(xuanke)
    # Create a sample Tree structure
    trunk = Tree(name="Trunk")
    db.session.add(trunk)
    for i in range(5):
        branch = Tree()
        branch.name = "Branch " + str(i+1)
        branch.parent = trunk
        db.session.add(branch)
        for j in range(5):
            leaf = Tree()
            leaf.name = "Leaf " + str(j+1)
            leaf.parent = branch
            db.session.add(leaf)


    db.session.add(Screen(width=500, height=2000))
    db.session.add(Screen(width=550, height=1900))

    db.session.commit()
    return

if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)
