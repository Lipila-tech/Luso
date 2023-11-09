from django.contrib import admin


from django.contrib import admin


class SchoolAdminView(admin.AdminSite):
    site_header = "Lipila School Administration"
    

# #register school site models
school_site = SchoolAdminView(name="SchoolAdmin")
