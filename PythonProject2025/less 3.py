"""
1. Application - Python
2. User - Teacher in the scool
3. Iterface - TUI (Terminal User Interface)


struct Student:
    name: str
    marks: list[int]

struct Teacher: no structure since authentication process
"""

storage: list[dict] = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "marks": [7, 8, 9, 10, 6, 7, 8],
        "info": "Alice Johnson is 18 y.o. Interests: math",
    },
    {
        "id": 2,
        "name": "Michael Smith",
        "marks": [6, 5, 7, 8, 7, 9, 10],
        "info": "Michael Smith is 19 y.o. Interests: science",
    },
    {
        "id": 3,
        "name": "Emily Davis",
        "marks": [9, 8, 8, 7, 6, 7, 7],
        "info": "Emily Davis is 17 y.o. Interests: literature",
    },
    {
        "id": 4,
        "name": "James Wilson",
        "marks": [5, 6, 7, 8, 9, 10, 11],
        "info": "James Wilson is 20 y.o. Interests: sports",
    },
    {
        "id": 5,
        "name": "Olivia Martinez",
        "marks": [10, 9, 8, 7, 6, 5, 4],
        "info": "Olivia Martinez is 18 y.o. Interests: art",
    },
    {
        "id": 6,
        "name": "Emily Davis",
        "marks": [4, 5, 6, 7, 8, 9, 10],
        "info": "Daniel Brown is 19 y.o. Interests: music",
    },
    {
        "id": 7,
        "name": "Sophia Taylor",
        "marks": [11, 10, 9, 8, 7, 6, 5],
        "info": "Sophia Taylor is 20 y.o. Interests: physics",
    },
    {
        "id": 8,
        "name": "William Anderson",
        "marks": [7, 7, 7, 7, 7, 7, 7],
        "info": "William Anderson is 18 y.o. Interests: chemistry",
    },
    {
        "id": 9,
        "name": "Isabella Thomas",
        "marks": [8, 8, 8, 8, 8, 8, 8],
        "info": "Isabella Thomas is 19 y.o. Interests: biology",
    },
    {
        "id": 10,
        "name": "Benjamin Jackson",
        "marks": [9, 9, 9, 9, 9, 9, 9],
        "info": "Benjamin Jackson is 20 y.o. Interests: history",
    },
]

def add_student(name: str, marks: list[int] | None = None, details: str | None = None) -> dict:
    new_id = max([s["id"] for s in storage], default=0) + 1
    student = {
        "id": new_id,
        "name": name,
        "marks": marks if marks else [],
        "info": details if details else "",
    }
    storage.append(student)
    return student


def show_student():
    print("\n=========================")
    for student in storage:
        print(f"{student['id']}. Student {student['name']}")
    print("=========================\n")


def search_students(student_id: int) -> None:
    for student in storage:
        if student["id"] == student_id:
            print(
                f"\n=========================\n"
                f"[{student['id']}] Student: {student['name']}\n"
                f"Marks: {student['marks']}\n"
                f"Info: {student['info']}\n"
                f"=========================\n"
            )
            return
    print(f"Student with ID {student_id} not found")


def ask_student_payload() -> dict:
    ask_prompt = (
        "\nEnter student's data using format: John Doe;1,2,3,4,5\n"
        "where 'John Doe' is full name and the numbers are marks.\n"
        "Use ';' as a separator: "
    )

    def parse(data) -> dict:
        try:
            name, raw_marks = data.split(";")
            marks = [int(item) for item in raw_marks.replace(" ", "").split(",")]
            info = input("Enter additional info (optional): ").strip()
            return {
                "name": name.strip(),
                "marks": marks,
                "info": info
            }
        except Exception as e:
            print(f"Error parsing input: {e}")
            return {}

    user_data = input(ask_prompt)
    return parse(user_data)


def add_mark_to_student():
    try:
        student_id = int(input("Enter student ID to add a mark: "))
        mark = int(input("Enter new mark (integer): "))
        for student in storage:
            if student["id"] == student_id:
                student["marks"].append(mark)
                print(f"Mark {mark} added to {student['name']}")
                return
        print("Student not found.")
    except ValueError:
        print("Invalid input. Please enter numeric ID and mark.")


def update_student():
    try:
        student_id = int(input("Enter student ID to update: "))
        for student in storage:
            if student["id"] == student_id:
                new_name = input("Enter new name (or press Enter to skip): ").strip()
                new_info = input("Enter new info (or press Enter to skip): ").strip()

                if new_name:
                    student["name"] = new_name

                if new_info:
                    current_info = student["info"]

                    if new_info in current_info:
                        student["info"] = new_info  # replace
                        print("Info updated (replaced).")
                    elif new_info and new_info != current_info:
                        student["info"] += " " + new_info  # augment
                        print("Info updated (augmented).")
                    else:
                        print("No changes made.")

                print("Student updated.")
                return
        print("Student not found.")
    except ValueError:
        print("Invalid student ID.")


def student_management_command_handle(command: str):
    if command == "show":
        show_student()
    elif command == "add":
        data = ask_student_payload()
        if data:
            student = add_student(data["name"], data["marks"], data.get("info"))
            print(f"Student: {student['name']} is added")
        else:
            print("The student's data is NOT correct. Please try again")
    elif command == "search":
        student_id = input("Enter student's ID: ")
        if student_id.isdigit():
            search_students(int(student_id))
        else:
            print("Please enter a valid numeric ID.")
    elif command == "add_mark":
        add_mark_to_student()
    elif command == "update":
        update_student()
    else:
        print("Unknown student command.")


def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search", "add_mark", "update")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)

    HELP_MESSAGE = (
        "\n📘 Welcome to the Journal App!\n"
        f"Available commands: {AVAILABLE_COMMANDS}\n"
        "• show - Show all students\n"
        "• add - Add a new student\n"
        "• search - Find a student by ID\n"
        "• add_mark - Add mark to student\n"
        "• update - Update student's name/info\n"
        "• help - Show this help message\n"
        "• quit - Exit the application"
    )

    print(HELP_MESSAGE)

    while True:
        command = input("\nSelect command: ").strip().lower()

        if command == "quit":
            print("👋 Thanks for using the Journal application!")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            student_management_command_handle(command)


def main():
    handle_user_input()


if __name__ == "__main__":
    main()
