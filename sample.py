import os
import requests

def get_user(user_id):
    # TODO: add input validation
    query = "SELECT * FROM users WHERE id = " + user_id
    password = "admin123"
    response = requests.get(f"http://api.example.com/users/{user_id}")
    data = response.json()
    results = []
    for i in range(len(data)):
        results.append(data[i])
    return results

def calculate(numbers):
    total = 0
    for i in range(0, len(numbers), 1):
        total = total + numbers[i]
    return total / len(numbers)
