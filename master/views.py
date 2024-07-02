from django.shortcuts import render, redirect, get_object_or_404
from .models import Department,User,Designation,Location,Employee,Skill
from .forms import DepartmentForm,Designation_Add_Form,LocationForm,EmployeeForm,SkillFormSet,User_Add_Form,User_Edit_Form
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def indexpage(request):
    return render(request, 'index.html')



def user_login(request):

    template_name = 'login.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_exist = User.objects.filter(username=username).exists()
       
        if user_exist:
           
            user = authenticate(request, username=username, password=password)
           
            if user is not None:
                if user.role == 'ADMIN' :
                   
                    login(request, user)
           
                    return redirect('indexpage')
                
                elif user.role == 'VIEWER':
                    login(request, user)
                    return redirect('indexpage')
                
                else:
                    context = {'msg': 'Invalid Username or Password!'}
                    return render(request, template_name, context)
            else:
                
                context = {'msg': 'Password is incorrect!'}
                return render(request, template_name, context)

        else:
            context = {'msg': 'User Does Not exist'}
            return render(request, template_name, context)  
            
    return render(request, template_name)


def admin_logout(request):
    
    logout(request)
  
    return redirect(user_login)

@login_required(login_url='adlogin')
def department_add(request):
    form = DepartmentForm()
    template_name = 'master/add_department.html'
    context = {'form': form}
    
    if request.method == 'POST':
        print(request.user.id,"Form submitted")
        form = DepartmentForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("Form is valid")
            data = form.save()
            data.created_by =User.objects.get(id=request.user.id)
            data.save()
           
          
            return redirect('department_list')
            
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors to debug
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else :
        print("Rendering form")
        return render(request, template_name, context)
    
@login_required(login_url='adlogin')    
def department_edit(request, pk):
    template_name = 'master/department_edit.html'
    dep_obj = Department.objects.get(department_id=pk)
    form = DepartmentForm(instance=dep_obj)
    context = {'form': form, 'dep_obj': dep_obj}
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance=dep_obj)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Department Successfully Updated.', 'alert-success')
            return redirect('department_list')
        else:
            print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else:
        return render(request, template_name, context)
    
@login_required(login_url='adlogin')
def department_list(request):
    # Write your raw SQL query
    sql_query = "SELECT * FROM master_department;"
    
    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        departments = cursor.fetchall()  # Fetch all rows
   
    # Process the results
    context = {
        'departments': departments
    }
    
    return render(request, 'master/department_list.html', context)


@login_required(login_url='adlogin')
def department_detail(request,pk):
     departments = get_object_or_404(Department,department_id=pk)
     print(departments,"kkkkk")
     context = {
        'departments': departments
    }
    
     return render(request, 'master/department_detail.html', context)

@login_required(login_url='adlogin')
def department_delete(request, pk):
    department = Department.objects.get(department_id=pk)
    
    department.delete()
    return redirect('department_list')

@login_required(login_url='adlogin')
def designation_add(request):
    form = Designation_Add_Form
    template_name = 'master/add_designation.html'
    context = {'form': form}
   
    if request.method == 'POST':
        print(request.user.id,"Form submitted")
        form = Designation_Add_Form(request.POST, request.FILES)
        
        if form.is_valid():
            print("Form is valid")
            data = form.save()
            data.created_by =User.objects.get(id=request.user.id)
            data.save()
           
          
            return redirect('designation_list')
            
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors to debug
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else :
        print("Rendering form")
        return render(request, template_name, context)
    

@login_required(login_url='adlogin')   
def designation_edit(request, pk):
    template_name = 'master/designation_edit.html'
    des_obj = Designation.objects.get(designation_id=pk)
    form = Designation_Add_Form(instance=des_obj)
    context = {'form': form, 'des_obj': des_obj}
    if request.method == 'POST':
        form = Designation_Add_Form(request.POST, request.FILES, instance=des_obj)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Designation Successfully Updated.', 'alert-success')
            return redirect('designation_list')
        else:
            print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else:
        return render(request, template_name, context)
