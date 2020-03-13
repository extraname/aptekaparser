import csv
import datetime
import requests
from bs4 import BeautifulSoup


class AptekaParser:

    def __init__(self, name):
        self.name = name
        self.links_for_search = []
        self.links_list = []
        self.list_of_results = []

    def find_drug(self):
        drug = self.name.lower()
        response = requests.get(
            f"https://apteka911.com.ua/drugs/search?query={drug}")

        soup = BeautifulSoup(response.text, 'html.parser')


        name_block = soup.find('ul', {'class': "symptoms-list-all"})
        link_list = name_block.find_all('li')

        for link in link_list:
            self.links_for_search.append(link.a['href'])


        return self.links_for_search

    def list_of_drug(self):

        for url in self.links_for_search:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            try:
                links = soup.find_all('div',
                                  {'class': 'block-prod-full extra-small'})
                for link in range(len(links)):
                    self.links_list.append(links[link].a["href"])

            except AttributeError:
                links = soup.find_all('div', {'class': "block-search-indexes"})
            for link in range(len(links)):
                self.links_list.append(links[link].a["href"])

        return self.links_list

    def parse_page(self):
        price_for = ''
        for link in self.links_list:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')

            product_name = soup.find_all('div',
                                         {'class': 'product-head-instr tl'})
            name = product_name[0].find("h1").text.split(" ")[0]

            try:
                price_blocks = soup.find_all('div', {'class': 'price-new'})

                if price_blocks[0].text is None:
                    price_for_table = 'Нет в наличии'
                else:
                    price = price_blocks[0].text
                    price_for_table = "".join(s for s in price
                                              if
                                              s.isdigit() or s == ',')

                price_for_block = soup.find("p", {
                    'class': 'mb10 fs10 text-grey packing-amount'})
                price_for = price_for_block.find('b').text

            except IndexError:
                if soup.find("div", {'class': 'price-new'}) is None:
                    price_for_table = 'Нет в наличии'
                else:
                    price = soup.find("div", {'class': 'price-new'}).text
                    price_for_table = "".join(s for s in price if
                                              s.isdigit() or s == ',')

            except AttributeError:
                if soup.find("div", {'class': 'price-new'}) is None:
                    price_for_table = 'Нет в наличии'
                else:
                    price = soup.find("div", {'class': 'price-new'}).text
                    price_for_table = "".join(s for s in price if
                                              s.isdigit() or s == ',')

            brand_block = soup.find('td', {'itemprop': 'brand'}).text
            brand = brand_block.strip().replace('\n', '')

            active_substance = soup.find_all('tr')[8]
            active_substance_text = active_substance.find_all('td')
            active_substance_mg = active_substance_text[1].text.strip()
            active_substance_mg_for_table = "".join(
                s for s in active_substance_mg
                if s.isdigit()
                or s == '+'
                or s == '/'
                or s == ','
                or s == 'в'
                or s == 'м'
                or s == 'г'
                or s == 'л')

            form_block = soup.find_all("tr")[4]
            form_block_text = form_block.find_all('td')
            form_for_table = form_block_text[1].text.strip().replace('\n', '')

            pack_block = soup.find_all("tr")[7]
            pack_block_text = pack_block.find_all('td')
            pack = pack_block_text[1].text.strip()

            today = datetime.datetime.today()

            result = name, price_for_table, price_for, brand, \
                     active_substance_mg_for_table, form_for_table, \
                     pack, today.strftime("%d/%m/%Y")
            self.list_of_results.append(result)

        return self.list_of_results

    def write_to_csv_file(self):
        with open("base.csv", 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for element in self.list_of_results:
                writer.writerow(element)


a = AptekaParser("Метронидазол")
a.find_drug()
a.list_of_drug()
a.parse_page()
a.write_to_csv_file()
