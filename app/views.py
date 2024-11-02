# views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .models import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
#******************************************************************************
#this function  creates  new transaction
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



