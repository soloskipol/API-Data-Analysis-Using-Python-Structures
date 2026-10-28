from pprint import pprint
import requests
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

url = "https://jsonplaceholder.typicode.com/users"

# A folder to store the output files
output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)


# Get customer data from the API
def get_customers(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        my_data = response.json()  # Convert the response into Python data
        return my_data
    except requests.exceptions.RequestException as e:
        print("An error occurred when getting customer data", e)
        return None


# Explore the structure of the data and show the type of each value
def explore(record, indent=0):
    for key, value in record.items():
        print(" " * indent, key, ":", type(value).__name__)

        if isinstance(value, dict):
            explore(value, indent + 4)  # Explore nested dictionaries

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    explore(item, indent + 4)


# Extract the customer details needed and flatten the nested data
def extract_attributes(customers):
    new_customers = []

    for customer in customers:
        street = customer["address"]["street"]
        suite = customer["address"]["suite"]
        city = customer["address"]["city"]
        zipcode = customer["address"]["zipcode"]
        latitude = float(customer["address"]["geo"]["lat"])
        longitude = float(customer["address"]["geo"]["lng"])

        company_name = customer["company"]["name"]
        catch_phrase = customer["company"]["catchPhrase"]
        bs = customer["company"]["bs"]

        new_customer = {
            "id": customer["id"],
            "name": customer["name"],
            "user_name": customer["username"],
            "email": customer["email"],
            "street": street,
            "suite": suite,
            "city": city,
            "zipcode": zipcode,
            "latitude": latitude,
            "longitude": longitude,
            "phone": customer["phone"],
            "website": customer["website"],
            "company_name": company_name,
            "catch_phrase": catch_phrase,
            "bs": bs
        }

        new_customers.append(new_customer)

    return new_customers


# Find all the different cities using a set, this avoids duplicates
def unique_cities(customers):
    cities = {customer["address"]["city"] for customer in customers}
    return cities


# Count how many customers come from each city
def city_counts(customers):
    counts = {}

    for customer in customers:
        city = customer["address"]["city"]

        if city in counts:
            counts[city] += 1
        else:
            counts[city] = 1

    return counts


# Count customers by the last part of their email address
def email_domain_counts(customers):
    counts = {}

    for customer in customers:
        email = customer["email"]
        domain = email.split(".")[-1]  # Get the part after the last dot( i.e ".com" etc)

        if domain in counts:
            counts[domain] += 1
        else:
            counts[domain] = 1

    return counts


# Convert the extracted customer records into a DataFrame
def to_dataframe(rows):
    df = pd.DataFrame(rows)
    return df


# Create and save a bar chart showing the distribution
def plot_distribution(counts):
    plt.figure(figsize=(8, 5))
    plt.bar(list(counts.keys()), list(counts.values()), color="skyblue")

    plt.xlabel("Categories")
    plt.ylabel("Count")
    plt.title("Customer Distribution Chart")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(output_dir / "customer_distribution.png", dpi=300)
    plt.show()
    plt.close()


# Run the functions and save the results
customers = get_customers(url)

if customers:
    print("The data type is:", type(customers).__name__)
    print("Total Customers:", len(customers))
    print("-" * 30)

    print("Exploring first customer record structure:")
    explore(customers[0])
    print("-" * 30)

    flat_customers = extract_attributes(customers)
    print("Extracted attributes for", len(flat_customers), "customers.")
    print("-" * 30)

    cities = unique_cities(customers)
    print("Unique cities found:", cities)
    print("Total unique cities:", len(cities), "out of", len(customers), "total customers.")
    print("Marketing Insight: The sample shows how customers are distributed across cities. This information could help guide geographically targeted marketing, although a larger dataset would be needed for stronger conclusions.")
    print("-" * 30)

    c_counts = city_counts(customers)
    print("Customer counts per city:", c_counts)
    print("-" * 30)

    domain_counts = email_domain_counts(customers)
    print("Customer counts per email domain:", domain_counts)
    print("-" * 30)

    df = to_dataframe(flat_customers)
    print("DataFrame head:")
    print(df.head(3))

    # Save the flattened customer data as a CSV file
    df.to_csv(output_dir / "customers.csv", index=False)
    print("Saved:", output_dir / "customers.csv")
    print("-" * 30)

    # Save the city counts separately for further analysis
    city_df = pd.DataFrame(
        list(c_counts.items()),
        columns=["city", "customer_count"]
    )
    city_df.to_csv(output_dir / "city_counts.csv", index=False)
    print("Saved:", output_dir / "city_counts.csv")
    print("-" * 30)

    plot_distribution(c_counts)
    print("Saved:", output_dir / "customer_distribution.png")

else:
    print("No customer data was retrieved.")


# Show where the output files are stored
print("Output folder:", Path("output").resolve())