@login_required(login_url='adlogin')    
def designation_list(request):
   
    sql_query = """
        SELECT d.designation_id, d.designation_name, d.description, dep.department_name
        FROM master_designation d
        LEFT JOIN master_department dep ON d.department_id = dep.department_id;
    """
    
   
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        designations = cursor.fetchall()  # Fetch all rows

   
    designation_list = [
        {
            'designation_id': row[0],
            'designation_name': row[1],
            'description': row[2],
            'department_name': row[3]
        }
        for row in designations
    ]
    print(designation_list,"designation_list")
   
    context = {
        'designation_list': designation_list
    }
    
    return render(request, 'master/designation_list.html', context)

@login_required(login_url='adlogin')
def designation_detail(request,pk):
     designation = get_object_or_404(Designation,designation_id=pk)
     department_name = designation.department.department_name
     context = {
        'designation': designation,
        'department_name':department_name
    }
    
     return render(request, 'master/designation_detail.html', context)

@login_required(login_url='adlogin')
def designation_delete(request, pk):
    designation = Designation.objects.get(designation_id=pk)
    
    designation.delete()
    return redirect('designation_list')
@login_required(login_url='adlogin')
def location_add(request):
    form = LocationForm
    template_name = 'master/add_location.html'
    context = {'form': form}
   
    if request.method == 'POST':
        print(request.user.id,"Form submitted")
        form = LocationForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("Form is valid")
            data = form.save()
            data.created_by =User.objects.get(id=request.user.id)
            data.save()
           
          
            return redirect('location_list')
            
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors to debug
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else :
        print("Rendering form")
        return render(request, template_name, context)
@login_required(login_url='adlogin')
def location_list(request):
   
    sql_query = "SELECT * FROM master_location;"
    
   
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        location = cursor.fetchall()  
    print(location,"departments")
   
    context = {
        'location': location
    }
    
    return render(request, 'master/location_list.html', context)


@login_required(login_url='adlogin')
def location_detail(request,pk):
     location = get_object_or_404(Location,location_id=pk)
    
     context = {
        'location': location
    }
    
     return render(request, 'master/location_detail.html', context)

@login_required(login_url='adlogin')
def location_edit(request, pk):
    template_name = 'master/location_edit.html'
    loc_obj = Location.objects.get(location_id=pk)
    form = LocationForm(instance=loc_obj)
    context = {'form': form, 'loc_obj': loc_obj}
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES, instance=loc_obj)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Location Successfully Updated.', 'alert-success')
            return redirect('location_list')
        else:
            print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else:
        return render(request, template_name, context)
    

@login_required(login_url='adlogin')    
def location_delete(request, pk):
    location = Location.objects.get(location_id=pk)
    
    location.delete()
    return redirect('location_list')

@login_required(login_url='adlogin')
def employee_add(request):
    form = EmployeeForm
    formset = SkillFormSet(queryset=Skill.objects.none())
    template_name = 'master/add_employee.html'
    context = {'form': form, 'formset': formset}
   
    if request.method == 'POST':
        print(request.user.id,"Form submitted")
        form = EmployeeForm(request.POST, request.FILES)
        formset = SkillFormSet(request.POST, queryset=Skill.objects.none())
        if form.is_valid() and formset.is_valid():
            print("Form is valid")
            data = form.save()
            data.created_by =User.objects.get(id=request.user.id)
            data.save()
            
            
            for skill_form in formset:
                skill = skill_form.save(commit=False)
                skill.employee = data
                skill.save()
          
            return redirect('employee_list')
            
        else:
            print("Form is not valid")
            print(form.errors)  
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form,'formset': formset}
            return render(request, template_name, context)
    else :
        print("Rendering form")
        return render(request, template_name, context)
    
def designations(request):
    department_id = request.GET.get('department')
    designations = Designation.objects.filter(department=department_id).all()
    return JsonResponse(list(designations.values('designation_id', 'designation_name')), safe=False)

