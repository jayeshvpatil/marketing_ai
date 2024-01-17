from faker import Faker
import pandas as pd
import random

# Create an instance of the Faker class
fake = Faker()

# Set seed for reproducibility
Faker.seed(0)
random.seed(0)

# Generate fake data and create a DataFrame
num_rows = 1000  # Adjust the number of rows as needed
data = {
    'ad_event_id': [fake.uuid4() for _ in range(num_rows)],
    'user_id': [fake.uuid4() for _ in range(num_rows)],
    'state': [fake.state() for _ in range(num_rows)],
    'os': [fake.random_element(elements=('Windows', 'Linux', 'Mac OS X')) for _ in range(num_rows)],
    'browser': [fake.random_element(elements=('Chrome', 'Firefox', 'Safari')) for _ in range(num_rows)],
    'id': [fake.uuid4() for _ in range(num_rows)],
    'gender': [fake.random_element(elements=('Male', 'Female')) for _ in range(num_rows)],
    'age': [fake.random_int(min=18, max=99) for _ in range(num_rows)],
    'keyword_id': [fake.uuid4() for _ in range(num_rows)],
    'ad_id': [fake.uuid4() for _ in range(num_rows)],
    'cpc_bid_amount': [round(random.uniform(0, 3000), 2) for _ in range(num_rows)],
    'bidding_strategy_type': [fake.random_element(elements=('Manual', 'Automated')) for _ in range(num_rows)],
    'quality_score': [round(random.uniform(0, 10), 2) for _ in range(num_rows)],
    'keyword_match_type': [fake.random_element(elements=('Exact', 'Broad', 'Phrase')) for _ in range(num_rows)],
    'ad_group_id': [fake.uuid4() for _ in range(num_rows)],
    'name': [fake.name() for _ in range(num_rows)],
    'amount': [round(random.uniform(0, 1000), 2) for _ in range(num_rows)],
    'device_type': [fake.random_element(elements=('Desktop', 'Mobile')) for _ in range(num_rows)],
}

# Create DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df.head())

df.to_csv("ads_data.csv")
