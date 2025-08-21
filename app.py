from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

# mongo url set up
MONGO_URI = os.environ.get('MONGO_URI', "mongodb+srv://idowubabatee:<db_password>@my-cluster.bzotqpo.mongodb.net/healthcare_survey")
client = MongoClient(MONGO_URI)
db = client.healthcare_survey 
participants = db.participants 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Collect basic info
        user_data = {
            'age': int(request.form['age']),
            'gender': request.form['gender'],
            'total_income': float(request.form['total_income']),
            'expenses': {}
        }

        # Collect expense data dynamically.
        expense_categories = ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']
        for category in expense_categories:
            # Check if the category checkbox was ticked
            if category in request.form:
                amount = request.form.get(f'{category}_amount', '0').strip()
                # Store the amount if it's a valid number, otherwise store 0
                user_data['expenses'][category] = float(amount) if amount else 0.0

        # Insert the data into the MongoDB collection
        participants.insert_one(user_data)

        return render_template('success.html')

    except Exception as e:
        print(f"An error has occurred: {e}")
        # To redirect to an error page or back to the form
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5555)
