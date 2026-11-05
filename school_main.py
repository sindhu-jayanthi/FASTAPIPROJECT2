from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.middleware.cors import CORSMiddleware
import Database_Schemas
from sqlalchemy.orm import Session, sessionmaker

import models
from Database import sessionlocal,engine
from models import  CourseCreate,CourseOut,CourseWithStudents,StudentCreate

app=FastAPI(title="School API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)
Database_Schemas.Base.metadata.create_all(bind=engine)
def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/courses",response_model=models.CourseOut)
def create_course(Data:CourseCreate,db=Depends(get_db)):

    db.add(Database_Schemas.Course(**Data.model_dump()))
    db.commit()
    db.refresh(Database_Schemas.Course)

@app.get("/courses", response_model=list[models.CourseOut])
def list_courses(db:Session = Depends(get_db)):
    return db.query(Database_Schemas.Course).all()


@app.get("/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Database_Schemas.Course).filter(Database_Schemas.Course.id == course_id).first()
    if course:
        return course
    else:
        print("Course Not Found")

@app.post("/courses")
def create_course(Data:models.CourseCreate,db:Session=Depends(get_db)):
    db.add(Database_Schemas.Course(**Data.model_dump()))
    db.commit()
    print("Course Created")

@app.post("/students")
def create_student(Data:StudentCreate,db:Session=Depends(get_db)):
    if not db.get(Database_Schemas.Course, Data.course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    else:
        student=Database_Schemas.Student(**Data.model_dump())
        db.add(student)
        try:
          db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Email already registered")
        db.refresh(student)
        return student

@app.get("/students")
def list_students(db:Session = Depends(get_db)):
    return db.query(Database_Schemas.Student).all()

@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student=db.query(Database_Schemas.Student).filter(Database_Schemas.Student.id == student_id).first()
    if student:
        return student

    else:
        print("student not found")

@app.put("/students/{student_id}")
def update_student(student_id:int, Data:models.StudentCreate, db:Session=Depends(get_db)):
    student=db.query(Database_Schemas.Student).get(student_id)
    if student:
        student.id=student_id
        student.name=Data.name
        student.email=Data.email
        student.age=Data.age
        student.course_id=Data.course_id

    try:
        db.commit()
        db.refresh(student)
        print("Student Updated")
        return student

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="record not found")

@app.patch("/students/{student_id}")
def patch_student(student_id:int, Data:models.StudentOut, db:Session=Depends(get_db)):
    student=db.query(Database_Schemas.Student).get(student_id)
    if student:
        updated_student=Data.model_dump(exclude_unset=True)
        for key, value in updated_student.items():
            setattr(student, key, value)
        db.commit()
    else:
        db.rollback()
        raise HTTPException(status_code=404, detail="student not found")




@app.delete("/students/{student_id}")
def delete_student(student_id: int, db:Session = Depends(get_db)):
    student=db.query(Database_Schemas.Student).get(student_id)
    if student:
        db.delete(student)
        db.commit()
        print("Student Deleted")

    else:
        raise HTTPException(status_code=404, detail="student not found")



