from django.shortcuts import render, redirect, get_object_or_404
from .models import Department,User,Designation,Location,Employee,Skill
from .forms import DepartmentForm,Designation_Add_Form,LocationForm,EmployeeForm,SkillFormSet,User_Add_Form,User_Edit_Form,UploadFileForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from datetime import datetime
import openpyxl
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
    
# @login_required(login_url='adlogin')
# def department_list(request):
#     # Write your raw SQL query
#     sql_query = "SELECT * FROM master_department;"
    
#     # Execute the query
#     with connection.cursor() as cursor:
#         cursor.execute(sql_query)
#         departments = cursor.fetchall()  # Fetch all rows
   
#     # Process the results
#     context = {
#         'departments': departments
#     }
    
#     return render(request, 'master/department_list.html', context)


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
# def designation_list(request):
   
#     sql_query = """
#         SELECT d.designation_id, d.designation_name, d.description, dep.department_name
#         FROM master_designation d
#         LEFT JOIN master_department dep ON d.department_id = dep.department_id;
#     """
    
   
#     with connection.cursor() as cursor:
#         cursor.execute(sql_query)
#         designations = cursor.fetchall()  # Fetch all rows

   
#     designation_list = [
#         {
#             'designation_id': row[0],
#             'designation_name': row[1],
#             'description': row[2],
#             'department_name': row[3]
#         }
#         for row in designations
#     ]
#     print(designation_list,"designation_list")
   
#     context = {
#         'designation_list': designation_list
#     }
    
#     return render(request, 'master/designation_list.html', context)

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
    
# @login_required(login_url='adlogin')
# def location_list(request):
   
#     sql_query = "SELECT * FROM master_location;"
    
   
#     with connection.cursor() as cursor:
#         cursor.execute(sql_query)
#         location = cursor.fetchall()  
#     print(location,"departments")
   
#     context = {
#         'location': location
#     }
    
#     return render(request, 'master/location_list.html', context)


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

# def employee_list(request):
#     # Write your raw SQL query
#     sql_query = """
#     SELECT 
#         e.employee_id,e.join_date, e.emp_no, e.name, e.phone, e.address, 
#         e.emp_start_date, e.emp_end_date,e.photo,e.status,
#         d.department_name, ds.designation_name, l.location_name
#     FROM master_employee e
#     LEFT JOIN master_department d ON e.department_id = d.department_id
#     LEFT JOIN master_designation ds ON e.designation_id = ds.designation_id
#     LEFT JOIN master_location l ON e.location_id = l.location_id;
#     """
    
   
#     with connection.cursor() as cursor:
#         cursor.execute(sql_query)
#         employees = cursor.fetchall()  # Fetch all rows
    
   
#     employee_list = []
#     for row in employees:
#         employee = {
#             'employee_id':row[0],
#             'join_date': row[1],
#             'emp_no': row[2],
#             'name': row[3],
#             'phone': row[4],
#             'address': row[5],
#             'emp_start_date': row[6],
#             'emp_end_date': row[7],
#             'photo':settings.MEDIA_URL + row[8],
#             'status':row[9],
#             'department_name': row[10],
#             'designation_name': row[11],
#             'location_name': row[12],
#         }
#         employee_list.append(employee)
   
#     context = {
#         'employees': employee_list
#     }
    
#     return render(request, 'master/employee_list.html', context)

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


def employee_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    employees = Employee.objects.all()
    

    employees_skills = []
    for employee in employees:
        skills = employee.skills.all()
        employees_skills.append({
            'employee': employee,
            'skills': skills
        })

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            employees = employees.filter(join_date__range=[start_date, end_date])
        except ValueError:
            # Handle invalid date format
            pass

    if 'download' in request.GET:
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename=employee_report.xlsx'},
        )

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Employee Report'

        # Write the header
        headers = ['Employee Number', 'Name', 'Phone', 'Start Date', 'End Date', 'Status', 'Department', 'Designation', 'Location', 'Skills']
        sheet.append(headers)

        # Write the data
        for employee in employees:
          
            skills = Skill.objects.filter(employee=employee)
          
            skills_list = ", ".join([skill.skill_name for skill in skills])
            
            row = [
                employee.emp_no,
                employee.name,
                employee.phone,
                employee.emp_start_date.strftime('%Y-%m-%d') if employee.emp_start_date else '',
                employee.emp_end_date.strftime('%Y-%m-%d') if employee.emp_end_date else '',
                employee.status,
                employee.department.department_name if employee.department else '',
                employee.designation.designation_name if employee.designation else '',
                employee.location.location_name if employee.location else '',
                skills_list,
            ]
            sheet.append(row)
       

        workbook.save(response)
        return response
  
    context = {
        'employees': employees_skills,
        
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'master/employee_report.html', context)



