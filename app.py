from flask import Flask, render_template, request, jsonify, redirect, url_for
from db import init_db, insert_user_info, get_user_info
from apscheduler.schedulers.background import BackgroundScheduler
from assistant import process_chat

app = Flask(__name__)

# Initialize database if it doesn't exist
init_db()   

# Function to remind water intake
def remind_water_intake():
    user_info = get_user_info()
    if user_info:
        water_intake = user_info[0][3]
        message = f"Hãy nhớ uống đủ {water_intake}ml nước trong ngày nhé!"
        # Send reminder message
        chat(message)  # Replace print with send_message

# Initialize scheduler to send reminders every 2 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(remind_water_intake, 'interval', minutes=2)
scheduler.start()

@app.route("/")
def home():
    return render_template("index.html")  # No popup needed

@app.route("/submit_info", methods=["POST"])
def submit_info():
    # This route is no longer needed for user info input
    return redirect(url_for('home'))

@app.route("/chat", methods=["POST"])
def chat(message=None):
    if message:
        return jsonify({'message': message})
    else:
        user_message = request.form['message']
        # Process user message through process_chat from assistant.py
        response_message = process_chat(user_message)
    return jsonify({'message': response_message})

if __name__ == "__main__":
    app.run(debug=True)


