from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs
import xlsxwriter
import time
from requests.structures import CaseInsensitiveDict

# Налаштування WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Використовувати браузер без інтерфейсу
chrome_options.add_argument("--log-level=OFF")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--window-size=800,600")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
headers = CaseInsensitiveDict([
            ('X-Requested-With', 'XMLHttpRequest'),
            ('Accept', 'application/json')])
# URL для завантаження
url = "https://tabletki.ua/uk/%D0%A0%D0%B8%D0%BD%D1%82-%D0%BD%D0%B0%D0%B7%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9-%D1%81%D0%BF%D1%80%D0%B5%D0%B9-%D1%83%D0%B2%D0%BB%D0%B0%D0%B6%D0%BD%D1%8F%D1%8E%D1%89%D0%B8%D0%B9/25642/pharmacy/dnepr/"

# Створення WebDriver
service = Service(executable_path= 'E:\\Work\\Python\\Parser\\chromedriver\\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Завантаження сторінки
    driver.get(url)

    # Очікуємо завантаження сторінки
    wait = WebDriverWait(driver, 10)

    push = 0

    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".tabletki-adcontainer .col-12 button")))

            ActionChains(driver).move_to_element(button).perform()
            button.click()

            time.sleep(5)

        except Exception as e:
            print("Більше немає кнопки для натискання.")
            break

    # Після натискання всіх кнопок отримуємо HTML-контент
    html_content = driver.page_source

    # Знаходимо всі елементи з класом 'address-card'
    # table_rows = soup.findAll('article', class_='address-card')

    filename = 'Pharmacies.xls'
    xlsxFile = xlsxwriter.Workbook(r'Pharmacies.xlsx')
    worksheet = xlsxFile.add_worksheet()

    delimiter = ';'
    with open(filename, 'w') as file:
        line = "Назва;Адреса;Місто;Ціна"
        worksheet.write(0, 0, 'Назва')
        worksheet.write(0, 1, 'Адреса')
        worksheet.write(0, 2, 'Місто')
        worksheet.write(0, 3, 'Ціна')
        file.write('{}\n'.format(line))
        i=0
        for el in html_content.select(".tabletki-adcontainer > .address-card"):
            i += 1
            # Get elements
            title_el = el.select(".address-card__header--name span")
            address_el = el.select(".address-card__header--address span")
            price_el = el.select(".filter-group__list--price")

            title = ' '.join(title_el[0].text.split())
            address1 = ' '.join(address_el[0].text.split())
            price = ' '.join(price_el[0].text.split())

            address_arr = address1.split(', ')
            city = address_arr[-1]
            del address_arr[-1]
            address = ', '.join(address_arr)

            worksheet.write(i, 0, title)
            worksheet.write(i, 1, address)
            worksheet.write(i, 2, city)
            worksheet.write(i, 3, price)


            line = title+';'+address+';'+city+';'+price
            if line:  # Проверка пустой строки
                # print(line)
                file.write('{}\n'.format(line))

    xlsxFile.close()



    print("Дані успішно збережено у файл 'results.txt'.")
    print(push)
    # Виводимо результати
    # for row in table_rows:
    #     print(row.text.strip())



except Exception as e:
    print(f"Виникла помилка: {e}")

finally:
    # Закриваємо драйвер
    driver.quit()
