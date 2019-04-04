import requests
import matplotlib.pyplot as plt

class russiaInDigitales:

    def __init__(self, string):
        self.id = string_id # Id товара или услуги
        try:
            int(self.id)
            self.flag = 'okdp=' # Поиск по окдп
        except:
            self.flag = 'industrial=' # Поиск по отрасли экономики
        self.url = "http://openapi.clearspending.ru/" \
        "restapi/v3/contracts/select/?" \
        + str(self.flag) + str(self.id) # URL товара или услуги
        self.data = requests.get(self.url) # Данные с АPI
        if self.data.text != "Data not found.":
            print("Идёт обработка данных, пожалуйста подождите")
            self.data_parse()
        else:
            print("Информация не найдена")

    def data_parse(self):
        self.regions_price = {str(i): 0 for i in range(1, 95)}
        self.regions_date = {}
        self.total_price = 0 # Кол-во потраченных денег на контракты во всех регионах
        try:
            self.data = self.data.json()
        except:
            print(self.data.text)
            return False
        for i in self.data["contracts"]["data"]:
            price = i.get("price")
            region = i.get("regionCode")
            if price != None:
                self.total_price += price
                try:
                    self.regions_price[region] += price
                except:
                    self.regions_price[region] = price
                date = i.get("publishDate")[:7]
                try:
                    self.regions_date[date] += price
                except:
                    self.regions_date[date] = price
        self.top = [i for i in self.regions_price.items() if i[1] != 0]
        self.top.sort()
        self.top2 = [i for i in self.regions_date.items()]
        self.top2.sort()
        self.print_price()

    def print_price(self):
        plt.bar([i[0] + "регион\n" + str(int(i[1])) + "₽" for i in self.top],
                [i[1] for i in self.top])
        plt.show()

        plt.bar([i[0] + "\n" + str(int(i[1])) + "₽" for i in self.top2],
                [i[1] for i in self.top2])
        plt.show()

print("Введите окдп товара")
string_id = input("Все окдп вы можете найти по адресу http://classifikators.ru/okdp\n")
obj = russiaInDigitales(string_id)