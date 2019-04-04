import requests
import matplotlib.pyplot as plt

class russiaInDigitales:

        def __init__(self, string_id):
                self.id = string_id#Id товара или услуги
                self.start()

        def start(self):
                try:
                        int(self.id)
                        self.flag = 'okdp='#Поиск по окдп
                except:
                        self.flag = 'industrial='#Поиск по отрасли экономики
                if self.test_id(): self.data_parse()

        def test_id(self):
                self.url = "http://openapi.clearspending.ru/" \
                      "restapi/v3/contracts/select/?"\
                           +str(self.flag)+str(self.id)#URL товара или услуги
                self.data = requests.get(self.url)#Данные с АPI
                if self.data.text == "Data not found.":
                        print("Информация не найдена")
                        return False
                print("Идёт обработка данных, пожалуйста подождите")
                return True

        def data_parse(self):
            self.regions_price = {str(i): 0 for i in range(1, 95)}#Словарь регионов
            self.regions_date = {}
            self.total_price = 0#Кол-во потраченных денег на контракты во всех регионах
            for region in range(1, 95):
                self.region2 = self.is_correct(region)#Номер региона
                self.data = self.test_id_region(region)#Данные с API с учётом региона
                if self.data:
                    self.data = self.data.json()#Данные в виде словаря
                    self.calculation(region)
            self.create_top_regions()
            self.create_top_date()

        def is_correct(self, region):
                if region < 10:
                        return "0" + str(region)
                else:
                        return region

        def test_id_region(self, region):
                url = "http://openapi.clearspending.ru/restapi/" \
                      "v3/contracts/select/?"+str(self.flag)+str(self.id)+ \
                      "&customerregion=" + str(region)#URL товари или услуги с учётом региона
                data = requests.get(url)
                if data.text == "Data not found.":
                        return False
                return data

        def calculation(self, region):
            for i in self.data["contracts"]["data"]:

                price = i.get("price")
                if price:
                    self.regions_price[str(region)] += i["price"]
                    self.total_price += i["price"]

                    date = i.get("publishDate")[:7]

                    try:
                        self.regions_date[date] += price
                    except:
                        self.regions_date[date] = price

        def create_top_regions(self):
            self.top_regions = [(self.regions_price[str(i)], str(i))
                                for i in range(1, 95)
                                if self.regions_price[str(i)] != 0]
            self.print_diagram_regions()

        def create_top_date(self):
            self.top_date = [(i, self.regions_date[i]) for i in self.regions_date]
            self.print_diagram_date()

        def print_diagram_regions(self):
            plt.bar([i[1] for i in self.top_regions],
                    [i[0] for i in self.top_regions])
            plt.title("Распределение по регионам\n" +
                      str(int(self.total_price))+" Рублей")
            plt.show()

        def print_diagram_date(self):
            plt.bar([(i[0])for i in self.top_date],
             [i[1] for i in self.top_date])
            plt.title("Распределение по месяцам\n" + str(int(self.total_price)) + " Рублей")
            plt.show()

while True:
    print(("Введите id товара или услиги"))
    string_id = input("Все id вы можете найти по адресу http://classifikators.ru/okdp\n")
    obj1 = russiaInDigitales(string_id)