import csv
import requests
from bs4 import BeautifulSoup

r = requests.get("https://tallardapartments.appfolio.com/connect/ledger")
if r.status_code != 200:
    r.raise_for_status()
r.json()
print(r)

# def process_csv(filename):
#     file = open(filename, encoding="utf-8")
#     reader = csv.reader(file)
#     data = list(reader)
#     file.close()
#     return data

# #returns how much each person has paid total
# def paidByPerson(csv_rows):
#     tenants = {}
#     for row in csv_rows:
#         name = row[2]
#         payment = float(row[3])
#         if name not in tenants.keys():
#             tenants[name] = []
#         tenants[name].append(payment)
#     for key,payments in tenants.items():
#         tenants[key] = round(sum(payments), 2)
#     amt = 276.08
#     # paid back for first month of rent
#     tenants['Zachary Peetz'] -= amt
#     tenants['Zachary Olbrantz'] -= 233
#     #paid for first month of rent
#     tenants['Derrick Houmey'] += amt
#     tenants['William Ward'] += 233
#     return tenants

# #returns how much we have been charged in total
# def charged(csv_rows):
#     totalCharge = 0
#     for row in csv_rows:
#         charge = float(row[4])
#         totalCharge += charge
#     return totalCharge

# def paymentPerPerson(csv_rows):
#     tenants = {}
#     for row in csv_rows:
#         name=row[2]
#         if name not in tenants.keys():
#             tenants[name] = {}
#         payment = float(row[3])
#         date = row[0]
#         tenants[name][date] = payment
#     return tenants

# def prompts():
#     print("Pick a category:")
#     print("[1]: amount paid per person")
#     print('[2]: total amount charged')
#     print('[3]: charge per person')
#     print('[4]: total amount paid')
#     print('[5]: pay log for each person')
#     print('[6]: money owed per person')
#     print('[Q]: to quit')


# if __name__ == '__main__':
#     csv_data = process_csv('rent.csv')
#     csv_header = csv_data[0]
#     for header in csv_header:
#         header = header.replace('\t', '')
#     # print(csv_header)
#     csv_rows = csv_data[1:]
#     for row in csv_rows:
#         for i in range(len(row)):
#              row[i] = row[i].replace('\t', '')
#     # print(csv_rows[0:2])
#     num_rows = len(csv_rows)
#     # print(paymentPerPerson(csv_rows))
#     prompts()
#     while True:
#         inp = input("Enter your choice: ")
#         print()
#         if inp == '1':
#             tenants = paidByPerson(csv_rows)
#             print('Total paid per person:')
#             print(tenants,'\n')
#         elif inp == '2':
#             print('Tallard has charged a total amount of: $'+str(charged(csv_rows)))
#             print()
#         elif inp == '3':
#             charge_per_person = round((charged(csv_rows) / 7), 2)
#             print(f'Charge per person should be: ${charge_per_person}', '\n')
#         elif inp == '4':
#             print()
#             tenants = paidByPerson(csv_rows)
#             total = [value for (key, value) in tenants.items()]
#             total = sum(total)
#             print(f'Total amount paid by everyone: ${total}', '\n')
#         elif inp =='5':
#             print()
#             tenants = paymentPerPerson(csv_rows)
#             print(f'Log of payments for each person: ','\n')
#             for tenant, payments in tenants.items():
#                 if tenant == 'Tallard':
#                     continue
#                 print(tenant, ': ')
#                 print('Dates          Amount')
#                 for date, amount in payments.items():
#                     currDate = date
#                     currAmount = amount
#                     print(f'{currDate}        ${currAmount}')
#                 print()
#         elif inp == '6':
#             tenants = paidByPerson(csv_rows)
#             tenants.pop('Tallard')
#             charge_per_person = round((charged(csv_rows) / 7), 2)
#             for tenant in tenants:
#                 tenants[tenant] -= charge_per_person
#                 tenants[tenant] = round(tenants[tenant],2)
#             print('Total owed/over per person:')
#             print(tenants)
#         elif inp == 'Q' or inp == 'q':
#             break
#         else:
#             prompts()
#     print()
