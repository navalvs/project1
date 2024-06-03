from django.shortcuts import render, redirect, get_object_or_404
import csv
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.

def home(request):
    title = "Welcome to Home Page"
    context = {
        'title' : title,
    }
    return render(request, 'home.html', context)



@login_required
def list_items(request):
    form = StockSearchForm(request.POST or None)
    title = 'List of Items'
    queryset = Stock.objects.all()

    if request.method == 'POST':
        form = StockSearchForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            item_name = form.cleaned_data.get('item_name')
            
            if category:
                queryset = queryset.filter(category__name__icontains=category)
            if item_name:
                queryset = queryset.filter(item_name__icontains=item_name)

    context = {
        'title': title,
        'queryset': queryset,
        'form': form,
    }
    return render(request, 'list_items.html', context)



@login_required
def add_items(request):
    if request.method == 'POST':
        form = StockCreateForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            item_name = form.cleaned_data['item_name']
            
            # Check if a stock item with the same category and item name exists
            if Stock.objects.filter(category=category, item_name=item_name).exists():
                messages.error(request, "Item with the same category and name already exists.")
            else:
                form.save()
                messages.success(request, "Item added successfully.")
                return redirect ('/list_items')
    else:
        form = StockCreateForm()
    
    context = {
        'form': form,
        'title': "Add Item"
    }
    return render(request, 'add_items.html', context)



def update_quantity(request, pk):
    item = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        form = StockCreateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quantity updated successfully.')
            return redirect('/list_items')
    else:
        form = StockCreateForm(instance=item)

    return render(request, 'update_quantity.html', {'form': form})



def delete_item(request, item_id):
    try:
        item = Stock.objects.get(pk=item_id)
        item.delete()
        messages.success(request, f'Item "{item.item_name}" has been deleted successfully.')
    except Stock.DoesNotExist:
        messages.error(request, 'Item does not exist.')
    return redirect('list_items')





def export_stock_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock_items.csv"'

    writer = csv.writer(response)
    writer.writerow(['Category', 'Item Name', 'Quantity'])  # CSV header

    stock_items = Stock.objects.all()
    for item in stock_items:
        writer.writerow([item.category.name, item.item_name, item.quantity])

    return response



# def stock_detail(request, pk):
#     queryset = Stock.objects.get(id=pk)
#     context = {
    
#         'queryset' : queryset,
#     }
#     return render(request, "stock_detail.html", context)
def stock_detail(request, pk):
    try:
        instance = Stock.objects.get(id=pk)  # Corrected typo: Stock.objects.get
    except Stock.DoesNotExist:
        # Handle the case where the Stock object with the given id does not exist
        # You can customize this based on your application logic
        instance = None
    
    context = {
        'instance': instance,  # Changed queryset to instance
    }
    return render(request, "stock_detail.html", context)





# def issue_items(request, pk):
#     queryset = Stock.objects.get(id=pk)
#     form = IssueForm(request.POST or None, instance=queryset)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.quantity -= instance.issue_quantity
#         # instance.issue_by = str(request.user)
#         messages.success(request,"ISSUED SUCCESSFULLY" + str(instance.quantity) + " " + str(instance.item_name)+ "s now in store")
#         instance.save()
#         return redirect('/stock_detail/'+ str(instance.id))
    
#     context = {
#         'title' : ' Issue' + str(queryset.item_name),
#         'queryset' : queryset,
#         'form' : form,
#         'username' : 'Issue By' + str(request.user)
#     }
#     return render (request, 'add_items.html', context)


def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            issue_quantity = form.cleaned_data['issue_quantity']
            if issue_quantity <= instance.quantity:
                instance.quantity -= issue_quantity

                instance.issue_quantity = issue_quantity  # Set the issue quantity
                instance.receive_quantity = 0
                instance.issue_by = str(request.user)

                messages.success(request, f"ISSUED SUCCESSFULLY. {issue_quantity} {instance.item_name}s now in store")
                instance.save()
                return redirect('/stock_detail/'+ str(instance.id))
            else:
                messages.error(request, "Issue quantity cannot be greater than available quantity.")

    context = {
        'title' : ' Issue' + str(queryset.item_name),
        'queryset' : queryset,
        'form' : form,
        'username' : 'Issue By' + str(request.user)
    }
    return render (request, 'add_items.html', context)


def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.receive_by = str(request.user)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, f"Received {instance.receive_quantity} {instance.item_name}s successfully. Total quantity now: {instance.quantity}.")
        return redirect('/stock_detail/' + str(instance.id))

    context = {
        'title': 'Receive ' + str(queryset.item_name),
        'queryset': queryset,
        'form': form,
        'username': 'Received By ' + str(request.user)
    }
    return render(request, 'add_items.html', context)




# def reorder_level(request, pk):
#     stock_item = get_object_or_404(Stock, pk=pk)
#     form = ReorderLevelForm(request.POST or None, instance=stock_item)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Reorder Level for {stock_item.item_name} updated to {stock_item.reorder_level}.")
#             return redirect('/list_items')
#     context = {
#         'stock_item': stock_item,
#         'form': form,
#     }
#     return render(request, 'reorder_level.html', context)
def reorder_level(request, pk):
    stock_item = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        form = ReorderLevelForm(request.POST, instance=stock_item)
        if form.is_valid():
            form.save()
            return redirect('list_items')  # Redirect to the list items page after saving
    else:
        form = ReorderLevelForm(instance=stock_item)
    
    context = {
        'form': form,
    }
    return render(request, 'reorder_level.html', context)





# @login_required
# def list_history(request):
#     header = 'LIST OF IT'
#     queryset = StockHistory.objects.all()
#     context = {
#         'header': header,  # Corrected the typo here
#         'queryset': queryset
#     }
#     return render(request, 'list_history.html', context)




@login_required
def list_history(request):
    header = 'HISTORY'
    category_name = request.GET.get('category', '')  # Get the category name from the request
    item_name = request.GET.get('item_name', '')  # Get the item name from the request

    # Perform case-insensitive search on the related fields and order by last_update
    queryset = StockHistory.objects.filter(
        category__name__icontains=category_name,
        item_name__icontains=item_name
    ).order_by('-last_update')

    context = {
        'header': header,
        'queryset': queryset,
        'category_name': category_name,  # Pass category_name to the template for pre-filling search form
        'item_name': item_name,  # Pass item_name to the template for pre-filling search form
    }

    # Export data if requested
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stock_history.csv"'
        
        # Create a CSV writer
        writer = csv.writer(response)
        
        # Write CSV header
        writer.writerow(['ID', 'Category', 'Item Name', 'Quantity in Store', 'Issue Quantity', 'Receive Quantity', 'Issue By', 'Receive By', 'Last Updated'])
        
        # Write CSV data rows
        for instance in queryset:
            writer.writerow([
                instance.id,
                instance.category.name if instance.category else 'No Category',
                instance.item_name,
                instance.quantity,
                instance.issue_quantity,
                instance.receive_quantity,
                instance.issue_by,
                instance.receive_by,
                instance.last_update
            ])
        
        return response

    return render(request, 'list_history.html', context)



# @login_required
# def clear_history(request):
#     if request.method == "POST":
#         StockHistory.objects.all().delete()
#         messages.success(request, "Stock history has been cleared successfully.")
#     return redirect('list_history')