from faker import Faker
fake = Faker()
import random
from .models import *

def create_subject_marks(n):
    try:
        student_objs=Student.objects.all()
        for student in student_objs:
            subjects=Subject.objects.all()
            
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject=subject,
                    student=student,
                    marks=random.randint(0,100)
                )
    except Exception as e:
        print(e)    
        
def seed_db(n=100) -> None:
    try:
      for _ in range(0,n):
            department_objs=Department.objects.all()
            random_department = random.choice(department_objs)
            department_code = random_department.department[:3]  # Assuming department name holds a code
            student_id = f'2021B{department_code}{random.randint(100, 999)}'
            
            student_name=fake.name()
            student_email=fake.email()
            student_age=random.randint(20,30)
            student_address=fake.address()
        
            student_id_obj=StudentID.objects.create(student_id=student_id)
        
            student_obj=Student.objects.create(
                department=random_department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
        )
        
    except Exception as e:
          print(e)        