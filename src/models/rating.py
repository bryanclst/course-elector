from src.models.course import Course

class Rating:
    def __init__(self, course: Course, prof: str, quality: int, difficulty: int, grade: str, desc: str) -> None:
        self.course = course
        self.prof = prof
        self.quality = quality
        self.difficulty = difficulty
        self.grade = grade
        self.desc = desc