
import json
from abc import ABC ,abstractmethod
from pathlib import Path 

database = "school_data.json"
data = {"student":[],"teachers":[]}
try:
 if Path(database).exists():
     with open(database,'r')as f:
         content = f.read()
         if content:
             data= json.loads(content)
except Exception as err:
   print(f"error occured as {err}")

def save():
   with open(database,"w") as f:
      json.dump(data,f,indent=4)

class Persons(ABC):
   @abstractmethod
   def get_roles(self):
      pass
   @abstractmethod
   def register(self):
      pass
   @abstractmethod
   def show_details(self):
      pass
   @staticmethod
   def validate_email(email):
     if "@" in email and "." in email:
        return True
     else:
        return False

class Students(Persons):
   def get_roles(self):
      return "student"
   def register(self):
      name = input("tell your name:-")
      age = int(input("tell your age:-"))
      roll_n0=int(input("tell your roll no"))
      email= input("tell your email:-")

      if not Persons.validate_email(email):
         print("Invalid email")
         return
      for i in data['student']:
         if i ['roll_no'] == roll_n0:
            print("student already exist")
            return
      data['student'].append({
         "name": name,
         "age" :age,
         "roll_no": roll_n0,
         "email": email,
         "grades":{}
      })
      save()
      print(f"student {name} registered")

   def show_details(self):
       roll_no= int(input("roll no:-"))
       for s in data['student']:
          if s['roll_no'] ==roll_no:
             grades = s['grades']
             avg = sum(grades.values())/len(grades) if grades else 0

             print(f"\n Name :{s['name']}")
             print(f"\n Roll no :{s['roll_no']}")
             print(f"\n Grades:{grades}")
             print(f"\n Avarage:{avg:1f}")
             return
             

          


   def add_grade(self):
      roll_no = int(input("tell the roll no:-"))
      subject= input("subject:-")
      marks =float(input("Marks: "))
      for i in data['student']:
         if i['roll_no'] == roll_no:
           i['grades'][subject] =marks
           save()
           print("grade added successfully")
           return
      
      print("student not found")
      

class Teacher(Persons):
   def get_roles(self):
      return "Teacher"
   def register(self):
      name = input("tell your name:-")
      age = int(input("tell your age:-"))
      email =input("tell your email:-")
      subject= input("tell your subject:-")
      emp_id=int(input("tell your employee id:-"))
      if not Persons.validate_email(email):
               print("Invalid email")
               return
      for i in data['teachers']:
               if i ['employee_id'] == emp_id:
                  print("student already exist")
                  return
      data['teachers'].append({
               "name": name,
               "age" :age,
               "employee_id": emp_id,
               "subject": subject,
               "email": email,
               
        })
      save()
      print(f"Teacher {name} registered")
   def show_details(self):
      empyee_id= int(input("employee_id:-"))
      for t in data['teachers']:
        if t['employee_id'] ==empyee_id:
        
      
          print(f"\n Name :{t['name']}")
          print(f"\n employee_id :{t['employee_id']}")
          print(f"\n subject: {t['subject']}")
          return
        print("Teacher not found ")

        
        
          

        return


obj1= Students()
obj = Teacher()


print("press 1 to register a student")
print("press 2 to register a Teacher")
print("press 3 to add grades:-")
print("press 4 show a student detail")
print("press 5 to show teacher details")


choice = int(input("please tell your choice:-"))
if choice ==1:
   obj1.register()

elif choice==2:
   obj.register()
elif choice==3:
   obj1.add_grade()
elif choice ==4:
   obj1.show_details()
elif choice==5:
   obj.show_details()
   
