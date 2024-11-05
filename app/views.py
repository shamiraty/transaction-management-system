# views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

 
#******************************************************************************
#this function  creates  new transaction
@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction created successfully!")
            return redirect('transaction_create')
        else:
            messages.error(request, "There was an error creating the transaction.")
    else:
        form = TransactionForm()
    return render(request, 'index.html', {'form': form})

#******************************************************************************
#this function  list transactions on datatable
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})
#******************************************************************************
#this function  list transactions on datatable clicked item
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)   
    # Prepare the data to send back as JSON
    data = {
        'id': transaction.id,
        'created_date': transaction.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        'action': transaction.get_action_display(),  # Assuming this is a choice field
        'customer': transaction.customer,
        'amount': transaction.amount,
        'phonenumber': transaction.phonenumber,
        'updated_date': transaction.updated_date.strftime('%Y-%m-%d %H:%M:%S') if transaction.updated_date else '',
    } 
    return JsonResponse(data)

#******************************************************************************
#this function  update transactions on datatable click
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            #return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
        # Add a message to inform the user they are editing this transaction
        # messages.info(request, 'You are currently editing the transaction.')
    return render(request, 'transaction_update.html', {'form': form, 'transaction': transaction})

#******************************************************************************
#this function  delete transactions on datatable click
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transaction_list')
    return render(request, 'transaction_delete.html', {'transaction': transaction})
#******************************************************************************
#this function  performs  analysis
def transaction_summary(request):
    # Get today's date
    today = timezone.now()
    yesterday = today - timedelta(days=1)
    week_start = today - timedelta(days=today.weekday())  # Start of the current week
    month_start = today.replace(day=1)  # Start of the current month
    year_start = today.replace(month=1, day=1)  # Start of the current year

    # Define a dictionary to store each time period's data
    time_periods = {
        'yesterday': Transaction.objects.filter(created_date__date=yesterday.date()),
        'today': Transaction.objects.filter(created_date__date=today.date()),
        'this_week': Transaction.objects.filter(created_date__gte=week_start),
        'this_month': Transaction.objects.filter(created_date__gte=month_start),
        'this_year': Transaction.objects.filter(created_date__gte=year_start),
        'lifetime': Transaction.objects.all(),
    }

    # Compute count and sum for each network and action combination in each time period
    summary_data = {}
    for period, queryset in time_periods.items():
        data = queryset.values('network__name', 'action') \
            .annotate(count=Count('id'), total_amount=Sum('amount')) \
            .order_by('network__name', 'action')
        
        # Calculate grand totals for count and amount
        grand_total_count = sum(row['count'] for row in data)
        grand_total_amount = sum(row['total_amount'] or 0 for row in data)  # Handle None values
        
        summary_data[period] = {
            'data': data,
            'grand_total_count': grand_total_count,
            'grand_total_amount': grand_total_amount,
        }

    # Structure data for Chart.js
    chart_data = {}
    for period, queryset in time_periods.items():
        chart_data[period] = {
            'labels': [],
            'datasets': {},
        }
        for entry in queryset.values('network__name', 'action').annotate(count=Count('id')):
            network = entry['network__name']
            action = entry['action']
            count = entry['count']

            if network not in chart_data[period]['labels']:
                chart_data[period]['labels'].append(network)
            
            if action not in chart_data[period]['datasets']:
                chart_data[period]['datasets'][action] = []
            
            chart_data[period]['datasets'][action].append(count)

    context = {
        'summary_data': summary_data,
        'chart_data': chart_data,
    }
    return render(request, 'transaction_summary.html', context)

#******************************************************************************
#this function add product  to database
def add_product_batch(request):
    if request.method == 'POST':
        form = ProductBatchForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            product_description = form.cleaned_data['product_description']
            total_quantity = form.cleaned_data['total_quantity']
            total_purchasing_price = form.cleaned_data['total_purchasing_price']
            selling_price = form.cleaned_data['selling_price']
            tax_collection = form.cleaned_data['tax_collection']
            expiry_date = form.cleaned_data['expiry_date']
            category = form.cleaned_data['category']

            individual_purchasing_price = total_purchasing_price / total_quantity

            for _ in range(total_quantity):
                Product.objects.create(
                    product_name=product_name,
                    product_description=product_description,
                    purchasing_price=individual_purchasing_price,
                    selling_price=selling_price,
                    tax_collection=tax_collection,
                    expiry_date=expiry_date,
                    category=category
                )

            messages.success(request, f"{total_quantity} products have been successfully registered.")
            #return redirect('add_product_batch')

    else:
        form = ProductBatchForm()

    return render(request, 'add_product_batch.html', {'form': form})


#******************************************************************************

#this function list products, for the purpose of selling
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
#******************************************************************************

