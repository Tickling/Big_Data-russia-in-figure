import requests
import matplotlib.pyplot as plt


def print_diagram(top):
    plt.pie([i[0] for i in top],
            labels=[i[1] for i in top],
            startangle=90,
            explode=[0.01 for i in top],
            autopct='%1.1f%%')
    plt.title("Распределение по регионам")
    plt.show()


def create_top(regions):
    price_all_regions = sum([regions[str(i)] for i in regions])
    top_regions = [(regions[str(i)], i)

                   for i in range(1, 95)

                   if regions[str(i)] != 0 and
                   (regions[str(i)] / price_all_regions) > 0.01]
    top_regions.sort(reverse=True)
    top_regions.append((price_all_regions - sum([i[0] for i in top_regions]), 'other'))
    print_diagram(top_regions)


def calculation(region, data, regions):
    total_price_region = 0
    for i in data["contracts"]["data"]:
        try:
            total_price_region += i["price"]
        except:
            continue
    regions[str(region)] += total_price_region


def test_id_region(id, region):
    url = "http://openapi.clearspending.ru/restapi/" \
          "v3/contracts/select/?okdp=" + id + \
          "&customerregion=" + str(region)
    data = requests.get(url)
    if data.text == "Data not found.":
        return False
    return data


def is_correct(number):
    if number < 10:
        return "0" + str(number)
    else:
        return number


def data_parse(id):
    regions = {str(i): 0 for i in range(1, 95)}
    for region in range(1, 95):
        region2 = is_correct(region)
        data = test_id_region(id, region2)
        if data:
            data = data.json()
            calculation(region, data, regions)
    create_top(regions)


def test_id(id):
    url = "http://openapi.clearspending.ru/" \
          "restapi/v3/contracts/select/?okdp=" + str(id)
    data = requests.get(url)
    if data.text == "Data not found.":
        print("Информация не найдена")
        return False
    print("Идёт обработка данных, пожалуйста подождите")
    return True


def start():
    id = input("Введите id товара или услуги - ")
    if test_id(id):
        data_parse(id)


while True:
    start()