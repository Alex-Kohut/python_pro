from repository import Repository

repo = Repository()


def handle_user_input():
    print("\n📘 Welcome to the Journal App!")
    print("Commands: show, add, search, add_mark, update, delete, help, quit")

    while True:
        command = input("\nCommand: ").strip().lower()

        if command == "quit":
            print("👋 Goodbye!")
            break

        elif command == "help":
            print("Available commands: show, add, search, add_mark, update, delete, quit")

        elif command == "show":
            for s in repo.list_students():
                print(f"[{s['id']}] {s['name']} | Marks: {s['marks']} | Info: {s['info']}")

        elif command == "add":
            line = input("Enter student like: John Doe;1,2,3,4: ")
            try:
                name_part, marks_part = line.split(";")
                name = name_part.strip()
                marks = [int(m) for m in marks_part.split(",") if m.strip().isdigit()]
                info = input("Info (optional): ")
                student = repo.add_student(name, marks, info)
                print(f"✅ Student added: {student}")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif command == "search":
            try:
                id_ = int(input("Enter student ID: "))
                student = repo.get_student(id_)
                if student:
                    print(f"[{student['id']}] {student['name']} | Marks: {student['marks']} | Info: {student['info']}")
                else:
                    print("Student not found.")
            except ValueError:
                print("Invalid ID.")

        elif command == "add_mark":
            try:
                id_ = int(input("Student ID: "))
                mark = int(input("Mark: "))
                if repo.add_mark(id_, mark):
                    print("✅ Mark added.")
                else:
                    print("❌ Student not found.")
            except ValueError:
                print("Invalid input.")

        elif command == "update":
            try:
                id_ = int(input("Student ID: "))
                name = input("New name (optional): ")
                info = input("New info (optional): ")
                if repo.update_student(id_, name=name or None, info=info or None):
                    print("✅ Student updated.")
                else:
                    print("❌ Student not found.")
            except ValueError:
                print("Invalid input.")

        elif command == "delete":
            try:
                id_ = int(input("Enter student ID to delete: "))
                if repo.delete_student(id_):
                    print("✅ Student deleted.")
                else:
                    print("❌ Not found.")
            except ValueError:
                print("Invalid ID.")

        else:
            print("Unknown command.")


def main():
    handle_user_input()


if __name__ == "__main__":
    main()