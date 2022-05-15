from django.db import models
from django.contrib.auth.models import User

# School Programs
class Program(models.Model):
    program_name = models.CharField(max_length=120, unique=True)
    tuition = models.IntegerField()

    def __str__(self):
        return ("{}".format(self.program_name).upper())

    def count_objs(self):
        return self.objects.all().count()

# Students Personal info class
class Student(models.Model):
    username = models.OneToOneField(User,
                                    related_name="studentname",
                                    on_delete=models.CASCADE,
                                    primary_key=True)
    tuition = models.IntegerField()
    program = models.ForeignKey(Program, related_name="student", on_delete=models.CASCADE)

    def __str__(self):
        return ("{}".format(self.username).lower())

class Term(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "{} {}".format(self.name, self.end_date)

    def is_valid_term(self):
        return self.start_date < self.end_date

class Payment(models.Model):
    """Student payments Term 1"""
    student = models.OneToOneField(Student,
                                   related_name='payment',
                                   on_delete=models.CASCADE,
                                   primary_key=True)
    amount = models.IntegerField()
    pay_date = models.DateField()
    term = models.ForeignKey(Term, related_name="term", on_delete=models.CASCADE)

    def __str__(self):
        return "Username: {} Amount: {} Date: {} Term: {}".format(self.student,
                                                                 self.amount,
                                                                 self.pay_date,
                                                                 self.term)
