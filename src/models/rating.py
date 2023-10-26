from src.models.course import Course

class Rating:
    def __init__(self, course: Course, major: str, prof: str, quality: int, difficulty: int) -> None:
        self.course = course
        self.major = major
        self.prof = prof
        self.quality = quality
        self.difficulty = difficulty