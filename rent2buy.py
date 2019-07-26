from bs4 import BeautifulSoup
import re
import requests
import lxml


def run(url):
    currentCar = 0
    # totalCars = 41441
    totalCars = 40500

    csvFile = open('rent2buy-cars.csv', 'w')
    csvFile.write(
        "saving,actualPrice,diff,make,odometer,year,model,bodyStyle,kbbPrice,state,city,extColor,intColor,carUrl,driveLine,transmission,cityFuelEconomy,engine,doors,vin,zipCode,driveTrain,classification,trim,uuid,accountId,available\n")
    while currentCar < totalCars:
        # PageURL setup
        if currentCar == 0:
            pageUrl = url
        else:
            pageUrl = url + '?start=' + str(currentCar)

        # Increase the current car
        currentCar += 35
        htmlContent = None
        # retry 5 times
        for i in range(5):
            try:
                response = requests.get(pageUrl, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
                htmlContent = response.content
                break
            except Exception as e:
                print("Failed attempt: ", i)

        # If not get HTML content skip the page url
        if not htmlContent:
            continue

        # Parse HTML Content
        soup = BeautifulSoup(htmlContent.decode('ascii', 'ignore'), 'html.parser')
        cars = soup.findAll('li', {'class': re.compile('item hproduct clearfix closed used fleet')})

        # for each Car build parse data
        for car in cars:
            accountId = car['data-accountid']
            bodyStyle = car['data-bodystyle']
            city = car['data-city']
            classification = car['data-classification']
            doors = car['data-doors']
            drivetrain = car['data-drivetrain']
            engine = car['data-engine']
            make = car['data-make']
            model = car['data-model']
            state = car['data-state']
            transmission = car['data-transmission']
            trim = car['data-trim']
            uuid = car['data-uuid']
            vin = car['data-vin']
            year = car['data-year']
            zipcode = car['data-zipcode']
            carUrl = 'https://www.hertzcarsales.com' + car.find('a', {'class': re.compile('url')})['href']
            odometer = car.find('span', {'data-name': re.compile('odometer')}).span.text.split()[0].replace(',', '')
            extColor = car.find('span', {'data-name': re.compile('exteriorColor')}).span.text
            intColor = car.find('span', {'data-name': re.compile('interiorColor')}).span.text
            driveLine = car.find('span', {'data-name': re.compile('driveLine')}).span.text
            cityFuelEconomy = car.find('span', {'data-name': re.compile('cityFuelEconomy')}).span.text
            inventoryDate = car.find('span', {'data-name': re.compile('inventoryDate')}).span.text
            prices = car.findAll('span', {'class': re.compile('value')})
            kbbPrice = 0
            diffPrice = 0
            actualPrice = 0
            saving = 0.0
            if len(prices) == 3:
                kbbPrice = int(prices[0].text.strip().replace(',', '').replace('$', ''))
                diff = int(prices[1].text.strip().replace(',', '').replace('$', ''))
                actualPrice = int(prices[2].text.strip().replace(',', '').replace('$', ''))
                saving = diff / kbbPrice * 100
            else:
                actualPrice = int(prices[0].text.strip().replace(',', '').replace('$', ''))
                kbbPrice = actualPrice
            saving = round(saving, 2)
            csvFile.write(
                str(saving) + "," + str(actualPrice) + "," + str(
                    diff) + "," + make + "," + odometer + "," + year + "," + model + "," + bodyStyle + "," + str(
                    kbbPrice) + "," + state + "," + city + "," + extColor + "," + intColor + "," + carUrl + "," + driveLine + "," + transmission + "," + cityFuelEconomy + "," + engine + "," + doors + "," + vin + "," + zipcode + "," + drivetrain + "," + classification + "," + trim + "," + uuid + "," + accountId + "," + inventoryDate + "\n")
    csvFile.close()


if __name__ == '__main__':
    url = 'https://www.hertzcarsales.com/rent2buy-inventory/index.htm?geoZip=07306&geoRadius=5000'
    run(url)
