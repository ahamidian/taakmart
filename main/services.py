import requests
import json
import bs4
from main.models import Category, Product, Brand, Type


def get_all_categories():
    get_categories("food-beverage")


def get_categories(category_path, parent=None):
    url = "https://service2.digikala.com/api/Category/GetCategoryByPath?categoryPath=" + category_path
    headers = {'content-type': 'application/json', 'Mobile-Agent': 'MobileApp/Android/v-5/100',
               'ApplicationVersion': '10'}
    x = requests.get(url=url, headers=headers)
    if parent and len(json.loads(x.text)['Data']) > 0:
        parent.is_leaf = False
        parent.save()
    for category in json.loads(x.text)['Data']:
        new_category = Category.objects.create(pk=category["Id"],
                                               title=category["Title"],
                                               image=category["ImagePath"],
                                               url_code=category["UrlCode"],
                                               queryString=category["QueryStringValue"],
                                               level=category["QueryStringValue"].count("/") - 1,
                                               parent=parent if parent else None)
        get_categories(new_category.queryString, new_category)


def create_product_from_obj(text, category):
    product_list = []
    for product in json.loads(text)['hits']['hits']:
        if Brand.objects.filter(pk=product["_source"]["Brand"]["Id"]).__len__() > 0:
            brand = Brand.objects.get(pk=product["_source"]["Brand"]["Id"])
        else:
            brand = Brand.objects.create(pk=product["_source"]["Brand"]["Id"],
                                         title=product["_source"]["Brand"]["Title"])
        product_list.append(Product(pk=product["_id"],
                                    title=product["_source"]["FaTitle"],
                                    price=product["_source"]["MinPriceList"],
                                    discounted_price=product["_source"]["MinPrice"],
                                    image=product["_source"]["ImagePath"],
                                    existStatus=product["_source"]["ExistStatus"],
                                    brand=brand,
                                    parent=category))
    return product_list


def get_products_of_page(category, page_num, type=None):
    query = "type=" + str(type) + "&" if type else ""
    x = requests.get(
        "https://search.digikala.com/api2/search/get/?" + query + "pageSize=200&pageno=" + str(
            page_num) + "&category=" + str(category.id))
    return create_product_from_obj(x.text, category)


def get_page_count(category, type=None):
    query = "type=" + str(type) + "&" if type else ""
    url = "https://search.digikala.com/api2/search/get/?" + query + "pageSize=200&pageno=0&category=" + str(
        category.id)
    x = requests.get(url)
    print(json.loads(x.text)["trackerData"]["foundItems"])
    return json.loads(x.text)["trackerData"]["pages"], create_product_from_obj(x.text, category)


def get_products(category, type=None):
    page_count, product_list = get_page_count(category, type)
    for page_num in range(1, page_count):
        product_list.extend(get_products_of_page(category, page_num, type))
    return product_list


def save_product_list_in_db(product_list):
    for product in product_list:
        if Product.objects.filter(id=product.id).__len__() == 0:
            product.save()


def get_kinds_of_category(category):
    kinds = []
    headers = {'content-type': 'application/json', 'Mobile-Agent': 'MobileApp/Android/v-5/100',
               'ApplicationVersion': '10'}
    x = requests.get(
        "https://service2.digikala.com/api/ProductFilter/GetFilterAttributes?categoryUrlCode=" + category.queryString,
        headers=headers)
    json_data = json.loads(x.text)
    if json_data["Data"]["ProductTypes"]:
        for kind in json_data["Data"]["ProductTypes"]["Attributes"]:
            if Type.objects.filter(search_value=kind["SearchValue"].replace("Type-", "")).__len__() == 0:
                kinds.append(
                    Type.objects.create(title=kind["Title"], search_value=kind["SearchValue"].replace("Type-", ""),
                                        category=category))
            else:
                kinds.append(Type.objects.get(search_value=kind["SearchValue"].replace("Type-", "")))
    return kinds


def get_all_products():
    for category in Category.objects.filter(is_leaf=True):
        print(category.title)
        save_product_list_in_db(get_products(category))
        types = get_kinds_of_category(category)
        for type in types:
            print(type.title)
            products = get_products(category, type.search_value)
            for product in products:
                if Product.objects.filter(id=product.id).__len__() > 0:
                    Product.objects.get(id=product.id).types.add(type)
                else:
                    product.save()
                    product.types.add(type)


def get_all_brands():
    for brand in Brand.objects.all():
        print(brand.title)
        res = requests.get("https://www.digikala.com/brand/" + brand.title.replace(" ", "-"))
        soup = bs4.BeautifulSoup(res.text, "lxml")
        elems = soup.select('.c-brand-description__text')
        if len(elems) > 0:
            brand.description = elems[0].get_text()

        elems = soup.select('.c-brand-profile__avatar')
        if len(elems) > 0:
            brand.image = elems[0].get("style").replace("background-image: url(", "").replace(
                "?x-oss-process=image/resize,m_lfit,h_300,w_300/quality,q_80)", "")

        elems = soup.select('.c-brand-profile__username')
        if len(elems) > 0:
            brand.fa_title = elems[0].get_text()
        brand.save()
