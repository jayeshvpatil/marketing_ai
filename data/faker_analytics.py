from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta

fake = Faker()

# Actual values for source, medium, and campaign
source_values = ['google', 'referral', 'enterprisemarketingportal', 'brightedge']
medium_values = ['organic', 'paid', 'referral', 'none']
campaign_values = ['chrome_launch_switch', 'direct', 'organic', 'referral']
current_date = datetime.now()

# Generate fake data for the table
data = []
for _ in range(500):  # Number of records
    date = random_date = fake.date_between_dates(date_start=current_date - timedelta(days=365 * 3), date_end=current_date)
    source = random.choice(source_values)
    medium = random.choice(medium_values)
    campaign = random.choice(campaign_values)
    cost = round(random.uniform(2, 100), 2)
    impressions = fake.random_int(4, 10000)
    clicks = fake.random_int(3, 9000)
    users = fake.random_int(2, 1000)
    revenue = round(random.uniform(2, 1000), 2)
    conversion_rate = f"{fake.random_int(1, 30)}%"
    bounce_rate = f"{fake.random_int(5, 25)}%"
    time_on_site = f"{fake.random_int(1, 10)}m {fake.random_int(1, 59)}s"
    device_type = fake.random_element(elements=('Desktop', 'Mobile'))
    browser = fake.random_element(elements=('Chrome', 'Safari', 'Firefox'))
    satisfaction_score = random.choice([1,2,3,4, 5])  # Assuming CSAT score ranges from 1 to 5
    feedback_score = random.choice([3,4, 5])  # Assuming Feedback Score ranges from 1 to 5


    data.append([date, source, medium, campaign, cost, impressions, clicks, users, revenue, conversion_rate, bounce_rate, time_on_site, device_type, browser, satisfaction_score, feedback_score])

# Create a DataFrame
columns = ['date', 'source', 'medium', 'campaign', 'cost', 'impressions', 'clicks', 'users', 'revenue', 'conversion_rate', 'bounce_rate', 'time_on_site', 'device_type', 'browser', 'satisfaction_score', 'feedback_score']
df = pd.DataFrame(data, columns=columns)

# Save DataFrame to CSV
df.to_csv('data/generated_analytics_data.csv', index=False)
