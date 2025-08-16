from django.shortcuts import render,redirect 
from django.http import HttpRequest 
import requests 
from bs4 import BeautifulSoup 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basic.models import * 
from django.views.generic.edit import CreateView
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 
from django.urls import reverse



from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup

def scrape_data(base_url, endpoint, query_params_template, pages, name_class, price_class, link_selector=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    products = []
    
    for page in range(1, pages + 1):
        url = f"{base_url}{endpoint}" + query_params_template.format(page=page)
        
        response = requests.get(url, headers=headers)

        # Check for redirection or errors
        if response.status_code != 200 or "http404.php" in response.url:
            print(f"Error: Received {response.status_code} for {url}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        name_elements = soup.find_all(class_=name_class)
        price_elements = soup.find_all(class_=price_class)
        link_elements = soup.select(link_selector) if link_selector else []
        
        for i, name in enumerate(name_elements):
            price = price_elements[i].text.strip() if i < len(price_elements) else "N/A"
            link = link_elements[i]['href'] if i < len(link_elements) else "N/A"

            if link.startswith('/'):
                link = base_url.rstrip('/') + link

            products.append({
                'name': name.text.strip(),
                'price': price,
                'link': link
            })

    return products

@login_required(login_url='/login/')
def home(request):
    """
    Renders the home page and handles user input for selecting e-commerce options.

    Redirects to specific views based on user selection.
    """
    if request.method == 'POST':
        data = request.POST
        website = data.get('website')
        product = data.get('phone')
        pages = int(data.get('pages', 1))  # Default to 1 page if not provided

        if website == "Flipkart" and product == "Iphones":
            return redirect(f"/iphone_flipkart?pages={pages}")
        elif website == "Flipkart" and product == "Samsung":
            return redirect(f"/samsung_flipkart?pages={pages}")
        elif website == "Amazon" and product == "Iphones":
            return redirect(f"/iphone_amazon?pages={pages}")
        elif website == "Amazon" and product == "Samsung":
            return redirect(f"/samsung_amazon?pages={pages}")

    return render(request, "web.html")
@login_required(login_url='/login/')
def iphone_flipkart(request):
    """
    Scrapes iPhone data from Flipkart and implements pagination.
    """
    pages_to_scrape = int(request.GET.get('pages', 1))
    scraped_data = scrape_data(
        base_url='https://www.flipkart.com/',
        endpoint='search',
        query_params_template='?q=i+phone&page={page}',
        pages=pages_to_scrape,
        name_class='KzDlHZ',
        price_class='Nx9bqj _4b5DiR',
        link_selector='a.CGtC98'  # Update with the correct CSS selector for product links
    )

    paginator = Paginator(scraped_data, 25)  # 10 items per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)

    return render(request, "iphone.html", {"page_obj": page_obj})

@login_required(login_url='/login/')
def iphone_amazon(request):
    """
    Scrapes iPhone data from Amazon and implements pagination.
    """
    pages_to_scrape = int(request.GET.get('pages', 1))
    
    scraped_data = scrape_data(
        base_url='https://www.amazon.in/',
        endpoint='s',
        query_params_template='?k=i+phones&page={page}',
        pages=pages_to_scrape,
        name_class='a-size-medium a-spacing-none a-color-base a-text-normal',
        price_class='a-price-whole',
        link_selector='a.a-link-normal.s-no-outline'
    )
    
    paginator = Paginator(scraped_data, 25)  # 10 items per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)

    return render(request, "iphone.html", {"page_obj": page_obj})

@login_required(login_url='/login/')
def samsung_flipkart(request):
    """
    Scrapes Samsung data from Flipkart and implements pagination.
    """
    pages_to_scrape = int(request.GET.get('pages', 1))
    scraped_data = scrape_data(
        base_url='https://www.flipkart.com/',
        endpoint='search',
        query_params_template='?q=samsung&page={page}',
        pages=pages_to_scrape,
        name_class='KzDlHZ',
        price_class='Nx9bqj _4b5DiR',
        link_selector='a.CGtC98'
    )

    paginator = Paginator(scraped_data, 25)  # 10 items per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)

    return render(request, "samsung.html", {"page_obj": page_obj})

@login_required(login_url='/login/')
def samsung_amazon(request):
    """
    Scrapes Samsung data from Amazon and implements pagination.
    """
    pages_to_scrape = int(request.GET.get('pages', 1))
    scraped_data = scrape_data(
        base_url='https://www.amazon.in/',
        endpoint='s',
        query_params_template='?k=samsung&page={page}',
        pages=pages_to_scrape,
        name_class='a-size-medium a-spacing-none a-color-base a-text-normal',
        price_class='a-price-whole',
        link_selector='a.a-link-normal.s-no-outline'
    )

    paginator = Paginator(scraped_data, 25)  # 10 items per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)
    return render(request, "samsung.html", {"page_obj": page_obj})











def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username.')
            return redirect(reverse('login'))

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid username or password.')
            return redirect(reverse('login'))

        login(request, user)
        return redirect(reverse('home'))

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect(reverse('login'))

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect(reverse('register'))

        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password
            )
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect(reverse('login'))
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect(reverse('register'))

    return render(request, 'register.html')
