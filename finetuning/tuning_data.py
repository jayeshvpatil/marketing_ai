import pandas as pd

# Sample synthetic data for illustration
questions = [
    "What are the top campaigns with the highest conversion rates?",
    "How does user behavior correlate with revenue?",
    "What sources contribute significantly to total revenue?",
    "Can you identify any notable trends in campaign performance?",
    "What is the relationship between cost and user engagement?",
]

answers = [
    "The top campaigns with the highest conversion rates are X, Y, and Z.",
    "User behavior correlates positively with revenue, indicating a strong relationship.",
    "The sources that contribute significantly to total revenue are A, B, and C.",
    "There is a general upward trend in campaign performance over time.",
    "The relationship between cost and user engagement is not immediately apparent.",
]

# Creating a DataFrame
qa_df = pd.DataFrame({"input_text": questions, "output_text": answers})

# Splitting the dataset into training and validation sets
training_qa = qa_df.sample(frac=0.8, random_state=42)
validation_qa = qa_df.drop(training_qa.index)

# Saving the datasets as JSONL files
training_qa.to_json("finetuning/training_qa.jsonl", orient="records", lines=True)
validation_qa.to_json("finetuning/validation_qa.jsonl", orient="records", lines=True)

# Displaying a confirmation message
print("Training and validation datasets saved successfully.")
