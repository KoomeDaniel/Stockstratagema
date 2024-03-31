from bs4 import BeautifulSoup
import requests
import pprint

def remove_duplicates(data):
    # Convert list of dictionaries to list of tuples
    data_tuples = [tuple(item.items()) for item in data]

    # Convert list of tuples to set to remove duplicates
    data_set = set(data_tuples)

    # Convert set back to list of dictionaries
    data_no_duplicates = [dict(item) for item in data_set]

    return data_no_duplicates

def bselosers():
    data = requests.get('https://www.moneycontrol.com/stocks/marketstats/bseloser/index.php').text
    soup = BeautifulSoup(data, 'lxml')

    allCompanies = soup.find_all('span', class_='gld13 disin')
    companyNames = [row.find('a').text for row in allCompanies]

    tablerow = soup.find_all('tr')
    companyHigh = []
    companyLow = []
    companyClose = []
    companyChange = []
    companyLoss = []

    for tr in tablerow:
        high = tr.find_all('td', attrs={'width': 75, 'align': 'right'})
        for i in high:
            companyHigh.append(i.text.replace(',', ''))
            break

        low = tr.find_all('td', attrs={'width': 80, 'align': 'right'})
        for i in low:
            companyLow.append(i.text.replace(',', ''))
            break

        close = tr.find_all('td', attrs={'width': 85, 'align': 'right'})
        for i in close:
            companyClose.append(i.text.replace(',', ''))
            break

        change = tr.find_all('td', attrs={'width': 45, 'align': 'right', "class": 'red'})
        for i in change:
            companyChange.append(i.text.replace(',', ''))
            break

        loss = tr.find_all('td', attrs={'width': 45, 'align': 'right', "class": 'red'})
        for i in loss:
            companyLoss.append(float(i.text.replace(',', '')))
            break

    companyData = []
    for i in range(len(companyNames)):
        companyData.append({
            'company': companyNames[i],
            'High': float(companyHigh[i]),
            'Low': float(companyLow[i]),
            'Change': float(companyChange[i]),
            'Loss_in_per': float(companyLoss[i]),
            'close_price': float(companyClose[i])
        })

    new_dict = sorted(companyData, key=lambda i: i['Loss_in_per'])
    new_dict = remove_duplicates(new_dict)
    return new_dict[:10]