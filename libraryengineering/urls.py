
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView,LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view),

    path('adminclick', views.adminclick_view),
    path('studentclick', views.studentclick_view),
    path('addauthor', views.addauthor_view),
    path('viewauthor', views.viewauthor_view),
    path('viewauthorbystudent', views.viewauthorbystudent_view),

    path('adminsignup', views.adminsignup_view),
    path('studentsignup', views.studentsignup_view),
    path('adminlogin', LoginView.as_view(template_name='library/adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='library/studentlogin.html')),

    path('logout', LogoutView.as_view(template_name='library/index.html')),
    path('afterlogin', views.afterlogin_view),

    path('addbook', views.addbook_view),
    path('viewbook', views.viewbook_view),
    path('issuebook', views.issuebook_view),
    path('viewissuedbook', views.viewissuedbook_view),
    path('viewstudent', views.viewstudent_view),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent),
    path('viewbookbystudent', views.viewbookbystudent_view),
    path('aboutus', views.aboutus_view),
    path('aboutusstudent', views.aboutusstudent_view),
    path('aboutusadmin', views.aboutusadmin_view),
    path('contactus', views.contactus_view),
   path('contactusstudent', views.contactusstudent_view),
    path('contactusadmin', views.contactusadmin_view),
 

]
