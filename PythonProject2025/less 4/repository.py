import csv
from typing import Optional


class Repository:
    def __init__(self, filepath: str = "students.csv"):
        self.filepath = filepath
        self.students: dict[int, dict] = {}
        self._load()

    def _load(self):
        try:
            with open(self.filepath, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    student_id = int(row["id"])
                    marks = [int(m) for m in row["marks"].split(',') if m.strip().isdigit()]
                    self.students[student_id] = {
                        "id": student_id,
                        "name": row["name"],
                        "marks": marks,
                        "info": row["info"]
                    }
        except FileNotFoundError:
            self._save()

    def _save(self):
        with open(self.filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name", "marks", "info"])
            writer.writeheader()
            for student in self.students.values():
                writer.writerow({
                    "id": student["id"],
                    "name": student["name"],
                    "marks": ",".join(map(str, student["marks"])),
                    "info": student["info"]
                })

    def list_students(self) -> list[dict]:
        return list(self.students.values())

    def add_student(self, name: str, marks: list[int] = None, info: str = "") -> dict:
        new_id = max(self.students.keys(), default=0) + 1
        student = {
            "id": new_id,
            "name": name.strip(),
            "marks": marks or [],
            "info": info.strip()
        }
        self.students[new_id] = student
        self._save()
        return student

    def get_student(self, id_: int) -> Optional[dict]:
        return self.students.get(id_)

    def update_student(self, id_: int, name: Optional[str] = None, info: Optional[str] = None) -> bool:
        student = self.students.get(id_)
        if not student:
            return False
        if name:
            student["name"] = name.strip()
        if info:
            current_info = student["info"]
            if info not in current_info:
                student["info"] += " " + info.strip()
        self._save()
        return True

    def delete_student(self, id_: int) -> bool:
        if id_ in self.students:
            del self.students[id_]
            self._save()
            return True
        return False

    def add_mark(self, id_: int, mark: int) -> bool:
        student = self.students.get(id_)
        if not student:
            return False
        student["marks"].append(mark)
        self._save()
        return True