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

@dataclass
class Donation:
    bond_number: int
    urn: str
    journal_date: str
    purchase_date: str
    expiry_date: str
    encashment_date: str
    donor_name: str
    party_name: str
    denominations: str

donors = {}
parties = {}

with open('donors.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        donor = Donor(int(row['srno']), row['urn'], row['journal_date'], row['purchase_date'], row['expiry_date'], row['name'], row['prefix'], int(row['bond_number']), row['denominations'], row['issue_branch_code'], int(row['issue_teller']), row['status'])
        donors[donor.bond_number] = donor
        

with open('parties.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        party = Party(int(row['srno']), row['encashment_date'], row['name'], row['account_number'], row['prefix'], int(row['bond_number']), row['denominations'], row['pay_branch_code'], int(row['pay_teller']))
        parties[party.bond_number] = party

donations = []
        
for donor in donors.values():
    if donor.bond_number in parties:
        party = parties[donor.bond_number]
        donation = Donation(donor.bond_number, donor.urn, donor.journal_date, donor.purchase_date, donor.expiry_date, party.encashment_date, donor.name, party.name, donor.denominations)
        donations.append(donation)

with open('donations.csv', 'w', newline='') as csvfile:
    fieldnames = ['bond_number', 'urn', 'journal_date', 'purchase_date', 'expiry_date', 'encashment_date', 'donor_name', 'party_name', 'denominations']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for donation in donations:
        writer.writerow(donation.__dict__)
