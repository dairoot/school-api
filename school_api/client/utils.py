
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


class NullClass():

    def __init__(self, tip=''):
        self.tip = tip

    def __str__(self):
        return self.tip

    def __getattr__(self, name):
        def func():
            return self
        return func
