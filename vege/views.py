from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q,Sum

from django.contrib.auth import get_user_model

User=get_user_model()

#create your views
#function for adding the receipe
@login_required(login_url="/login/")
def receipes(request):
    if request.method=="POST":
        data=request.POST
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        receipe_image=request.FILES.get('receipe_image')
        # print(receipe_name)
        # print(receipe_description)
        # print(receipe_image)
        
        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image,
        )
        
        return redirect('/receipes/')
    querySet=Receipe.objects.all()
    
    if request.GET.get('search'):
        querySet=querySet.filter(receipe_name__icontains = request.GET.get('search'))
        
    context={'receipes':querySet}
    return render(request,'receipes/receipes.html',context)

#function for delete the receipe
def delete_receipe(request,id):
    queryset=Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/receipes/')

#function for update the receipe
def update_receipe(request,id):
    queryset=Receipe.objects.get(id=id)
    if request.method=="POST":
        data=request.POST
        
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        receipe_image=request.FILES.get('receipe_image')
        
        queryset.receipe_name=receipe_name
        queryset.receipe_description=receipe_description
        
        if receipe_image:
            queryset.receipe_image=receipe_image
        
        queryset.save() 
        return redirect('/receipes/')   
    context={'receipe':queryset}
    return render(request,'receipes/update_receipes.html',context)

#function for login
def login_page(request):
     if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
         
        if not User.objects.filter(username=username).exists():
            messages.error(request,"Invalid Username")
            return redirect('/login/')
        
        user = authenticate(username=username,password=password)
        
        if user is None:
            messages.error(request,"Invalid Password")
            return redirect('/login/')
            
        else:
            login(request,user)
            return redirect('/receipes/')     
     return render(request,'receipes/login.html')

#function for registartion
def register(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "username already taken")
            return redirect('/register/')
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            
        )
        
        user.set_password(password)
        user.save()
        messages.info(request, "Account created successfully")
        return redirect('/register/')
    return render(request,'receipes/register.html')

#function for logout
def logout_page(request):
    logout(request)
    return redirect('/login/')

def get_students(request):
    queryset=Student.objects.all()
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-student_age')
    
    if request.GET.get('search'):
        search=request.GET.get('search')
        queryset=queryset.filter(
            Q(student_name__icontains= search) |
            Q(department__department__icontains= search) |
            Q(student_id__student_id__icontains= search) |
            Q(student_email__icontains= search) |
            Q(student_age__icontains= search)
        )
        
    paginator = Paginator(queryset, 25)  # Show 25 student per page.

    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)
    return render(request,'report/student.html',{'queryset':page_obj})



from .seed import generate_report_card
def see_marks(request,student_id):
    # generate_report_card()
    queryset=SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks=queryset.aggregate(total_marks=Sum('marks'))
    
    return render(request,'report/see_marks.html',{'queryset':queryset,'total_marks':total_marks})

