import pandas as pd
import json

# Read the CSV file
# outputfile of extract here
df = pd.read_csv('')

# Drop NaN values
df.dropna(subset=['Rating', 'Review'], inplace=True)

# Drop a row if the number of entries is odd
if len(df) % 2 != 0:
    df = df[:-1]

# Split the dataframe into two equal halves
half_size = len(df) // 2
df_train = df[:half_size]
df_test = df[half_size:]

# Function to determine the new rating
def get_new_rating(rating):
    if rating >= 1 and rating <= 5:
        return 0
    elif rating >= 6 and rating <= 10:
        return 1
    else:
        return None

# Extract 'new_rating' and 'Review' columns for training data
train_data = []
for _, row in df_train.iterrows():
    rating = int(row['Rating'])
    new_rating = get_new_rating(rating)
    if new_rating is not None:
        label = new_rating
        text = row['Review']
        train_data.append({'label': label, 'text': text})

# Extract 'new_rating' and 'Review' columns for test data
test_data = []
for _, row in df_test.iterrows():
    rating = int(row['Rating'])
    new_rating = get_new_rating(rating)
    if new_rating is not None:
        label = new_rating
        text = row['Review']
        test_data.append({'label': label, 'text': text})

# Export training data as JSON
with open('train.json', 'w') as train_file:
    json.dump(train_data, train_file, indent=4)

# Export test data as JSON
with open('test.json', 'w') as test_file:
    json.dump(test_data, test_file, indent=4)

# Create README file
readme_text = f"Number of entries in train.json: {len(train_data)}\n" \
              f"Number of entries in test.json: {len(test_data)}\n\n" \
              "JSON Structure:\n" \
              "{\n" \
              "    \"label\": <int>,\n" \
              "    \"text\": <string>\n" \
              "}\n"

with open('README.txt', 'w') as readme_file:
    readme_file.write(readme_text)

print("JSON files and README file created successfully.")