def employee_list(request):
    # Write your raw SQL query
    sql_query = """
    SELECT 
        e.employee_id,e.join_date, e.emp_no, e.name, e.phone, e.address, 
        e.emp_start_date, e.emp_end_date,e.photo,e.status,
        d.department_name, ds.designation_name, l.location_name
    FROM master_employee e
    LEFT JOIN master_department d ON e.department_id = d.department_id
    LEFT JOIN master_designation ds ON e.designation_id = ds.designation_id
    LEFT JOIN master_location l ON e.location_id = l.location_id;
    """
    
   
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        employees = cursor.fetchall()  # Fetch all rows
    
   
    employee_list = []
    for row in employees:
        employee = {
            'employee_id':row[0],
            'join_date': row[1],
            'emp_no': row[2],
            'name': row[3],
            'phone': row[4],
            'address': row[5],
            'emp_start_date': row[6],
            'emp_end_date': row[7],
            'photo':settings.MEDIA_URL + row[8],
            'status':row[9],
            'department_name': row[10],
            'designation_name': row[11],
            'location_name': row[12],
        }
        employee_list.append(employee)
   
    context = {
        'employees': employee_list
    }
    
    return render(request, 'master/employee_list.html', context)

@login_required(login_url='adlogin')
def employee_edit(request, pk):
    template_name = 'master/employee_edit.html'
    emp_obj = get_object_or_404(Employee, employee_id=pk)
    related_model = get_object_or_404(Skill, employee_id=emp_obj)

    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=emp_obj)
        formset = SkillFormSet(request.POST, queryset=Skill.objects.filter(employee=emp_obj))
        
        if form.is_valid() :
         
            employee = form.save(commit=False)
            employee.save()
           
            if formset.is_valid():
                for i in formset:
                  
                    skill = i.save()
                    skill.employee = employee
                    skill.save()
             
            messages.success(request, 'Employee Successfully Updated.', 'alert-success')
            return redirect('employee_list')
        else:
            print(form.errors,"kkkk")
            print(formset.errors,"11111111111")
            messages.error(request, 'Data is not valid.', 'alert-danger')
    else:
        form = EmployeeForm(instance=emp_obj)
        formset = SkillFormSet(queryset=Skill.objects.filter(employee=emp_obj))
    
    context = {'form': form, 'formset': formset, 'emp_obj': emp_obj}
    return render(request, template_name, context)



@login_required(login_url='adlogin')
def employee_detail(request,pk):
     employee = get_object_or_404(Employee,employee_id=pk)
     department=employee.department.department_name
     designation=employee.designation.designation_name
     location=employee.location.location_name
     skills = Skill.objects.filter(employee=employee)
    
     context = {
        
        'employee': employee,
        'department':department,
        'location':location,
        'designation':designation,
        'skills': skills,
    }
    
     return render(request, 'master/employee_detail.html', context)
   
@login_required(login_url='adlogin')    
def employee_delete(request, pk):
    employee = Employee.objects.get(employee_id=pk)
    
    employee.delete()
    return redirect('employee_list')


def user_add(request):
    form = User_Add_Form
   
    template_name = 'accounts/user_add.html'
    
    context = {'form': form}
    if request.method == 'POST':
        form = User_Add_Form(request.POST, request.FILES)
        
        if form.is_valid() :
            data = form.save(commit=False)
           
            passw = data.password
            passw = make_password(passw)
            data.password = passw
           
            data.save()

            return redirect('employee_list')
        else:
           
            context = {'form': form,}
            return render(request, template_name, context)
    else:
        return render(request, template_name, context)
    


def user_list(request):
   
    sql_query = "SELECT * FROM master_user;"
    
   
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        user = cursor.fetchall()  
    
   
    context = {
        'user': user
    }
    
    return render(request, 'accounts/user_list.html', context)


@login_required(login_url='adlogin')
def user_detail(request,pk):
     user = get_object_or_404(User,id=pk)
    
     context = {
        'user': user
    }
    
     return render(request, 'accounts/user_detail.html', context)


def user_edit(request, pk):
    template_name = 'accounts/user_edit.html'
    user_obj = User.objects.get(id=pk)
   
    form = User_Edit_Form(instance=user_obj)
   
    context = {'form': form}
    if request.method == 'POST':
        form = User_Edit_Form(request.POST, request.FILES, instance=user_obj)
       
        if form.is_valid():
            data = form.save(commit=False)
           
            data.save()
           
            return redirect('user_list')
        else:
           
            context = {'form': form,}
            print(form.errors)
            return render(request, template_name, context)
    else:
        return render(request, template_name, context)
    


@login_required(login_url='adlogin')    
def user_delete(request, pk):
    user = User.objects.get(id=pk)
    
    user.delete()
    return redirect('user_list')