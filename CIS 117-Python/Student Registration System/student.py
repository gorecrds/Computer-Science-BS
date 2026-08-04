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