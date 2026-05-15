import os
from time import sleep
from unittest import case
from student import Student, Course

def clear_screen():
    try:
        if os.system("cls") != 0:
            raise Exception
    except:
        os.system("clear")

def message(message,delay=3):
    clear_screen()
    print(message)
    sleep(delay)
    clear_screen()

def get_valid_input(prompt, min_value=1, max_value=None):
    while True:
        user_input = input(prompt)
        if user_input.isnumeric():
            user_input = int(user_input)
            if user_input >= min_value and (max_value is None or user_input <= int(max_value)):
                return user_input
        print("Please enter a valid number.")

    
def menu():
    students = []
    courses = []

    while True:
        selection=0
        print("COURSE REGISTRATION SYSTEM\nMenu\n\
            1 Enroll student.\n\
            2 Create a course\n\
            3 Register student to a course\n\
            4 Drop a student from a course\n\
            5 View course information\n\
            0 Exit")
        selection = input("Make a selection: ")


        if selection == "":
            print("Please enter a number.")
        else:
            try:
                
                selection = int(selection)
            except ValueError:
                message("Invalid selection.")

        match selection:
            case 1:
                student_id = input("Enter student ID: ")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                paid = input("Has tuition been paid? yes/no: ")

                if paid.lower() != "yes":
                    tuition_paid = False
                else:
                    tuition_paid = True
            
                student = Student(student_id, first_name, last_name, tuition_paid)
                students.append(student)
                message("Student enrolled.")

            case 2:
                course_name = input("Enter course name: ")
                max_roster_size = get_valid_input("Enter maximum roster size: ",0)
                max_waitlist_size = get_valid_input("Enter maximum waitlist size: ",0)
                course = Course(course_name, max_roster_size, max_waitlist_size)
                courses.append(course)

                message("Course created.")

            case 3:
                if not courses:
                    message("You need to create a course first.")
                else:
                    for i in range(len(courses)):
                        print(f"{i + 1} {courses[i].course_name}")

                    course_number = get_valid_input("Enter course number: ", 1, len(courses))
                    selected_course = courses[course_number - 1]

                    student_id = input("Enter student ID to register: ")

                    student_found = None

                    for student in students:
                        if student.student_id == student_id:
                            student_found = student

                    if student_found is None:
                        message("Student not found.")
                    else:
                        result = selected_course.add_student(student_found)

                        if result is True:
                            message(f"{student_found.first_name} {student_found.last_name} ({student_found.student_id}) added successfully.")
                        else:
                            message(f"{student_found.first_name} {student_found.last_name} ({student_found.student_id}) not added.")
            case 4:
                if not courses:
                    message("You need to create a course first.")
                else:
                    for i in range(len(courses)):
                        print(f"{i + 1} {courses[i].course_name}")

                    course_number = get_valid_input("Enter course number: ", 1,len(courses))
                    selected_course = courses[course_number - 1]

                    student_id = input("Enter student ID to drop: ")

                    student_found = None

                    for student in selected_course.roster:
                        if student.student_id == student_id:
                            student_found = student

                    for student in selected_course.waitlist:
                        if student.student_id == student_id:
                            student_found = student

                    if student_found is None:
                        message("Student not found.")
                    else:
                        result = selected_course.drop_student(student_found)

                        if result is True:
                            message(f"{student_found.first_name} {student_found.last_name} ({student_found.student_id}) dropped successfully.")
                        else:
                            message(f"{student_found.first_name} {student_found.last_name} ({student_found.student_id}) not dropped.")
            case 5:

                if not courses:
                    message("You need to create a course first.")
                else:
                    courses_summary = ""
                    for course in courses:
                        courses_summary+=str(course)+"\n"
                message (courses_summary,5)

            case 0:
                message("Exiting program.")
                quit()

            case _:
                message("Invalid selection.")
        
        
if __name__ == "__main__":
    menu()






            
        