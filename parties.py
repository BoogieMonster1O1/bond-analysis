from pypdf import PdfReader
from dataclasses import dataclass
import csv

@dataclass
class Party:
    srno: int
    encashment_date: str
    name: str
    account_number: str
    prefix: str
    bond_number: int
    denominations: str
    pay_branch_code: str
    pay_teller: int

parties = []
reader = PdfReader("parties.pdf")
number_of_pages = len(reader.pages)

for i in range(0, number_of_pages):
    page = reader.pages[i]
    text = page.extract_text()
    lines = text.splitlines()
    for line in lines:
        words = line.split(' ')
        if not words[0].isdigit():
            continue

        if words[-1] == "":
            words.pop()

        srno = int(words[0])
        encashment_date = words[1]
        name = " ".join(words[2:-6])
        account_number = words[-6]
        prefix = words[-5]
        bond_number = int(words[-4])
        denomination = words[-3]
        pay_branch_code = words[-2]
        pay_teller = int(words[-1])

        party = Party(srno, encashment_date, name, account_number, prefix, bond_number, denomination, pay_branch_code, pay_teller)
        parties.append(party)

with open('parties.csv', 'w', newline='') as csvfile:
    fieldnames = ['srno', 'encashment_date', 'name', 'account_number', 'prefix', 'bond_number', 'denominations', 'pay_branch_code', 'pay_teller']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for party in parties:
        writer.writerow(party.__dict__)
