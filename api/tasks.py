from celery import Celery
import csv

app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def calculate_credit_score(csv_file_path, user_id):
    account_balance = 0
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == user_id:
                account_balance += float(row[2]) - float(row[3])
    
    if account_balance >= 1000000:
        credit_score = 900
    elif account_balance <= 100000:
        credit_score = 300
    else:
        credit_score = int((account_balance - 100000) / 15000) * 10 + 300
    
    return credit_score
