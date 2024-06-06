from pypdf import PdfReader
from dataclasses import dataclass
import csv

@dataclass
class Donor:
    srno: int
    urn: str
    journal_date: str
    purchase_date: str
    expiry_date: str
    name: str
    prefix: str
    bond_number: int
    denominations: int
    issue_branch_code: str
    issue_teller: int
    status: str

donors = []
reader = PdfReader("donors.pdf")
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
        urn = words[1]
        journal_date = words[2]
        purchase_date = words[3]
        expiry_date = words[4]
        name = " ".join(words[5:-6])
        prefix = words[-6]
        bond_number = int(words[-5])
        denomination = words[-4]
        issue_branch_code = words[-3]
        issue_teller = int(words[-2])
        status = words[-1]

        donor = Donor(srno, urn, journal_date, purchase_date, expiry_date, name, prefix, bond_number, denomination, issue_branch_code, issue_teller, status)
        
        donors.append(donor)

with open('donors.csv', 'w', newline='') as csvfile:
    fieldnames = ['srno', 'urn', 'journal_date', 'purchase_date', 'expiry_date', 'name', 'prefix', 'bond_number', 'denominations', 'issue_branch_code', 'issue_teller', 'status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for donor in donors:
        writer.writerow(donor.__dict__)
