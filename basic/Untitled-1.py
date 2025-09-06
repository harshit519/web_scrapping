def scrape_data(base_url, endpoint, query_params_template, pages, name_class, price_class):
    """
    Scrapes product names and prices from a given e-commerce website.

    Args:
        base_url (str): Base URL of the e-commerce website.
        endpoint (str): Endpoint for product search.
        query_params_template (str): Query parameter template with placeholders.
        pages (int): Number of pages to scrape.
        name_class (str): HTML class name for product names.
        price_class (str): HTML class name for product prices.

    Returns:
        dict: A dictionary of product names as keys and prices as values.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac macOS 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    product_names = []
    product_prices = []

    for page in range(1, pages + 1):
        url = f"{base_url}{endpoint}" + query_params_template.format(page=page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # data=soup.find_all(class_=['tUxRFH'])
        # data_dict={el["class"][0]:el.text for el in data }
        # print(data)
        # exit()
        name_elements = soup.find_all(class_=name_class)
        price_elements = soup.find_all(class_=price_class)

        product_names.extend([name.text.strip() for name in name_elements])
        product_prices.extend([price.text.strip() for price in price_elements])

    return {name: price for name, price in zip(product_names,product_prices )}

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
    Scrapes iPhone data from Flipkart based on user-specified pages.
    """
    pages = int(request.GET.get('pages', 1))
    data = scrape_data(
        base_url='https://www.flipkart.com/',
        endpoint='search',
        query_params_template='?q=i+phone&page={page}',
        pages=pages,
        name_class='KzDlHZ',
        price_class='Nx9bqj _4b5DiR'
    )
    return render(request, "iphone.html", {"Iphones": data})

@login_required(login_url='/login/')
def iphone_amazon(request):
    """
    Scrapes iPhone data from Amazon based on user-specified pages.
    """
    pages = int(request.GET.get('pages', 1))
    data = scrape_data(
        base_url='https://www.amazon.in/',
        endpoint='s',
        query_params_template='?k=i+phones&page={page}',
        pages=pages,
        name_class='a-size-medium a-spacing-none a-color-base a-text-normal',
        price_class ='a-price-whole'
    )
    return render(request, "iphone.html", {"Iphones": data})

@login_required(login_url='/login/')
def samsung_flipkart(request):
    """
    Scrapes Samsung data from Flipkart based on user-specified pages.
    """
    pages = int(request.GET.get('pages', 1))
    data = scrape_data(
        base_url='https://www.flipkart.com/',
        endpoint='search',
        query_params_template='?q=samsung&page={page}',
        pages=pages,
        name_class='KzDlHZ',
        price_class='Nx9bqj _4b5DiR'
    )
    return render(request, "samsung.html", {"samsung": data})

@login_required(login_url='/login/')
def samsung_amazon(request):
    """
    Scrapes Samsung data from Amazon based on user-specified pages.
    """
    pages = int(request.GET.get('pages', 1))
    data = scrape_data(
        base_url='https://www.amazon.in/',
        endpoint='s',
        query_params_template='?k=samsung&page={page}',
        pages=pages,
        name_class='a-size-medium a-spacing-none a-color-base a-text-normal',
        price_class='a-price-whole'
    )
    return render(request, "samsung.html", {"samsung": data})