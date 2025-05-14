from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.contrib import messages

from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
from datetime import datetime

import csv
from django.http import HttpResponse


def is_valid(param):
    return param != "" and param is not None

# Create your views here.


@login_required
def index(request):
    dept = Department.objects.all()
    items = Items.objects.all()
    history = History.objects.all()
    supp = Supplier.objects.all()
    # dept = Department.objects.all()
    total_items = len(items)
    out_of_stock = len(items.filter(amount__lt=20))
    suppliers = len(supp)
    issued = len(dept)

    context = {
        "total_items": total_items,
        "out_of_stock": out_of_stock,
        "suppliers": suppliers,
        "issued": issued,
        "dept": dept
    }
    items = items.values()
    if request.method == "POST":
        # Create the CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="quaterly-report.csv"'

        # Write model data to the CSV file
        writer = csv.writer(response)
        writer.writerow(['item', 'qty', 'issue', 'rate', 'amount'])
        total = 0
        for obj in items:
            total += obj['amount'] * obj['unit_rate']
            writer.writerow([obj['item_name'], obj['amount'], obj['unit_issue'],
                             obj['unit_rate'], obj['amount'] * obj['unit_rate']])

        writer.writerow(['Total', '', '', '', total])

        return response
    return render(request, 'index.html', context)


@login_required
def dept(request, pk):
    if request.method == "POST": 
        op_type = request.POST["op_type"]
        if op_type == "add":
            input_name = request.POST['input_name']
            input_voucher = request.POST['input_voucher']
            input_supplier_name = request.POST['input_supp_name']
            input_amount = request.POST['input_amount']
            # input_unit_issue = request.POST["input_unit_issue"]
            input_unit_rate = request.POST["input_unit_rate"]
            
            if input_supplier_name == "":
                messages.info(request, 'Select a Supplier!')
                return redirect('/store/' + pk)
            
            if validateRate(input_unit_rate) == False:
                messages.info(request, 'Input right Unit Rate!')
                return redirect('/store/' + pk)
            
            if Items.objects.filter(item_name=input_name).exists():
                if validate(input_amount) == True:
                    item = Items.objects.all().filter(item_name=input_name)[0]
                    amnt = int(input_amount)
                    item.amount += amnt
                    # item.unit_issue = input_unit_issue
                    item.unit_rate = input_unit_rate
                    item.save()
                    history = History.objects.create(item_name=item.item_name,
                                                    voucher_no=input_voucher,
                                                    description=input_supplier_name,
                                                    action="received",
                                                    amount=str(amnt),
                                                    bal=str(item.amount),
                                                    unit_issue=item.unit_issue,
                                                    unit_rate=input_unit_rate,
                                                    slug=item.slug)
                    history.save()
                    return redirect('/store/' + pk)
                else:
                    messages.info(request, 'Enter a valid Quantity!')
                    return redirect('/store/' + pk)
            else:
                messages.info(request, 'Item does not exist!')
                return redirect('/store/' + pk)
        elif op_type == "subtract":
            input_name = request.POST['input_name']
            input_voucher = request.POST['input_voucher']
            input_dept_name = request.POST['input_dept_name']
            input_amount = request.POST['input_amount']
            # input_unit_issue = request.POST["input_unit_issue"]
            # input_unit_rate = request.POST["input_unit_rate"]
            
            if input_dept_name == "":
                messages.info(request, 'Select a Department!')
                return redirect('/store/' + pk)
            
            # if validateRate(input_unit_rate) == False:
            #     messages.info(request, 'Input right Unit Rate!')
            #     return redirect('/store')
            
            if Items.objects.filter(item_name=input_name).exists():
                if validate(input_amount) == True:
                    item = Items.objects.all().filter(item_name=input_name)[0]
                    if item.amount >= int(input_amount):
                        amnt = int(input_amount)
                        item.amount -= amnt
                        item.save()
                        history = History.objects.create(item_name=item.item_name,
                                                        voucher_no=input_voucher,
                                                        description=input_dept_name,
                                                        action="issued",
                                                        amount=str(amnt),
                                                        bal=str(item.amount),
                                                        unit_issue=item.unit_issue,
                                                        unit_rate=item.unit_rate,
                                                        slug=item.slug)
                        history.save()
                        return redirect('/store/' + pk)
                    else:
                        messages.info(request, 'Not enough in stock!')
                        return redirect('/store/' + pk)
                else:
                    messages.info(request, 'enter a valid amount!')
                    return redirect('/store/' + pk)
            else:
                messages.info(request, 'Item does not exist!')
                return redirect('/store/' + pk)

    item_name_input = request.GET.get('item_name')
    min_amnt = request.GET.get('min_amnt')
    max_amnt = request.GET.get('max_amnt')
    issue_unit = request.GET.get('issue_unit')

    try:
        department = Department.objects.get(dept_name=pk)
    except:
        return redirect('/')
    # if is_in_department == False:
        # 
    # Check if the department is associated with the item
    # is_in_department = Items.departments.filter(pk=department.pk).exists()
    
    department = Department.objects.get(dept_name=pk)
    dep = Department.objects.all()
    items = Items.objects.filter(dept__id=department.pk).order_by('-modified_at')
    supp = Supplier.objects.all()

    if is_valid(item_name_input):
        items = items.filter(item_name__contains=item_name_input)

    if is_valid(min_amnt):
        items = items.filter(amount__gte=min_amnt)

    if is_valid(max_amnt):
        items = items.filter(amount__lt=max_amnt)

    if is_valid(issue_unit):
        items = items.filter(unit_issue__icontains=issue_unit)

    return render(request, 'dept1.html', {'department': dep, 'items': items, 'supplier': supp, "pk": pk})


