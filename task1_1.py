import pandas as pd
from pymongo import MongoClient

# Step 1: Load the CSV
df = pd.read_csv('coffee_sales.csv')  # Replace with your actual file name

# Step 2: Preprocessing - Remove missing or empty card IDs
df = df.dropna(subset=['card'])               
df = df[df['card'].str.strip() != '']

# Step 3: Convert 'datetime' to datetime object
df['datetime'] = pd.to_datetime(df['datetime'])

# Step 4: Extract day, month, year, time
df['day'] = df['datetime'].dt.day
df['month'] = df['datetime'].dt.month
df['year'] = df['datetime'].dt.year
df['time'] = df['datetime'].dt.strftime('%H:%M:%S')

# Step 5: Prepare triplets (also prepare documents for MongoDB)
triplets = []
mongo_documents = []

for _, row in df.iterrows():
    triplet = f"<{row['coffee_name']}, {row['card']}, {row['money']}, {row['day']}, {row['month']}, {row['year']}, {row['time']}>"
    triplets.append(triplet)
    
    document = {
        "coffee_type": row['coffee_name'],
        "user_id": row['card'],
        "money": row['money'],
        "day": row['day'],
        "month": row['month'],
        "year": row['year'],
        "time": row['time']
    }
    mongo_documents.append(document)

# Step 6: Write triplets to text file
with open('task1_1_output.txt', 'w') as f:
    for triplet in triplets:
        f.write(triplet + '\n')

print(f"Saved {len(triplets)} triplets to 'task1_1_output.txt'.")

# Step 7: Insert into MongoDB
# Connect to MongoDB (default localhost:27017)
client = MongoClient('mongodb://localhost:27017/')

# Use a database (creates if not exists)
db = client['coffee_db']

# Use a collection (creates if not exists)
collection = db['coffee_extracted']

# Optional: Clear old data if needed
collection.delete_many({})

# Insert all documents
collection.insert_many(mongo_documents)

print(f"Inserted {len(mongo_documents)} documents into MongoDB collection 'coffee_extracted'.")
