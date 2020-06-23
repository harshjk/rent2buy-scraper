from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime


def run(url):
    current_car = 0
    total_cars = 1029
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    file_name = "rent2buy-cars" + dt_string + ".csv"
    csv_file = open(file_name, 'w+')
    csv_file.write(
        "saving,actual_price,diff,make,odometer,year,model,body_style,kbb_price,state,city,ext_color,int_color,car_url,drive_line,transmission,city_fuel_economy,engine,doors,vin,zipCode,driveTrain,classification,trim,uuid,account_id\n")
    while current_car < total_cars:
        # PageURL setup
        if current_car == 0:
            page_url = url
        else:
            page_url = url + '&start=' + str(current_car)

        # Increase the current car
        current_car += 35
        html_content = None
        # retry 5 times
        for i in range(5):
            try:
                response = requests.get(page_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
                html_content = response.content
                break
            except Exception as e:
                print("Failed attempt: ", i)

        # If not get HTML content skip the page url
        if not html_content:
            print("Cannot load HTML page for link: ", page_url)
            continue

        # Parse HTML Content
        soup = BeautifulSoup(html_content.decode('ascii', 'ignore'), 'html.parser')
        cars = soup.findAll('li', {'class': re.compile('item hproduct clearfix closed certified primary')})

        # for each Car build parse data
        for car in cars:
            account_id = car['data-accountid']
            body_style = car['data-bodystyle']
            city = car['data-city']
            classification = car['data-classification']
            doors = car['data-doors']
            drive_train = car['data-drivetrain']
            engine = car['data-engine']
            make = car['data-make']
            model = car['data-model']
            state = car['data-state']
            transmission = car['data-transmission']
            trim = car['data-trim']
            uuid = car['data-uuid']
            vin = car['data-vin']
            year = car['data-year']
            zip_code = car['data-zipcode']
            drive_line = car['data-driveline']
            city_fuel_economy = car['data-cityfueleconomy']
            ext_color = car['data-exteriorcolor']
            int_color = car['data-interiorcolor']
            car_url = 'https://www.hertzcarsales.com' + car.find('a', {'class': re.compile('url')})['href']
            odometer = car.find('span', {'data-name': re.compile('odometer')}).span.text.split()[0].replace(',', '')
            prices = car.findAll('span', {'class': re.compile('value')})
            kbb_price = 0
            diff_price = 0
            actual_price = 0
            saving = 0.0
            if len(prices) == 3:
                kbb_price = int(prices[0].text.strip().replace(',', '').replace('$', ''))
                diff = int(prices[1].text.strip().replace(',', '').replace('$', ''))
                actual_price = int(prices[2].text.strip().replace(',', '').replace('$', ''))
                saving = diff / kbb_price * 100
            else:
                try:
                    actual_price = int(prices[0].text.strip().replace(',', '').replace('$', ''))
                    kbb_price = actual_price
                except Exception as e:
                    print("Failed to convert Integer: ", e)
                diff = 0
            saving = round(saving, 2)
            csv_file.write(
                str(saving) + "," + str(actual_price) + "," + str(
                    diff) + "," + make + "," + odometer + "," + year + "," + model + "," + body_style + "," + str(
                    kbb_price) + "," + state + "," + city + "," + ext_color + "," + int_color + "," + car_url + "," + drive_line + "," + transmission + "," + city_fuel_economy + "," + engine + "," + doors + "," + vin + "," + zip_code + "," + drive_train + "," + classification + "," + trim + "," + uuid + "," + account_id + "\n")
    csv_file.close()


if __name__ == '__main__':
    scrapping_url = 'https://www.hertzcarsales.com/used-cars-for-sale.htm?geoZip=07306&geoRadius=200&normalBodyStyle=SUV'
    run(scrapping_url)
