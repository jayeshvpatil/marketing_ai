from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta

fake = Faker()

# Actual values for source, medium, and campaign
source_values = ["youtube", "newsletter", "google", "linkedin", "twitter", "direct", "facebook", "instagram"]
medium_values = ["referral", "social", "video", "display", "social", "organic"]
campaign_values = ["new_product_launch", "brand_awareness", "lead_generation", "summer_sale", "customer_retention"]
current_date = datetime.now()

# Baseline CPC values (simplified for example purposes)
baseline_cpc = {
    "youtube": 0.20,
    "newsletter": 0.50,
    "google": 1.00,
    "linkedin": 2.00,
    "twitter": 0.30,
    "direct": 0.00,  # Assuming no cost for direct traffic
    "facebook": 0.25,
    "instagram": 0.40,
}
# Generate fake data for the table
data = []
for _ in range(500):  # Number of records
    date = random_date = fake.date_between_dates(date_start=current_date - timedelta(days=365 * 3), date_end=current_date)
    source = random.choice(source_values)
    medium = random.choice(medium_values)
    campaign = random.choice(campaign_values)

    # Adjusting CPC based on the source with a random fluctuation to simulate real-world variation
    base_cpc = baseline_cpc[source]
    cost_variation = random.uniform(-0.5, 0.5)  # Introduce some variation
    cpc = round(base_cpc + cost_variation, 2)

    # Ensure impressions are always greater than clicks
    impressions = fake.random_int(4, 10000)
    clicks = fake.random_int(3, impressions)  #
    cost = round(cpc * clicks, 2) 
    users = fake.random_int(1, clicks)  # Assuming users <= clicks
    conversions = fake.random_int(0, users)  # Assuming conversions <= users
    revenue = round(random.uniform(2, 1000), 2)
    conversion_rate = round((conversions / clicks) * 100, 2) if clicks > 0 else 0
    bounce_rate = round(100 - (users / clicks) * 100, 2) if clicks > 0 else 0
    time_on_site = f"{fake.random_int(30, 480)}"
    device_type = fake.random_element(elements=('Desktop', 'Mobile'))
    browser = fake.random_element(elements=('Chrome', 'Safari', 'Firefox'))
    satisfaction_score = random.choice([1,2,3,4, 5])  # Assuming CSAT score ranges from 1 to 5
    feedback_score = random.choice([3,4, 5])  # Assuming Feedback Score ranges from 1 to 5


    data.append([date, source, medium, campaign, cost, impressions, clicks, users, conversions,revenue, conversion_rate, bounce_rate, time_on_site, device_type, browser, satisfaction_score, feedback_score])

# Create a DataFrame
columns = ['date', 'source', 'medium', 'campaign', 'cost', 'impressions', 'clicks', 'users','conversions', 'revenue', 'conversion_rate', 'bounce_rate', 'time_on_site', 'device_type', 'browser', 'satisfaction_score', 'feedback_score']
df = pd.DataFrame(data, columns=columns)

# Save DataFrame to CSV
df.to_csv('data/generated_analytics_data.csv', index=False)
