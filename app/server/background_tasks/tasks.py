from datetime import datetime

# LOG NEW STUDENT
def log_student_creation(fullname: str):
    with open("D:/python/hello-flask/app/server/log/student_log.txt", "a") as log_file:
        log_file.write(f"Student created: {fullname}\n")


#LOG REQUEST
def log_request_time():
    with open("D:/python/hello-flask/app/server/log/request_log.txt", "a") as log_file:
        log_file.write(f"Request created: { datetime.now() } \n")