@login_required
def newstock(request):
    if request.method == "POST":
        item_name = request.POST['item_name']
        item_amount = request.POST['item_amount']
        input_unit_issue = request.POST['input_unit_issue']
        input_unit_rate = request.POST['input_unit_rate']
        input_pack_amount = request.POST['input_pack_amount']
        item_name = item_name.strip()
        input_unit_issue = input_unit_issue.strip()
        
        if (item_name == "" or input_unit_issue == ""):
            messages.info(request, 'Enter valid name and unit of issue!')
            return redirect("/stock")

        if Items.objects.all().filter(item_name=item_name).exists():
            messages.info(request, 'Item already exist!')
            return redirect("/stock")
        else:
            test = uuid.uuid4()
            item = Items.objects.create(item_id=test,
                                         item_name=item_name, amount=item_amount, pack_amount=input_pack_amount, unit_issue=input_unit_issue, unit_rate=input_unit_rate)
            item.save()
            departments_ids = request.POST.getlist('departments')  # Assuming departments are selected in a form
            for department_id in departments_ids:
                department = get_object_or_404(Department, pk=department_id)
                item.dept.add(department)
            item = Items.objects.all().filter(item_name=item_name)[0]
            history = History.objects.create(item_id=str(item.item_id),
                                             item_name=item.item_name,
                                             voucher_no="",
                                             description="",
                                             action="added",
                                             amount=str(item_amount),
                                             bal=str(item.amount),
                                             unit_issue=input_unit_issue,
                                             unit_rate=input_unit_rate,
                                             slug=item.slug)
            history.save()
            return redirect("/stock")
    
    item_name_input = request.GET.get('item_name')
    min_amnt = request.GET.get('min_amnt')
    max_amnt = request.GET.get('max_amnt')
    issue_unit = request.GET.get('issue_unit')
    
    items = Items.objects.all().order_by('-modified_at')
    dept = Department.objects.all()
    units = Units.objects.all()

    if is_valid(item_name_input):
        items = items.filter(item_name__contains=item_name_input)

    if is_valid(min_amnt):
        items = items.filter(amount__gte=min_amnt)

    if is_valid(max_amnt):
        items = items.filter(amount__lt=max_amnt)

    if is_valid(issue_unit):
        items = items.filter(unit_issue__icontains=issue_unit)

    return render(request, "newstock.html", {"items": items, "department": dept, "units": units})