def handle_uploaded_file(file):
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append(row)

    return data

def bulk_upload_dep(request):
   
    if request.method == 'POST':
       
        data = handle_uploaded_file(request.FILES['filename'])
      
        for row in data:
            
            if not Department.objects.filter(department_name=row[0]).exists():
                Department.objects.create(department_name=row[0],description=row[1])
        return redirect('department_list')
    
   
def bulk_upload_des(request):
    if request.method == 'POST':
       
        data = handle_uploaded_file(request.FILES['file'])
        print(data,"data")
       
        for row in data:
            department_name = row[0]
            designation_name = row[1]
            description = row[2]

         
            department = Department.objects.filter(department_name=department_name).first()
            if department and not Designation.objects.filter(designation_name=designation_name, department=department).exists():
                Designation.objects.create(department=department, designation_name=designation_name, description=description)

        return redirect('designation_list')
   
def bulk_upload_loc(request):
   
    if request.method == 'POST':
       
        data = handle_uploaded_file(request.FILES['file'])
      
        for row in data:
            
            if not Location.objects.filter(location_name=row[0]).exists():
                Location.objects.create(location_name=row[0],description=row[1])
        return redirect('location_list')
    

def save_uploaded_file(uploaded_file, save_directory):
    try:
        print("kkkkkkkkkkk",uploaded_file)
        # Ensure the save directory exists
        file_name, uploaded_file = next(iter(uploaded_file.items()))
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Construct the full path to save the file
        save_path = os.path.join(save_directory, uploaded_file.name)
        print(save_path,'save')
        # Save the file to the specified directory
        with default_storage.open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        print(f"File saved at {save_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def bulk_upload_emp(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')  # Accessing multiple files using getlist()
        print(files)
        photo_files = {file.name: file for file in files if file.name.endswith(('.png', '.jpg', '.jpeg'))} 
        save_directory = 'employee_photos'

        save_uploaded_file(photo_files, save_directory)
        print(photo_files,"photo_files") # Collect photo files
        errors = []
        for uploaded_file in files:
            try:
                data = handle_uploaded_file(uploaded_file)  # Process each file using your utility function

                for row in data:
                    join_date = row[0]
                    emp_no = row[1]
                    name = row[2]
                    phone = row[3]
                    address = row[4]
                    emp_start_date = row[5]
                    emp_end_date = row[6]
                    status = row[7]
                    department_name = row[8]
                    designation_name = row[9]
                    location_name = row[10]
                    photo_name  = row[11]
                    skills_data = row[12:]  # Assuming skills data starts from the 12th column onwards

                    # Check if the employee already exists
                    employee_exists = Employee.objects.filter(emp_no=emp_no).exists()
                    if employee_exists:
                        raise ValueError(f'Employee with Employee No. {emp_no} already exists.')

                    department = Department.objects.filter(department_name=department_name).first()
                    designation = Designation.objects.filter(designation_name=designation_name, department=department).first()
                    location = Location.objects.filter(location_name=location_name).first()

                    if not department or not designation or not location:
                        raise ValueError('Invalid department, designation, or location')

                   
                  
                    photo_file = photo_files.get(photo_name)
                    print(photo_file)
                   
                    employee = Employee.objects.create(
                        emp_no=emp_no,
                        join_date=join_date,
                        name=name,
                        phone=phone,
                        address=address,
                        emp_start_date=emp_start_date,
                        emp_end_date=emp_end_date,
                        status=status,
                        department=department,
                        designation=designation,
                        location=location,
                        photo='employee_photos'+'/'+photo_name
                    )

                    # Create associated skills
                    for i in range(0, len(skills_data), 2):  # Assuming each skill has two columns: skill_name and description
                        skill_name = skills_data[i]
                        skill_description = skills_data[i + 1]
                        Skill.objects.create(employee=employee, skill_name=skill_name, description=skill_description)
                

            except Exception as e:
                errors.append(str(e))

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, 'Employees uploaded successfully.')

        return redirect('employee_list')

    return render(request, 'employee_list.html')


