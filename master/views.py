from django.shortcuts import render, redirect, get_object_or_404
from .models import Department,User,Designation,Location,Employee
from .forms import DepartmentForm,Designation_Add_Form,LocationForm,EmployeeForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse

# Create your views here.
def indexpage(request):
    return render(request, 'index.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
           
            login(request, user)
           
            return redirect('indexpage')
        else:
          
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def admin_logout(request):
    
    logout(request)
  
    return redirect(admin_login)

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
    print(departments,"departments")
    # Process the results
    context = {
        'departments': departments
    }
    
    return render(request, 'master/department_list.html', context)

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
    template_name = 'master/add_employee.html'
    context = {'form': form}
   
    if request.method == 'POST':
        print(request.user.id,"Form submitted")
        form = EmployeeForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("Form is valid")
            data = form.save()
            data.created_by =User.objects.get(id=request.user.id)
            data.save()
           
          
            return redirect('employee_list')
            
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors to debug
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form}
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
        e.emp_start_date, e.emp_end_date, 
        d.department_name, ds.designation_name, l.location_name
    FROM master_employee e
    LEFT JOIN master_department d ON e.department_id = d.department_id
    LEFT JOIN master_designation ds ON e.designation_id = ds.designation_id
    LEFT JOIN master_location l ON e.location_id = l.location_id;
    """
    
    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        employees = cursor.fetchall()  # Fetch all rows
    
    # Process the results
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
            'department_name': row[8],
            'designation_name': row[9],
            'location_name': row[10],
        }
        employee_list.append(employee)
    
    context = {
        'employees': employee_list
    }
    
    return render(request, 'master/employee_list.html', context)

@login_required(login_url='adlogin')
def employee_edit(request, pk):
    template_name = 'master/employee_edit.html'
    emp_obj = Employee.objects.get(employee_id=pk)
    form = EmployeeForm(instance=emp_obj)
    context = {'form': form, 'emp_obj': emp_obj}
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=emp_obj)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Employee Successfully Updated.', 'alert-success')
            return redirect('employee_list')
        else:
            print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else:
        return render(request, template_name, context)
    
@login_required(login_url='adlogin')    
def employee_delete(request, pk):
    employee = Employee.objects.get(employee_id=pk)
    
    employee.delete()
    return redirect('employee_list')