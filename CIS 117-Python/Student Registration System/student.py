class Student:
    def __init__(self, student_id, first_name, last_name, tuition_paid):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.tuition_paid = tuition_paid
    
    def __eq__(self, student):
        check = (self.student_id, self.first_name.lower(), self.last_name.lower(), self.tuition_paid) == \
        (student.student_id, student.first_name.lower(), student.last_name.lower(), student.tuition_paid)
        return check
    
    def __str__(self):
        info = f"{self.first_name} {self.last_name} ({self.student_id})"
        return info


class Course:
    def __init__(self, course_name, max_roster_size, max_waitlist_size):
        self.course_name = course_name
        self.roster = []
        self.waitlist = []
        self.max_roster_size = max_roster_size
        self.max_waitlist_size = max_waitlist_size
    
    def __str__(self):

        course_summary = f"{self.course_name}\n{len(self.roster)} enrolled (maximum allowed {self.max_roster_size})\n"
        for student in self.roster:
            course_summary += f"\t{student}\n"

        course_summary += f"{len(self.waitlist)} on waitlist (maximum allowed {self.max_waitlist_size})\n"
        for student in self.waitlist:
            course_summary += f"\t{student}\n"

        return course_summary
    
    def add_student(self, student):
        if student in self.roster or student in self.waitlist or not student.tuition_paid or (len(self.roster) >= self.max_roster_size and len(self.waitlist) >= self.max_waitlist_size):
            return False

        if len(self.roster) < self.max_roster_size:
            self.roster.append(student)
        elif len(self.waitlist) < self.max_waitlist_size:
            self.waitlist.append(student)
  
        return True


    def drop_student(self, student):
        if student in self.roster:
            self.roster.remove(student)

            if len(self.waitlist) > 0:
                self.roster.append(self.waitlist.pop(0))
            return True

        if student in self.waitlist:
            self.waitlist.remove(student)
            return True

        return False


if __name__ == "__main__":

    course = Course("Media Studies", 5, 5)
    print(course)
    print("*****TESTING ADDS")
    students = [Student("S925", "Adam", "Ant", True), Student("S713", "Bob", "Barker", False), Student("S512", "Chevy", "Chase", True), Student("S513", "Doris", "Day", True), Student("S516", "Emilio", "Estevez", True), Student("S956", "Farrah", "Fawcet", True), Student("S419", "Greta", "Garbo", True), Student("S281", "Helen", "Hunt", True), Student("S790", "Jack", "Johnson", True), Student("S336", "Kim", "Kardashian", True), Student("S156", "Martina", "McBride", True), Student("S219", "Renne", "Russo", True), Student("S472", "Susan", "Serandon", True), Student("S892", "Vince", "Vaughn", True), Student("S901", "Walt", "Whitman", True)]
    for student in students:
        result = course.add_student(student)
        if result is True:
            print(f"{student} added successfully")
        else:
            print(f"{student} not added")
    print(course)
    chevy = students[2]
    result = course.add_student(chevy)
    if result is True:
        print(f"{chevy} added successfully")
    else:
        print(f"{chevy} not added")

    print(course)
    helen = students[7]
    result = course.add_student(helen)
    if result is True:
        print(f"{helen} added successfully")
    else:
        print(f"{helen} not added")

    print(course)
    print("*****TESTING DROPS")
    result = course.drop_student(chevy)

    if result is True:
        print(f"{chevy} dropped successfully")
    else:
        print(f"{chevy} not dropped")

    print(course)
    walt = students[14]
    result = course.drop_student(walt)

    if result is True:
        print(f"{walt} dropped successfully")
    else:
        print(f"{walt} not dropped")
    print(course)

    jack = students[8]
    result = course.drop_student(jack)

    if result is True:
        print(f"{jack} dropped successfully")
    else:
        print(f"{jack} not dropped")

    print(course)
    adam = students[0]
    result = course.drop_student(adam)

    if result is True:
        print(f"{adam} dropped successfully")
    else:
        print(f"{adam} not dropped")
    print(course)