from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db

# Association table for many-to-many relationship
student_course = db.Table('student_course',
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
    )

class Students(db.Model):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    courses = relationship('Course', secondary=student_course, lazy='subquery',
                           backref=db.backref('students', lazy=True))
    
class Course(db.Model):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_name = Column(String, nullable=False)

    # Cambiar nombre al archivo