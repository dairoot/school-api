
class UserType():
    STUDENT = 0
    TEACHER = 1
    DEPT = 2

    def __get__(self, instance, owner):
        return self.value


class ScheduleType():
    PERSON = 0
    CLASS = 1

    def __get__(self, instance, owner):
        return self.value