def export_departments_to_excel(request):
   
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Departments'


    columns = ['Sl.No',  'Department Name', 'Description']
    row_num = 1

  
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    
    for index, department in enumerate(Department.objects.all(), start=1):
        row_num += 1
        row = [
            index,  # Sl.No
            department.department_name,
            department.description,
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=departments.xlsx'

    workbook.save(response)
    return response



def export_designations_to_excel(request):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Designations'

    columns = ['Sl.No', 'Department Name', 'Designation Name', 'Description']
    row_num = 1

   
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

   
    for index, designation in enumerate(Designation.objects.all(), start=1):
        row_num += 1
        row = [
            index, 
            designation.department.department_name if designation.department else '',
            designation.designation_name,
            designation.description,
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=designations.xlsx'

    workbook.save(response)
    return response


def export_locations_to_excel(request):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Locations'

    columns = ['Sl.No', 'Location Name', 'Description']
    row_num = 1

   
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

   
    for index, location in enumerate(Location.objects.all(), start=1):
        row_num += 1
        row = [
            index,  
            location.location_name,
            location.description,
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=locations.xlsx'

    workbook.save(response)
    return response


def export_employees_to_excel(request):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Employees'

  
    columns = ['Sl.No', 'Employee No', 'Join Date', 'Name', 'Phone', 'Address', 
               'Emp Start Date', 'Emp End Date', 'Status', 'Department', 'Designation', 'Location', 'Skills']

  
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.value = column_title

   
    employees = Employee.objects.all()

   
    for index, employee in enumerate(employees, start=2):
        skills = ', '.join([skill.skill_name for skill in employee.skills.all()])
        row = [
            index - 1, 
            employee.emp_no,
            employee.join_date.strftime('%Y-%m-%d'),
            employee.name,
            employee.phone,
            employee.address,
            employee.emp_start_date.strftime('%Y-%m-%d'),
            employee.emp_end_date.strftime('%Y-%m-%d'),
            employee.status,
            employee.department.department_name if employee.department else '',  
            employee.designation.designation_name if employee.designation else '',  
            employee.location.location_name if employee.location else '', 
            skills, 
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=index, column=col_num)
            cell.value = cell_value

   
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=employees.xlsx'

 
    workbook.save(response)

    return response


def emp_list_query(start_index, page_length, search_value, draw):
    script1 = ''' 
    SELECT 
        e.employee_id, e.join_date, e.emp_no, e.name, e.phone, e.address, 
        e.emp_start_date, e.emp_end_date, e.photo, e.status,
        d.department_name, ds.designation_name, l.location_name
    FROM master_employee e
    LEFT JOIN master_department d ON e.department_id = d.department_id
    LEFT JOIN master_designation ds ON e.designation_id = ds.designation_id
    LEFT JOIN master_location l ON e.location_id = l.location_id
    WHERE e.name <> 'ALL'
    '''
    
    script2 = ''' 
    SELECT COUNT(*) FROM master_employee e
    LEFT JOIN master_department d ON e.department_id = d.department_id
    LEFT JOIN master_designation ds ON e.designation_id = ds.designation_id
    LEFT JOIN master_location l ON e.location_id = l.location_id
    WHERE e.name <> 'ALL'
    '''
    
    if search_value:
        search_script = " AND e.name LIKE %s"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY e.name ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', int(page_length), int(start_index)))
        else:
            cursor.execute(script1, (int(page_length), int(start_index)))
        employees = cursor.fetchall()

        if search_value:
            cursor.execute(script2, ('%' + search_value + '%',))
        else:
            cursor.execute(script2)
        total_records = cursor.fetchone()[0]

    employee_list = []
    if start_index.isdigit():
        sl_no = int(start_index) + 1
    else:
        sl_no = 1

    for row in employees:
        employee = {
            'employee_id': row[0],
            'join_date': row[1],
            'emp_no': row[2],
            'name': row[3],
            'phone': row[4],
            'address': row[5],
            'emp_start_date': row[6],
            'emp_end_date': row[7],
            'photo': settings.MEDIA_URL + row[8],
            'status': row[9],
            'department_name': row[10],
            'designation_name': row[11],
            'location_name': row[12],
        }
        employee_list.append(employee)
        sl_no += 1

    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": employee_list
    }
    return response



@login_required(login_url='adlogin')
@csrf_exempt
def employee_list(request):
    if request.method == "GET":
        template_name = 'master/employee_list.html'
       
        return render(request, template_name, )

    if request.method == "POST":
        start_index = request.POST.get('start')
        page_length = request.POST.get('length')
        search_value = request.POST.get('search[value]')
        draw = request.POST.get('draw')
       
        emp = emp_list_query(start_index, page_length, search_value, draw)
       
        return JsonResponse(emp)
    


def department_list_query(start_index, page_length, search_value, draw):
    script1 = ''' 
    SELECT 
        d.department_id, d.department_name, d.description
    FROM master_department d
    WHERE d.department_name <> 'ALL'
    '''
    
    script2 = ''' 
    SELECT COUNT(*) FROM master_department d
    WHERE d.department_name <> 'ALL'
    '''
    
    if search_value:
        search_script = " AND d.department_name LIKE %s"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY d.department_name ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', int(page_length), int(start_index)))
        else:
            cursor.execute(script1, (int(page_length), int(start_index)))
        departments = cursor.fetchall()

        if search_value:
            cursor.execute(script2, ('%' + search_value + '%',))
        else:
            cursor.execute(script2)
        total_records = cursor.fetchone()[0]

    department_list = []
    if start_index.isdigit():
        sl_no = int(start_index) + 1
    else:
        sl_no = 1

    for row in departments:
        department = {
            'department_id': row[0],
            'department_name': row[1],
            'description': row[2]
        }
        department_list.append(department)
        sl_no += 1

    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": department_list
    }
    return response


@login_required(login_url='adlogin')
@csrf_exempt
def department_list(request):
    if request.method == "GET":
        template_name = 'master/department_list.html'
       
        return render(request, template_name, )

    if request.method == "POST":
        start_index = request.POST.get('start')
        page_length = request.POST.get('length')
        search_value = request.POST.get('search[value]')
        draw = request.POST.get('draw')
       
        dep = department_list_query(start_index, page_length, search_value, draw)
       
        return JsonResponse(dep)
    

    
def location_list_query(start_index, page_length, search_value, draw):
    script1 = ''' 
    SELECT 
        l.location_id, l.location_name, l.description
    FROM master_location l
    WHERE l.location_name <> 'ALL'
    '''
    
    script2 = ''' 
    SELECT COUNT(*) FROM master_location l
    WHERE l.location_name <> 'ALL'
    '''
    
    if search_value:
        search_script = " AND l.location_name LIKE %s"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY l.location_name ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', int(page_length), int(start_index)))
        else:
            cursor.execute(script1, (int(page_length), int(start_index)))
        locations = cursor.fetchall()

        if search_value:
            cursor.execute(script2, ('%' + search_value + '%',))
        else:
            cursor.execute(script2)
        total_records = cursor.fetchone()[0]

    location_list = []
    if start_index.isdigit():
        sl_no = int(start_index) + 1
    else:
        sl_no = 1

    for row in locations:
        location = {
            'location_id': row[0],
            'location_name': row[1],
            'description': row[2]
        }
        location_list.append(location)
        sl_no += 1

    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": location_list
    }
    return response


