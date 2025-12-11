import sentence as sen

import even_odd

sentence = input("Enter the Sentence :")

sen.sentence_check(sentence)

numbers = input("Enter the numbers separated by commas :")
num_list = [int(n.strip()) for n in numbers.split(",")]
    
even,odd = even_odd.count_even_odd(num_list)

print("Even Numbers : ", even)
print("Odd Numbers : ", odd)


'''Q3:
Given a CSV file Products.csv with columns:
Write a Python program to:

a) Read the CSV

b) Print each row in a clean format

c) Total number of rows

d) Total number of products priced above 500
e) Average price of all products
f) List all products belonging to a specific category (user input)
g) Total quantity of all items in stock'''



import csv

# a) Read the CSV file
filename = "Products.csv"

rows = []
with open(filename, "r") as file:
    csvreader = csv.DictReader(file)
    for row in csvreader:
        rows.append(row)

# b) Print each row in a clean format
print("---- Product List ----")
for r in rows:
    print(f"ID: {r['product_id']}, Name: {r['product_name']}, Category: {r['category']}, "
          f"Price: {r['price']}, Quantity: {r['quantity']}")

# c) Total number of rows
print("\nTotal number of rows:", len(rows))

# d) Total number of products priced above 500
count_above_500 = sum(1 for r in rows if float(r['price']) > 500)
print("Products priced above 500:", count_above_500)

# e) Average price of all products
avg_price = sum(float(r['price']) for r in rows) / len(rows)
print("Average price of all products:", avg_price)

# f) List all products belonging to a specific category (user input)
search_category = input("\Enter category to search: ")

print(f"\nProducts under category '{search_category}':")
for r in rows:
    if r['category'].lower() == search_category.lower():
        print(f"- {r['product_name']} (Price: {r['price']}, Qty: {r['quantity']})")

# g) Total quantity of all items in stock
total_qty = sum(int(r['quantity']) for r in rows)
print("\nTotal quantity of all items in stock:", total_qty)
