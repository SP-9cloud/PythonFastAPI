from fastapi import APIRouter, Body, Query, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from typing import Optional
from pydantic import EmailStr
from app.server.background_tasks.tasks import log_student_creation


from app.server.database.student import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student,
    build_search_query
)
from app.server.schemas.student import (
    StudentSchema,
)

from app.server.models.student import (
    ErrorResponseModel,
    ResponseModel,
    GetResponseModel,
    UpdateStudentModel,
)

router = APIRouter()

@router.post("/", response_description="Student data added into the database")
def add_student_data(student: StudentSchema = Body(...), background_tasks: BackgroundTasks = None
):
    student = jsonable_encoder(student)
    new_student = add_student(student)

    # IMPLEMENT BACKGROUND LOGGING
    background_tasks.add_task(log_student_creation, student["fullname"])

    return ResponseModel(new_student, "Student added successfully.")


@router.get("/", response_description="Students retrieved")
def get_students(
    skip: int = Query(0,ge = 0),
    limit: int = Query(0,le = 1000),
    search: Optional[str] = None,
    fullname: Optional[str] = None,
    email: Optional[str] = None,
    course: Optional[str] = None,
    year: Optional[str] = None,
    gpa: Optional[str] = None,
):
    query = {}
    if fullname:
        query['fullname']={"$regex" : fullname, "$options" : "i"}
    if email:
        query['email']={"$regex" : email, "$options" : "i"}
    if course:
        query['course_of_study']={"$regex" : course, "$options" : "i"}
    if year:
        query['year']=(year)
    if gpa:
        query['GPA']=(gpa)
    if search:
        query = build_search_query(search)
        

    students = retrieve_students(query,skip,limit)
    if students:
        return GetResponseModel(skip,limit,len(students),students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")


@router.get("/{id}", response_description="Student data retrieved")
def get_student_data(id):
    student = retrieve_student(id)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")

@router.put("/{id}")
def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = update_student(id, req)
    if updated_student:
        return ResponseModel(
            "Student with ID: {} name update is successful".format(id),
            "Student name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )

@router.delete("/{id}", response_description="Student data deleted from the database")
def delete_student_data(id: str):
    deleted_student = delete_student(id)
    if deleted_student:
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Student with id {0} doesn't exist".format(id)
    )

# IMPLEMENT BACKGROUND CHECKS
@router.post("/add-student-log")
async def add_student_log(background_tasks: BackgroundTasks, payload: dict = Body(...)):
    fullname = payload.get("fullname")
    if not fullname:
        return {"error": "Missing fullname"}

    background_tasks.add_task(log_student_creation, fullname)
    return {"message": f"Log task scheduled for {fullname}"}