@login_required(login_url='adlogin')
@csrf_exempt
def location_list(request):
    if request.method == "GET":
        template_name = 'master/location_list.html'
       
        return render(request, template_name, )

    if request.method == "POST":
        start_index = request.POST.get('start')
        page_length = request.POST.get('length')
        search_value = request.POST.get('search[value]')
        draw = request.POST.get('draw')
       
        loc = location_list_query(start_index, page_length, search_value, draw)
       
        return JsonResponse(loc)

def designation_list_query(start_index, page_length, search_value, draw):
    script1 = ''' 
    SELECT 
        ds.designation_id, ds.designation_name, ds.description, 
        d.department_name
    FROM master_designation ds
    LEFT JOIN master_department d ON ds.department_id = d.department_id
    WHERE ds.designation_name <> 'ALL'
    '''
    
    script2 = ''' 
    SELECT COUNT(*) FROM master_designation ds
    LEFT JOIN master_department d ON ds.department_id = d.department_id
    WHERE ds.designation_name <> 'ALL'
    '''
    
    if search_value:
        search_script = " AND ds.designation_name LIKE %s"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY ds.designation_name ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', int(page_length), int(start_index)))
        else:
            cursor.execute(script1, (int(page_length), int(start_index)))
        designations = cursor.fetchall()

        if search_value:
            cursor.execute(script2, ('%' + search_value + '%',))
        else:
            cursor.execute(script2)
        total_records = cursor.fetchone()[0]

    designation_list = []
    if start_index.isdigit():
        sl_no = int(start_index) + 1
    else:
        sl_no = 1

    for row in designations:
        designation = {
            'designation_id': row[0],
            'designation_name': row[1],
            'description': row[2],
            'department_name': row[3]
        }
        designation_list.append(designation)
        sl_no += 1

    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": designation_list
    }
    return response


@login_required(login_url='adlogin')
@csrf_exempt
def designation_list(request):
    if request.method == "GET":
        template_name = 'master/designation_list.html'
       
        return render(request, template_name, )

    if request.method == "POST":
        start_index = request.POST.get('start')
        page_length = request.POST.get('length')
        search_value = request.POST.get('search[value]')
        draw = request.POST.get('draw')
       
        des = designation_list_query(start_index, page_length, search_value, draw)
       
        return JsonResponse(des)