@login_required
def history(request):
    history = History.objects.all()
    dept = Department.objects.all()

    item_name_input = request.GET.get('item_name')
    description = request.GET.get('description')
    issue_unit = request.GET.get('issue_unit')
    # rate_unit = request.GET.get('rate_unit')
    min_date_string = request.GET.get('min_date')
    max_date_string = request.GET.get('max_date')
    action = request.GET.get('action')

    # if dept !=  "general":
    #     history = history.filter(description=dept)

    # if item != "":
    #     history = history.filter(slug=item)
    # else:
    if is_valid(item_name_input):
        history = history.filter(item_name__icontains=item_name_input)

    if is_valid(description):
        history = history.filter(description__icontains=description)

    if is_valid(action) and action != "Choose...":
        history = history.filter(action__iexact=action)

    if is_valid(issue_unit):
        history = history.filter(unit_issue__iexact=issue_unit)

    # if is_valid(rate_unit):
    #     print("rateping")
    #     history = history.filter(unit_rate=rate_unit)

    if is_valid(min_date_string):
        specific_date = datetime.strptime(
            min_date_string, '%Y-%m-%d').date()
        # print("min date", min_date_string)
        # print("specific date", specific_date)
        # formatted_date = specific_date.strftime('%B %d, %Y')
        history = history.filter(dateCreated__gte=specific_date)

    if is_valid(max_date_string):
        specific_date = datetime.strptime(
            max_date_string, '%Y-%m-%d').date()
        # formatted_date = specific_date.strftime('%B %d, %Y')
        history = history.filter(dateCreated__lt=specific_date)

    history = history.order_by('-date_created')
    history = history.values()
    if request.method == "POST":
        # Create the CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="my_model.csv"'

        # Write model data to the CSV file
        writer = csv.writer(response)
        writer.writerow(['date', 'item', 'voucher no', 'action',
                         'description', 'unit issue', 'unit rate', 'amount', 'balance'])
        for obj in history:
            writer.writerow([obj['dateCreated'], obj['item_name'], obj['voucher_no'], obj['action'],
                             obj['description'], obj['unit_issue'], obj['unit_rate'], obj['amount'], obj['bal']])

        return response

    p = Paginator(history, 7)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger73:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # print('obj', page_obj.object_list)
    acts = ["issued", "received", "removed", "added"]
    context = {'page_obj': page_obj, "actions": acts, "department": dept}

    return render(request, 'history.html', context)


@login_required
def delete(request, id):
    item = Items.objects.filter(item_id=id)[0]
    history = History.objects.create(item_id=str(item.item_id),
                                     item_name=item.item_name,
                                     voucher_no="",
                                     description="",
                                     action="removed",
                                     amount=str(item.amount),
                                     bal=str(0),
                                     unit_issue=item.unit_issue,
                                     unit_rate=item.unit_rate,
                                     slug=item.slug)
    history.save()
    items = Items.objects.filter(item_id=id).delete()
    return redirect("/stock")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credetials Invalid')
            return redirect('/login')
    else:
        return render(request, 'login.html')

    # return render(request, 'login.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def department(request):
    dept = Department.objects.all()

    if request.method == "POST":
        dept_name = request.POST["dept_name"]
        dept_name = dept_name.strip()

        if dept_name == "":
            messages.info(request, 'Enter a valid name!')
            return redirect("/department")
        if dept.filter(dept_name=dept_name).exists():
            messages.info(request, 'Department already exist!')
            return redirect("/department")

        dept = dept.create(dept_name=dept_name)

        dept.save()

        return redirect("/department")

    return render(request, 'department.html', {"department": dept})


@login_required
def removeDept(request, id):
    dept = Department.objects.filter(dept_name=id).delete()

    return redirect("/department")


@login_required
def outOfStock(request):
    items = Items.objects.all()
    dept = Department.objects.all()
    items = items.filter(amount__lt=11)
    arr = [item.item_name for item in items]
    return render(request, 'outofstock.html', {"names": arr, "department": dept})