#this function sale product
@login_required
def create_sale(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Create a sale record
        sale = Sales(product=product, user=request.user)
        sale.save()

        # Create a sold product record
        sold_product = SoldProduct(
            product_name=product.product_name,
            product_description=product.product_description,
            purchasing_price=product.purchasing_price,
            selling_price=product.selling_price,
            tax_collection=product.tax_collection,
            expected_profit=product.expected_profit,
            barcode=product.barcode,
            expiry_date=product.expiry_date,
            category=product.category,
            user=request.user,
            profit=sale.profit
        )
        sold_product.save()

        # Remove the product after the sale
        product.delete()

        return JsonResponse({'success': True, 'message': 'Product sold successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

#******************************************************************************
#this function returns  sold product
def sold_product_list(request):
    sold_products = SoldProduct.objects.all()
    return render(request, 'sold_product_list.html', {'sold_products': sold_products})
#******************************************************************************

#this function show bootstrap modal to view product
def sold_product_detail(request, pk):
    sold_product = get_object_or_404(SoldProduct, pk=pk)
    data = {
        'product_name': sold_product.product_name,
        'product_description': sold_product.product_description,
        'purchasing_price': sold_product.purchasing_price,
        'selling_price': sold_product.selling_price,
        'tax_collection': sold_product.tax_collection.tax_collection,
        'expected_profit': sold_product.expected_profit,
        'barcode': sold_product.barcode,
        'expiry_date': sold_product.expiry_date,
        'category': sold_product.category.name,
        'profit': sold_product.profit,
        'user': sold_product.user.username,
        'created_at': sold_product.created_at,
        'updated_at': sold_product.updated_at,
    }
    return JsonResponse(data)
#******************************************************************************
#this can be deleted, it update products  but no this module in template
def update_sold_product(request, pk):
    sold_product = get_object_or_404(SoldProduct, pk=pk)
    if request.method == 'POST':
        form = SoldProductForm(request.POST, instance=sold_product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sold product updated successfully!')
            return redirect('sold_product_list')
        else:
            messages.error(request, 'There was an error updating the sold product.')
    else:
        form = SoldProductForm(instance=sold_product)
    
    return render(request, 'update_sold_product.html', {'form': form})

#******************************************************************************
#this function delete sold product
def delete_sold_product(request, pk):
    sold_product = get_object_or_404(SoldProduct, pk=pk)
    sold_product.delete()
    return JsonResponse({'success': True, 'message': 'Product deleted successfully'})

 
#******************************************************************************
#this function list products,  also view, delete and update
def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'product_list_view.html', {'products': products})
#******************************************************************************
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return JsonResponse({
        'product_name': product.product_name,
        'product_description': product.product_description,
        'purchasing_price': str(product.purchasing_price),
        'selling_price': str(product.selling_price),
        'expected_profit': str(product.expected_profit),
        'expiry_date': product.expiry_date,
    })

# views.py
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Product updated successfully!'})
           # return JsonResponse({'success': True})
        else:
            #return JsonResponse({'success': False})
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductForm(instance=product)
        return render(request, 'product_form.html', {'form': form, 'product': product})  # Pass product to template

#******************************************************************************
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return JsonResponse({'success': True})
#******************************************************************************
#product analytics
def analytics_page(request):
    # Product analytics
    categories = ProductCategory.objects.all()
    product_analytics_data = []

    grand_total_products = 0
    grand_total_purchasing_price = 0
    grand_total_selling_price = 0
    grand_total_expected_profit = 0

    for category in categories:
        products = Product.objects.filter(category=category)
        
        product_count = products.count()
        total_purchasing_price = products.aggregate(Sum('purchasing_price'))['purchasing_price__sum'] or 0
        total_selling_price = products.aggregate(Sum('selling_price'))['selling_price__sum'] or 0
        total_expected_profit = products.aggregate(Sum('expected_profit'))['expected_profit__sum'] or 0

        product_analytics_data.append({
            'category': category,
            'product_count': product_count,
            'total_purchasing_price': total_purchasing_price,
            'total_selling_price': total_selling_price,
            'total_expected_profit': total_expected_profit,
        })

        # Update grand totals
        grand_total_products += product_count
        grand_total_purchasing_price += total_purchasing_price
        grand_total_selling_price += total_selling_price
        grand_total_expected_profit += total_expected_profit

    # Sales analytics logic
    sales_analytics_data = {
        'today': SoldProduct.objects.filter(created_at__date=timezone.now().date()).aggregate(
            count=Count('id'),
            total_sales=Sum('selling_price'),
            total_profit=Sum('profit')
        ),
        'yesterday': SoldProduct.objects.filter(created_at__date=timezone.now().date() - timezone.timedelta(days=1)).aggregate(
            count=Count('id'),
            total_sales=Sum('selling_price'),
            total_profit=Sum('profit')
        ),
        'this_week': SoldProduct.objects.filter(created_at__week=timezone.now().isocalendar()[1]).aggregate(
            count=Count('id'),
            total_sales=Sum('selling_price'),
            total_profit=Sum('profit')
        ),
        'this_month': SoldProduct.objects.filter(created_at__month=timezone.now().month).aggregate(
            count=Count('id'),
            total_sales=Sum('selling_price'),
            total_profit=Sum('profit')
        ),
        'lifetime': SoldProduct.objects.aggregate(
            count=Count('id'),
            total_sales=Sum('selling_price'),
            total_profit=Sum('profit')
        ),
    }

    # Determine most sold products
    most_sold_products = SoldProduct.objects.values('product_name').annotate(
        total_sold=Count('id')
    ).order_by('-total_sold')[:5]  # Get top 5 most sold products

    context = {
        'product_analytics_data': product_analytics_data,
        'grand_total_products': grand_total_products,
        'grand_total_purchasing_price': grand_total_purchasing_price,
        'grand_total_selling_price': grand_total_selling_price,
        'grand_total_expected_profit': grand_total_expected_profit,
        'sales_analytics_data': sales_analytics_data,
        'most_sold_products': most_sold_products,
    }
    
    return render(request, 'analytics.html', context)

 
 
 
 
 
 
 


 
 
 
 
 
 
 
 
 
 
 
  