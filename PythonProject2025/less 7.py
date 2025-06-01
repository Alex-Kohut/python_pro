import enum


class Role(enum.StrEnum):
    STUDENT = enum.auto()
    TEACHER = enum.auto()


class User:
    def __init__(self, name: str, email: str, role: Role) -> None:
        self.name = name
        self.email = email
        self.role = role

    def send_notification(self, notification):
        print(f"\nTo: {self.name} <{self.email}>")
        print(notification)


class Notification:
    def __init__(self, subject: str, message: str, attachment: str = "") -> None:
        self.subject = subject
        self.message = message
        self.attachment = attachment

    def format(self) -> str:
        formatted = f"Subject: {self.subject}\nMessage: {self.message}"
        if self.attachment:
            formatted += f"\nAttachment: {self.attachment}"
        return formatted

    def __str__(self):
        return self.format()


class StudentNotification(Notification):
    def format(self) -> str:
        return super().format() + "\nSent via Student Portal"


class TeacherNotification(Notification):
    def format(self) -> str:
        return super().format() + "\nTeacher's Desk Notification"


def main():
    # Create users
    student_user = User(name="John Student", email="john@student.edu", role=Role.STUDENT)
    teacher_user = User(name="Anna Teacher", email="anna@school.edu", role=Role.TEACHER)

    # Create notifications
    student_note = StudentNotification(
        subject="Semester Grades",
        message="Your grades have been published.",
        attachment="grades.pdf"
    )

    teacher_note = TeacherNotification(
        subject="Staff Meeting Agenda",
        message="Reminder: staff meeting on Monday.",
        attachment="agenda.docx"
    )

    # Send notifications
    student_user.send_notification(student_note)
    teacher_user.send_notification(teacher_note)


if __name__ == "__main__":
    main()