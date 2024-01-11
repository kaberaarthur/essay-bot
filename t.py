import requests
import random
import hashlib
import string
import json
from datetime import datetime

def log_activity(activity):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: {activity}\n"
    
    with open("activity_log.txt", "a") as log_file:
        log_file.write(log_entry)

def generate_random_number():
    return random.randint(1, 10)

def read_json_by_key(key):
    # Assuming messages.json is in the same directory as this script
    file_path = 'messages.json'

    # Read JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Check if the key exists in the data
    if key in data:
        return data[key]
    else:
        return f"Key '{key}' not found in JSON data."

def generate_hash_id():
    # Generate a random string with specific character compositions
    random_string = ''.join(random.choices(string.digits, k=min(4, random.randint(0, 4))))  # Maximum of 4 numbers
    random_string += ''.join(random.choices(string.ascii_uppercase, k=min(6, random.randint(0, 6))))  # Maximum of 6 capital letters
    random_string += ''.join(random.choices(string.ascii_lowercase, k=min(2, random.randint(0, 2))))  # Maximum of 2 small letters

    # Shuffle the characters in the string
    random_list = list(random_string)
    random.shuffle(random_list)
    random_string = ''.join(random_list)

    # Hash the random string using SHA-256
    hashed = hashlib.sha256(random_string.encode()).hexdigest()

    # Take the first 12 characters of the hashed value
    hash_id = hashed[:12]

    return hash_id

def generate_numbers(input_string):
    # Split the input string into two numbers
    numbers = input_string.split('-')
    num1 = int(numbers[0])
    num2 = int(numbers[1])

    larger_number = max(num1, num2)
    lower_limit = int(larger_number * 0.9)  # 90% of the larger number

    # Generate a list of ten integers close to the larger number
    generated_numbers = []
    for _ in range(10):
        generated = random.randint(lower_limit, larger_number)
        generated_numbers.append(generated)

    return generated_numbers


# URL of the PHP script
url = 'https://essays-writing-service.org/bot/latest.php'  # Replace with your actual URL

def check_item_in_file(file_name, search_item):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]  # Remove newline characters
            
            if search_item in lines:
                return True  # Item found in the list
            else:
                return False  # Item not found in the list
    
    except FileNotFoundError:
        return False  # File doesn't exist
    
def append_line_to_file(file_name, line):
    try:
        with open(file_name, 'a') as file:
            file.write('\n' + line)
        print(f"Line '{line}' appended to '{file_name}'.")
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")


########################################
###         While Loop Here          ###
########################################        
file_path = 'users.txt'  # Replace with your file path

# Read lines from the text file into a list and remove spaces and newlines
with open(file_path, 'r') as file:
    users_list = [line.strip().replace(" ", "") for line in file.readlines()]

# Users List => users_list

# Making a POST request to the PHP script
response = requests.post(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the JSON response from the PHP script
    print(response.json()['id'])
    order_id = response.json()['id']

    # Check if this is in the history.txt
    print(check_item_in_file("history.txt", response.json()['id']))

    if(check_item_in_file("history.txt", response.json()['id'])):
        print("Bids Already Placed")
    else:
        print("Place Bids")
        print("New Bids: " + str(generate_numbers(response.json()['budget'])))

        bid_amounts = generate_numbers(response.json()['budget'])

        # Generate the Bids
        # Add the No. of Bids into the Orders Table Row
        def generate_random_string(length=8):
            return ''.join(random.choices(string.ascii_lowercase, k=length))

        def generate_user_document(user_id):
            json_object = {
                "hash_id": generate_hash_id(), # Correct
                "user_id": user_id, # Correct
                "user_role": "4", # Correct
                "question_id": response.json()['id'], # Correct
                "price": bid_amounts[generate_random_number() - 1], # Correct
                "text": read_json_by_key(str(generate_random_number())), # Correct
                "status": "0", # Correct
                "buyer_id": generate_random_number()
            }
            return json_object

        # List of user_ids
        user_ids = users_list

        # Generate documents for each user_id
        documents = []
        for user_id in user_ids:
            user_document = generate_user_document(user_id)
            documents.append(user_document)

        # Convert the list of documents to a JSON string
        json_data = json.dumps(documents, indent=2)

        # Write the JSON data to a file
        with open("out.json", 'w') as file:
            file.write(json_data)

        #### Write Bids Data to DB ####
        with open("out.json", 'r') as file:
            bids_data = json.load(file)

        # URL for the PHP endpoint
        url = 'https://essays-writing-service.org/bot/postbids.php'  # Replace with your actual URL

        # Send POST request with JSON data
        response = requests.post(url, json=bids_data)


        # Record Updated Bids on Order
        # URL of the PHP script
        update_bids_url = 'https://essays-writing-service.org/bot/update_bids_no.php'  # Replace with your actual URL

        # POST data with 'id' and 'new_bids' values
        update_bids_data = {
            'id': order_id,  # Replace with the specific ID you want to update
            'new_bids': len(users_list)  # Replace with the value to be added to 'bids'
        }

        # Send a POST request with data
        bids_response = requests.post(update_bids_url, data=update_bids_data)

        # Print the response from the server
        print(bids_response.text)



        # After Placing Bids, Record file to History
        append_line_to_file("history.txt", order_id)

        
else:
    # Print the error message if request failed
    print("Error:", response.text)


#### Activity Log ####
log_activity("Completed Run")