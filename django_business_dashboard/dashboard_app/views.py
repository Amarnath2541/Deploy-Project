import random
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Sum, Count, Avg, Q
from django.core.paginator import Paginator
from .models import Transaction

def seed_db_if_empty():
    if Transaction.objects.count() == 0:
        categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports']
        statuses = ['Completed', 'Pending', 'Refunded']
        names = ['Alice Smith', 'Bob Johnson', 'Charlie Brown', 'Diana Prince', 
                 'Evan Wright', 'Fiona Gallagher', 'George Clark', 'Hannah Abbott',
                 'Ian Malcolm', 'Julia Roberts', 'Kevin Bacon', 'Laura Croft']
        
        base_date = timezone.now() - timedelta(days=60)
        transactions = []
        for i in range(120):
            tx = Transaction(
                customer_name=random.choice(names),
                category=random.choice(categories),
                amount=round(random.uniform(15.0, 850.0), 2),
                status=random.choices(statuses, weights=[0.7, 0.2, 0.1])[0],
                date=base_date + timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))
            )
            transactions.append(tx)
        Transaction.objects.bulk_create(transactions)

def dashboard_view(request):
    seed_db_if_empty()

    # --- ORM Aggregations ---
    aggregates = Transaction.objects.aggregate(
        total_revenue=Sum('amount', filter=Q(status='Completed')),
        total_orders=Count('id'),
        avg_order_value=Avg('amount', filter=Q(status='Completed')),
        pending_orders=Count('id', filter=Q(status='Pending'))
    )

    total_revenue = aggregates['total_revenue'] or 0.0
    total_orders = aggregates['total_orders'] or 0
    avg_order_value = aggregates['avg_order_value'] or 0.0
    pending_orders = aggregates['pending_orders'] or 0

    # Aggregations for Charts
    category_sales = (
        Transaction.objects.filter(status='Completed')
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('category')
    )

    status_counts = (
        Transaction.objects.values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )

    # --- Search, Filter & Pagination ---
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()
    status_filter = request.GET.get('status', '').strip()

    queryset = Transaction.objects.all().order_by('-date')

    if search_query:
        queryset = queryset.filter(customer_name__icontains=search_query)
    if category_filter:
        queryset = queryset.filter(category=category_filter)
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    all_categories = Transaction.objects.values_list('category', flat=True).distinct()

    context = {
        'total_revenue': round(total_revenue, 2),
        'total_orders': total_orders,
        'avg_order_value': round(avg_order_value, 2),
        'pending_orders': pending_orders,
        'chart_categories': [item['category'] for item in category_sales],
        'chart_category_data': [round(item['total'], 2) for item in category_sales],
        'chart_statuses': [item['status'] for item in status_counts],
        'chart_status_data': [item['count'] for item in status_counts],
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'status_filter': status_filter,
        'all_categories': all_categories,
    }

    return render(request, 'dashboard_app/dashboard.html', context)
