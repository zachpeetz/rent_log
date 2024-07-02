import creds #a python file that has personal login information
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


"""
This function takes in a list of lists, ledger_rows is each individual payment that has been made
The function sums up the total amount that the tenants have individually paid
Returns: a dict that has each tenant and their respective total lump sum paid
"""
def paidByPerson(ledger_rows):
    tenants = {}
    for row in ledger_rows:
        name = row[2]
        payment = float(row[4]) if row[4] else 0
        if name not in tenants.keys():
            if name == '':
                continue
            tenants[name] = []
        tenants[name].append(payment)
    for key, payments in tenants.items():
        tenants[key] = round(sum(payments), 2)
    return creds.personalPayment(tenants)


"""
This function takes in a list of lists, ledger_rows is each individual payment that has been made
The function sums up the total amount that the tenants have been charged
Returns: The lump sum
"""
def charged(ledger_rows):
    totalCharge = 0
    for row in ledger_rows:
        charge = float(row[3]) if row[3] else 0
        totalCharge += charge
    return totalCharge


"""
This function takes in a list of lists, ledger_rows is each individual payment that has been made
The function manipulates the data and creates a dictionary of each tenant and their respective payments
Returns: dict of tenants as keys, list of dates and payments as values 
"""
def paymentPerPerson(ledger_rows):
    tenants = {}
    for row in ledger_rows:
        name=row[2]
        if name not in tenants.keys():
            tenants[name] = {}
        payment = float(row[4]) if row[4] else 0
        date = row[0]
        tenants[name][date] = payment
    return tenants


"""These are the prompts that the user can select from
    Returns: nothing 
"""
def prompts():
    print("Pick a category:")
    print("[1]: amount paid per person")
    print('[2]: total amount charged')
    print('[3]: charge per person')
    print('[4]: total amount paid')
    print('[5]: pay log for each person')
    print('[6]: money owed per person')
    print('[Q]: to quit')

""" This can optionally turn on headless mode, useful for testing, creates a webdriver to use
    Returns: webdriver to use to scrape website
"""
def get_webdriver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    #suppress logging
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    
    #suppress unnecessary console messages
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-features=VizDisplayCompositor")
    return webdriver.Chrome(options=options)

"""
This is the main method of the rent web scraper
This gets and loads the proper webpage, using login credentials
Then it scrapes the data and cleans it to ensure useful and wanted information
Gives prompts to user for their usage
"""
if __name__ == '__main__':

    driver = get_webdriver(headless=True)  #set headless=False to see the browser
    
    try:
        driver.get('https://tallardapartments.appfolio.com/connect/users/sign_in')

        #enter login credentials
        username_input = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="email-input"]')
        username_input.send_keys(creds.username)

        password_input = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="password-input"]')
        password_input.send_keys(creds.password)


        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="sign-in-button" and @aria-label="Sign In"]'))
        )
        
        #click the Sign In button
        sign_in_button.click()
        
        print("Credentials successfully extracted and submitted.")

        # Wait for the home page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Payments'))
        )
        print("Logged into Home page successfully.")

        #navigate to the payments page
        payments_link = driver.find_element(By.LINK_TEXT, 'Payments')
        payments_link.click()

        print("Payments page loaded successfully.")

        #navigate to ledger
        driver.get('https://tallardapartments.appfolio.com/connect/ledger')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-footable'))
        )
        print("Ledger page loaded successfully.")

        #get html from ledger webpage
        html_content = driver.page_source

        # Save content to HTML file
        with open('ledger_page.html', 'w', encoding='utf-8') as file:
            file.write(html_content)

    finally:
        driver.quit()

    #load content from file
    with open('ledger_page.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    print("Loading content to scrape...")
    time.sleep(2)

    #parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    #find the table, has all information that is needed
    table = soup.find('table', {'class': 'tenant-ledger-table'})

    #find the headers, this will be the keys in our dictionary
    headers = table.find('thead').find_all('th')
    keys = [header.get_text(strip=True) for header in headers]

    #create dictionary
    ledger_data = {key: [] for key in keys}

    #find rows, has each payment
    rows = table.find('tbody').find_all('tr')

    #populate dict
    for row in rows:
        columns = row.find_all('td')
        for key, column in zip(keys, columns):
            ledger_data[key].append(column.get_text(strip=True))

    ledger_rows = []
    for i in range(len(ledger_data[keys[0]])):
        row = []
        for key in keys:
            cleaned_value = ledger_data[key][i].replace(',', '')  # remove commas from numeric values
            row.append(cleaned_value)
        ledger_rows.append(row)
    
    #remove unwanted data
    ledger_rows = [row for row in ledger_rows if row[0] not in ['04/11/2023', '04/13/2023', '04/22/2024']]

    prompts()
    while True:
        inp = input("Enter your choice: ")
        print()

        #user wants the total amount that has been paid per person
        if inp == '1':
            tenants = paidByPerson(ledger_rows)
            print('Total paid per person:')
            print(tenants,'\n')

        #user wants to see how much the tenants have been charged in total
        elif inp == '2':
            print('Tallard has charged a total amount of: $'+str(charged(ledger_rows)))
            print()

        #user wants to see how much each person should have paid evenly
        elif inp == '3':
            charge_per_person = round((charged(ledger_rows) / 7), 2)
            print(f'Charge per person should be: ${charge_per_person}', '\n')

        #user wants to see how much money has been paid altogether
        elif inp == '4':
            print()
            tenants = paidByPerson(ledger_rows)
            total = [value for (key, value) in tenants.items()]
            total = sum(total)
            print(f'Total amount paid by everyone: ${total}', '\n')

        #user wants to see the log of payments for each tenant
        elif inp =='5':
            print()
            tenants = paymentPerPerson(ledger_rows)
            print(f'Log of payments for each person: ','\n')
            for tenant, payments in tenants.items():
                if tenant == '':
                    continue
                print(tenant, ': ')
                print('Dates          Amount')
                for date, amount in payments.items():
                    currDate = date
                    currAmount = amount
                    print(f'{currDate}        ${currAmount}')
                print()
        
        #user wants to see how much each tenant needs to pay/is over
        elif inp == '6':
            tenants = paidByPerson(ledger_rows)
            tenants = creds.correct(tenants)
            charge_per_person = round((charged(ledger_rows) / 7), 2)
            for tenant in tenants:
                if tenant == '':
                    continue
                tenants[tenant] -= charge_per_person
                tenants[tenant] = round(tenants[tenant],2)
            print('Total owed/over per person:')
            print(tenants)

        #user wants to exit
        elif inp == 'Q' or inp == 'q':
            break
        else:
            prompts()

    print()