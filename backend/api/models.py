"""
    This file contains the models for the student_transactions app.
"""
from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    school_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    administrator = models.ForeignKey(User, related_name='school',
                                      on_delete=models.CASCADE)

    def __str__(self):
        return self.school_name


class Parent(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email_address = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=150)
    employer = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    school = models.ForeignKey(School,
                               on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(
            self.first_name, self.last_name
        )
    
    def get_school_name(self):
        return self.school.school_name

    def get_contacts(self):
        return f"{self.email_address} {self.mobile_number}"
    

# Students Personal info class
class Student(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    grade_level = models.CharField(max_length=150)
    enrollment_number = models.CharField(max_length=150, unique=True)
    parent_id = models.ForeignKey(Parent, related_name='student',
                                  on_delete=models.CASCADE)
    tuition = models.FloatField()
   
    def __str__(self):
        return ("{} {} {} {} {}".format(
            self.enrollment_number, self.first_name, self.last_name, self.tuition, self.parent_id.school))
    
    def get_parent_email(self):
        return self.parent_id.email_address

    def get_parent_phone(self):
        return self.parent_id.mobile_number
        
    def get_school_name(self):
        return self.parent_id.school.school_name

    def get_tuition(self):
        return self.tuition
    
    def get_student_names(self):
        return f"{self.first_name} {self.last_name}"

    def get_enrollemnt_number(self):
        """ returns the username of the student"""
        return self.enrollment_number

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
    description = models.CharField(max_length=255)
    school = models.ForeignKey(School,
                               on_delete=models.CASCADE)

    def get_enrollemnt_number(self):
        """ returns the username of the student"""
        return self.enrollment_number.enrollment_number

    def __str__(self):
        return "{} {} {} {} {} {} {}".format(self.enrollment_number_id,
                                          self.payment_amount,
                                          self.payment_method,
                                          self.transaction_id,
                                          self.payment_date,
                                          self.school,
                                          self.description,
                                          )
    

class LipilaPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # currency = models.CharField(max_length=3)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    payer_account = models.CharField(max_length=10, null=False)
    payer_name = models.CharField(max_length=100, null=True)
    payer_email = models.EmailField(null=True)
    receiver_account = models.CharField(max_length=10, null=False)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ))

    def get_reference_id(self):
        return self.reference_id
    