"""
    This file contains the models for the student_transactions app.
"""
from django.db import models
from django.contrib.auth.models import User  
    
class Parent(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email_address = models.CharField(max_length=150, unique=True)
    mobile_number = models.CharField(max_length=150)
    employer = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return ("{}".format(self.email_address))


class School(models.Model):
    school_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    administrator = models.ForeignKey(User, related_name='school',
                                  on_delete=models.CASCADE)
    
    def __str__(self):
        return self.school_name

# Students Personal info class
class Student(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    grade_level = models.CharField(max_length=150)
    enrollment_number = models.CharField(max_length=150, unique=True)
    parent_id = models.ForeignKey(Parent, related_name='student',
                                  on_delete=models.CASCADE)
    school = models.ForeignKey(School,
                                  on_delete=models.CASCADE)
    tuition = models.FloatField()

    def __str__(self):
        return ("{}".format(self.enrollment_number))


    def get_enrollemnt_number(self):
        """ returns the username of the student"""
        return self.enrollment_number


class LoanRequest(models.Model):
    parent_id = models.ForeignKey(Parent,
                                   related_name='loanrequest',
                                   on_delete=models.CASCADE,
                                   )
    loan_amount = models.FloatField()
    students = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} {}".format(self.parent_id, self.loan_amount, self.created_at)


class LoanPayment(models.Model):
    parent_id = models.ForeignKey(Parent,
                                   related_name='loanpayment',
                                   on_delete=models.CASCADE,
                                   )
    payment_amount = models.FloatField()
    payment_method = models.CharField(max_length=55)
    transaction_id = models.CharField(max_length=20)
    payment_date = models.DateField()

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.parent_id,
                                          self.payment_amount,
                                          self.payment_method,
                                          self.transaction_id,
                                          self.payment_date,
                                          )
    

class Payment(models.Model):
    """Defines a Payments Table"""
    enrollment_number = models.ForeignKey(Student,
                                   related_name='payment',
                                   on_delete=models.CASCADE,
                                   )
    payment_amount = models.FloatField()
    payment_method = models.CharField(max_length=55)
    transaction_id = models.CharField(max_length=20)
    payment_date = models.DateField()

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.enrollment_number_id,
                                          self.payment_amount,
                                          self.payment_method,
                                          self.transaction_id,
                                          self.payment_date,
                                          )

    