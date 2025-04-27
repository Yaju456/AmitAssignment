import pandas as pd

# Load the CSV file
df = pd.read_csv('coffee_sales.csv')  # Replace 'your_file.csv' with your actual file name

# Drop transactions where 'card' is missing or empty
df = df.dropna(subset=['card'])               # Drop NaN
df = df[df['card'].str.strip() != '']          # Drop empty strings

# Convert 'datetime' column to pandas datetime type
df['datetime'] = pd.to_datetime(df['datetime'])

# Extract day, month, year, and time separately
df['day'] = df['datetime'].dt.day
df['month'] = df['datetime'].dt.month
df['year'] = df['datetime'].dt.year
df['time'] = df['datetime'].dt.strftime('%H:%M:%S')

# Prepare the triplets
triplets = []
for _, row in df.iterrows():
    triplet = f"<{row['coffee_name']}, {row['card']}, {row['money']}, {row['day']}, {row['month']}, {row['year']}, {row['time']}>"
    triplets.append(triplet)

# Write triplets to a text file
with open('task1_1_output.txt', 'w') as f:
    for triplet in triplets:
        f.write(triplet + '\n')

print("Triplets have been extracted and saved to 'task1_1_output.txt'.")
