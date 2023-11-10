from django.contrib import admin
from api.models import (
    Student, Payment, School, Parent
)
from api.admin import (
    StudentAdmin, PaymentAdmin,
    SchoolAdmin, ParentAdmin
)

from django.contrib import admin


class SchoolAdminView(admin.AdminSite):
    site_header = "Lipila School Administration"


# #register school site models
school_site = SchoolAdminView(name="SchoolAdmin")

school_site.register(Student, StudentAdmin)
school_site.register(Payment, PaymentAdmin)
school_site.register(School, SchoolAdmin)
school_site.register(Parent, ParentAdmin)
