from pydantic import BaseModel, ConfigDict, EmailStr


class CourseCreate(BaseModel):
    title: str
    duration_months: int


class CourseOut(CourseCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    name: str
    email: str
    age: int
    course_id: int


class StudentOut(BaseModel):
    id: int
    name: str
    email: str
    age: int
    course: CourseOut          # nested: the full course is returned inside the student
    model_config = ConfigDict(from_attributes=True)


class CourseWithStudents(CourseOut):
    students: list[StudentCreate] = []