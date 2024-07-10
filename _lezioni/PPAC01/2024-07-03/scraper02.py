from pprint import pprint
import requests
from time import sleep
from random import uniform
from bs4 import BeautifulSoup


URL_BASE = 'https://www.subidddto.it/annunci-italia/vendita/usato/'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:109.0) Gecko/20100101 Firefox/113.0'
}

def scrape_page(page_num):
    query_str = {
        'q': 'spectrum+sinclair',
        'o': page_num,
        'order': 'priceasc'
    }

    # Effettua una richiesta GET al primo URL nella lista
    result = requests.get(URL_BASE, query_str, headers=headers)

    # Controlla se la richiesta ha avuto successo (status code 200)
    if result.status_code == 200:
        # Parsing del contenuto HTML della pagina utilizzando BeautifulSoup
        soup = BeautifulSoup(result.content, 'html.parser')

        # Seleziona gli elementi HTML corrispondenti ai prodotti desiderati
        # products = soup.select('div.items__item.item-card')
        products = soup.select('div[class*=SmallCard-module_card__]')
        # pprint(products)  # Stampa la lista di prodotti (opzionale)

        # Lista per memorizzare gli oggetti di interesse
        page_items = []

        # # Itera sui prodotti trovati
        for adv in products:
            # Estrae i dati di interesse dal prodotto corrente
            data = {
                'name': adv.select('h2[class*=ItemTitle-module_item-title__]'),  # Nome del prodotto
                'price': adv.select("p[class*=SmallCard-module_price__]"),  # Prezzo del prodotto
                'town': adv.select('span[class*=index-module_town__]'),  # Città del venditore
                'province': adv.select('span.city'),
            }   

            # for key in data:
            #     if data[key]:
            #         ...

            # Elabora i dati estratti
            for key, value in data.items():
                # Se l'elemento è presente, estrai il testo
                if value:
                    data[key] = value[0].get_text()
                # Se l'elemento non è presente, imposta il valore a None
                else:
                    data[key] = None
            
            # Pulisce il prezzo sostitendo "\xa0" con uno spazio e rimuovendo la
            # dicitura "Spedizione disponibile" se presente.
            if data['price'] is not None:
                data['price'] = data['price'].replace('\xa0',' ').replace('Spedizione disponibile', '')

            # Aggiunge i dati estratti alla lista
            page_items.append(data)

        # Restituisce i dati estratti
        return page_items
    

current_page = 1  # Contatore per la pagina corrente
max_page = int(input("Quante pagine vuoi visitare? (0 per tutte) "))
all_items = []  # Lista per memorizzare tutti gli oggetti estratti dalle pagine
tot_products = 0

while True:
    print(f"Scraping page {current_page}...")
    
    try:
        page_items = scrape_page(current_page)
    except requests.exceptions.ConnectionError as err:
        print("Connection error:", err)
        break
    except Exception as err:
        print("An error occurred:", err)
        break
    
    # tot_products += len(page_items)
    if page_items and (max_page == 0 or current_page < max_page):
        # all_items.append(page_items)  # [ [ {...}, {...}], [ {...}, {...} ] ]
        all_items += page_items # [ {...}, {...}, {...}, {...} ]
        # tot_products += len(page_items)
        current_page += 1
        sleep(uniform(1, 5))
    else:
        print("No more data to scrape!")
        break

tot_products += len(all_items)
print(f"Scraped {tot_products} items.")
pprint(all_items)