@login_required
def suppliers(request):
    supp = Supplier.objects.all()
    dept = Department.objects.all()
    
    if request.method == "POST":
        supp_name = request.POST["supp_name"]
        supp_name = supp_name.strip()
    
        
        if supp_name == "":
            messages.info(request, 'Enter a valid name!')
            return redirect("/suppliers")

        if supp.filter(supp_name=supp_name).exists():
            messages.info(request, 'Supplier already exist!')
            return redirect("/suppliers")

        supp = supp.create(supp_name=supp_name)

        supp.save()

        return redirect("/suppliers")

    return render(request, 'supplier.html', {"supplier": supp, "department": dept})


@login_required
def removeSupp(request, id):
    supp = Supplier.objects.filter(supp_name=id).delete()

    return redirect("/suppliers")


@login_required
def units(request):
    unit = Units.objects.all()
    dept = Department.objects.all()
    
    if request.method == "POST":
        unit_name = request.POST["unit_name"]
        unit_code = request.POST["unit_code"]
        unit_name = unit_name.strip()
        unit_code = unit_code.strip()
    
        
        if unit_name == "" or unit_code == "":
            messages.info(request, 'Enter a valid name!')
            return redirect("/units")

        if unit.filter(unit_name=unit_name).exists():
            messages.info(request, 'Unit name already exist!')
            return redirect("/units")
        
        if unit.filter(unit_code=unit_code).exists():
            messages.info(request, 'Unit code already exist!')
            return redirect("/units")

        unit = unit.create(unit_name=unit_name, unit_code=unit_code)

        unit.save()

        return redirect("/units")

    return render(request, 'units.html', {"units": unit, "department": dept})

@login_required
def removeUnit(request, id):
    unit = Units.objects.filter(unit_name=id).delete()

    return redirect("/units")

@login_required
def updateUnit(request):
    if request.method == "POST":
        unit_id = request.POST["unit_id"]
        unit_name = request.POST["unit_name"]
        unit_code = request.POST["unit_code"]
        unit_name = unit_name.strip()
        unit_code = unit_code.strip()

        print('unit_name', unit_name)
        print('unit_code', unit_code)
    
        
        if unit_name == "" or unit_code == "":
            messages.info(request, 'Enter a valid name!')
            return redirect("/units")

        
        
        unit = get_object_or_404(Units, id=unit_id)
        if unit:
            unit.unit_name = unit_name
            unit.unit_code = unit_code

            unit.save()

            messages.info(request, 'Unit success fully updated')
            return redirect("/units")

    

    return redirect("/units")

@login_required
def updateStock(request):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        item_name = request.POST["item_name"]
        # input_unit_issue = request.POST["input_unit_issue"]
        # input_edit_pack_amount = request.POST["input_edit_pack_amount"]
        item_name = item_name.strip()
        item_id = item_id.strip()
        # input_unit_issue = input_unit_issue.strip()
        # input_edit_pack_amount = input_edit_pack_amount.strip()

    
        
        if item_name == "" or item_id == "":
            messages.info(request, 'Enter a valid name!')
            return redirect("/stock")

        
        
        item = get_object_or_404(Items, item_id=item_id)
        if item:
            item.item_name = item_name
            # item.pack_amount = input_edit_pack_amount
            # item.unit_issue = input_unit_issue

            item.save()

            messages.info(request, 'Item success fully updated')
            return redirect("/stock")

    

    return redirect("/units")

# @login_required
# def report(request):
#     allItems = []
#     for item in Items.objects.all():
        
#         monthly_avg = item.get_monthly_average_consumption()
#         weekly_avg = item.get_weekly_average_consumption()
        
#         allItems.append({
#             'item': item,
#             'monthly_avg': monthly_avg,
#             'weekly_avg': weekly_avg,
#         })

#     context = allItems

#     print(allItems)
#     # return render(request, 'inventory/item_detail.html', context)
