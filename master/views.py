from django.shortcuts import render, redirect, get_object_or_404
from .models import Department,User,Designation,Location
from .forms import DepartmentForm,Designation_Add_Form,LocationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection

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
           
          
            return render(request, template_name, context)
            
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors to debug
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else :
        print("Rendering form")
        return render(request, template_name, context)
    
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
            return redirect('indexpage')
        else:
            print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else:
        return render(request, template_name, context)
    

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


def department_delete(request, pk):
    department = Department.objects.get(department_id=pk)
    
    department.delete()
    return redirect('department_list')

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
           
          
            return render(request, template_name, context)
            
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors to debug
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else :
        print("Rendering form")
        return render(request, template_name, context)
    
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


def designation_delete(request, pk):
    designation = Designation.objects.get(designation_id=pk)
    
    designation.delete()
    return redirect('designation_list')

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
           
          
            return render(request, template_name, context)
            
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors to debug
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else :
        print("Rendering form")
        return render(request, template_name, context)

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
def location_edit(request, pk):
    template_name = 'master/location_edit.html'
    loc_obj = Location.objects.get(location_id=pk)
    form = LocationForm(instance=loc_obj)
    context = {'form': form, 'des_obj': loc_obj}
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
    
def location_delete(request, pk):
    location = Location.objects.get(location_id=pk)
    
    location.delete()
    return redirect('location_list')