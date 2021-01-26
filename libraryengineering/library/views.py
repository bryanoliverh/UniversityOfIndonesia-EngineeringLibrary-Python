from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
from libraryengineering.settings import EMAIL_HOST_USER

from django.db.models import Count , Avg, Max, Lookup, Q

from .models import Book, Author

def index_view(request):
    
    #num_books = models.Book.objects.all().annotate(Count('')).order_by('')  
    
    num_books = models.Book.objects.all().count()   
    num_authors = models.Author.objects.count() 
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1
    return render(request,'library/index.html', context= {'num_books': num_books, 
                'num_authors': num_authors,
                 'num_visits': num_visits,},
    ) 


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})






def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')
        


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
  
    form=forms.BookForm()
    if request.method=='POST':
      
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addauthor_view(request):
   
    form=forms.AuthorForm()
    if request.method=='POST':
     
        form=forms.AuthorForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'library/authoradded.html')
    return render(request,'library/addauthor.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books=models.Book.objects.all()
    num_books = models.Book.objects.all().count()   
    num_authors = models.Author.objects.count()
    tot_lang = models.Language.objects.count()
    tot_langeng = models.Book.objects.filter(language_id__exact='2').all().count()
    tot_langjap = models.Book.objects.filter(language_id__exact='3').all().count()
    tot_langjav = models.Book.objects.filter(language_id__exact='4').all().count()
    tot_langind = models.Book.objects.filter(language_id__exact='5').all().count()
    tot_langarab = models.Book.objects.filter(language_id__exact='6').all().count()
    tot_langger = models.Book.objects.filter(language_id__exact='7').all().count()
    num_edubooks= models.Book.objects.filter(category__exact='education').all().count()
    num_entbooks= models.Book.objects.filter(category__exact='entertainment').all().count()
    num_biobooks= models.Book.objects.filter(category__exact='biography').all().count()


    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1
    return render(request,'library/viewbook.html',context= {'num_books': num_books, 
                'num_authors': num_authors,
                 'num_visits': num_visits,'books':books, 'tot_lang' : tot_lang,'tot_langjap' : tot_langjap,
                 'tot_langjav' : tot_langjav,'tot_langind' : tot_langind,'tot_langarab' : tot_langarab,
                 'tot_langger' : tot_langger,  'tot_langeng' : tot_langeng,'num_edubooks' : num_edubooks,
                 'num_entbooks' : num_entbooks,'num_biobooks' : num_biobooks,
                 
                 })


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewauthor_view(request):
    authors=models.Author.objects.all()
    num_authors = models.Author.objects.count() 
    num_authorsa = models.Author.objects.filter(first_name__icontains='a').all().count()
    num_authorsstarta = models.Author.objects.filter(first_name__istartswith='a').all().count()
    num_authorendwithn = models.Author.objects.filter(first_name__iendswith='n').all().count()
    num_authorsstartj = models.Author.objects.filter(last_name__istartswith='j').all().count()
    num_authorsendsg = models.Author.objects.filter(last_name__iendswith='g').all().count()
    num_authorsor = models.Author.objects.filter(Q(first_name__exact='Oliver') | Q(last_name__exact='Oliver')).all().count()
    num_authorsand = models.Author.objects.filter(Q(first_name__exact='Raditya') , Q(last_name__exact='Dika')).all().count()
    num_authorseng = models.Author.objects.filter(Q(first_name__contains='English') , Q(last_name__contains='English')).all().count()
    num_visits = request.session.get('num_visits', 1)

    request.session['num_visits'] = num_visits+1
    return render(request,'library/viewauthor.html',context= {
                'num_authors': num_authors,  'num_authorsa': num_authorsa,'num_authorsstarta': num_authorsstarta,

             'num_authorendwithn': num_authorendwithn,'num_authorsendsg': num_authorsendsg,'num_authorsstartj': num_authorsstartj,    
             
             'num_authorsor' :num_authorsor,
             'num_authorsand' :num_authorsand, 'num_authorseng' :num_authorseng,
             'num_visits': num_visits,'authors': authors })



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
      
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'library/bookissued.html')
    return render(request,'library/issuebook.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    books=models.IssuedBook.objects.all()
    num_books = models.IssuedBook.objects.all().count()   

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1
    return render(request,'library/viewissuedbook.html',context= {'li':li,'num_books': num_books, 
                 'num_visits': num_visits,'books':books})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    
    studentselect18 = models.StudentExtra.objects.filter(enrollment__exact='2018').all().count()
    studentselect17 = models.StudentExtra.objects.filter(enrollment__exact='2017').all().count()
    studentselect19 = models.StudentExtra.objects.filter(enrollment__exact='2019').all().count()
    studentselect20 = models.StudentExtra.objects.filter(enrollment__exact='2020').all().count()
    num_visits = request.session.get('num_visits', 1)
    studentselectoth = models.StudentExtra.objects.filter(enrollment__exact='2006').all().count()
    request.session['num_visits'] = num_visits+1
    students=models.StudentExtra.objects.all()
    return render(request,'library/viewstudent.html',{'studentselect17' : studentselect17,
    'studentselect18' : studentselect18, 
    'studentselect19' : studentselect19,'studentselect20' : studentselect20, 'num_visits': num_visits,'studentselectoth' : studentselectoth,
    'students':students})


@login_required(login_url='studentlogin')
def viewbookbystudent_view(request):
    books=models.Book.objects.all()
    num_books = models.Book.objects.all().count()   
    num_authors = models.Author.objects.count()  # The 'all()' is implied by default.

    tot_lang = models.Language.objects.count()
    tot_langeng = models.Book.objects.filter(language_id__exact='2').all().count()
    tot_langjap = models.Book.objects.filter(language_id__exact='3').all().count()
    tot_langjav = models.Book.objects.filter(language_id__exact='4').all().count()
    tot_langind = models.Book.objects.filter(language_id__exact='5').all().count()
    tot_langarab = models.Book.objects.filter(language_id__exact='6').all().count()
    tot_langger = models.Book.objects.filter(language_id__exact='7').all().count()
    num_edubooks= models.Book.objects.filter(category__exact='education').all().count()
    num_entbooks= models.Book.objects.filter(category__exact='entertainment').all().count()
    num_biobooks= models.Book.objects.filter(category__exact='biography').all().count()


    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1
    return render(request,'library/viewbookbystudent.html',context= {'num_books': num_books, 
                'num_authors': num_authors,
                 'num_visits': num_visits,'books':books, 'tot_lang' : tot_lang,'tot_langjap' : tot_langjap,
                 'tot_langjav' : tot_langjav,'tot_langind' : tot_langind,'tot_langarab' : tot_langarab,
                 'tot_langger' : tot_langger,  'tot_langeng' : tot_langeng,'num_edubooks' : num_edubooks,
                 'num_entbooks' : num_entbooks,'num_biobooks' : num_biobooks,
                 
                 })


@login_required(login_url='studentlogin')
def viewauthorbystudent_view(request):
    authors=models.Author.objects.all()
    num_authors = models.Author.objects.count()  # The 'all()' is implied by default.
    num_authorsa = models.Author.objects.filter(first_name__icontains='a').all().count()
    num_authorsstarta = models.Author.objects.filter(first_name__istartswith='a').all().count()
    num_authorendwithn = models.Author.objects.filter(first_name__iendswith='n').all().count()
    num_authorsstartj = models.Author.objects.filter(last_name__istartswith='j').all().count()
    num_authorsendsg = models.Author.objects.filter(last_name__iendswith='g').all().count()
    num_authorsor = models.Author.objects.filter(Q(first_name__exact='Oliver') | Q(last_name__exact='Oliver')).all().count()
    num_authorsand = models.Author.objects.filter(Q(first_name__exact='Raditya') , Q(last_name__exact='Dika')).all().count()
    num_authorseng = models.Author.objects.filter(Q(first_name__contains='English')  ,Q(last_name__contains='English')).all().count()
    num_visits = request.session.get('num_visits', 1)

    request.session['num_visits'] = num_visits+1
    return render(request,'library/viewauthorbystudent.html',context= {
                'num_authors': num_authors,  'num_authorsa': num_authorsa,'num_authorsstarta': num_authorsstarta,

             'num_authorendwithn': num_authorendwithn,'num_authorsendsg': num_authorsendsg,'num_authorsstartj': num_authorsstartj,    
             
             'num_authorsor' :num_authorsor, 'num_authorsand' :num_authorsand, 'num_authorseng' :num_authorseng,
             'num_visits': num_visits,'authors': authors })


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10000
        t=(issdate,expdate,fine)
        li2.append(t)

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1
    return render(request,'library/viewissuedbookbystudent.html',context= {'li1':li1,'li2':li2, 
                 'num_visits': num_visits})


def aboutus_view(request):
    return render(request,'library/aboutus.html')

@login_required(login_url='studentlogin')
def aboutusstudent_view(request):
    return render(request,'library/aboutusstudent.html')

@login_required(login_url='adminlogin')
def aboutusadmin_view(request):
    return render(request,'library/aboutusadmin.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['holiverbryan@gmail.com'], fail_silently = False)
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form':sub})

@login_required(login_url='studentlogin') 
def contactusstudent_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['holiverbryan@gmail.com'], fail_silently = False)
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactusstudent.html', {'form':sub})

    
@login_required(login_url='adminlogin') 
def contactusadmin_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['holiverbryan@gmail.com'], fail_silently = False)
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactusadmin.html', {'form':sub})