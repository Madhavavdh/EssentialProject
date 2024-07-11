from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint as pp
import os

app = Flask(__name__)

#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
#creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
#client = gspread.authorize(creds)


# Function to access public Google Sheets
def get_public_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    #client = gspread.service_account()
    sheet = client.open(sheet_name).sheet1  # Change this to the specific sheet & worksheet you want to access
    return sheet


# Hardcoded username and password values for authentication
correct_username = "user123"
correct_password = "pass123"
correct_username2 = "user456"
correct_password2 = "pass456"


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/second-page', methods=['POST'])
def second_page():
    # Check if the entered username and password match the hardcoded values
    entered_username = request.form['username']
    entered_password = request.form['password']

    if entered_username == correct_username and entered_password == correct_password:
        return render_template('second_page.html')
    elif entered_username == correct_username2 and entered_password == correct_password2:
        return render_template('second_page.html')
    else:
        return "Invalid username or password. Please try again."


@app.route('/back-to-home')
def back_to_home():
    return render_template('second_page.html')


# Define routes for the three buttons
@app.route('/influencer-details')
def influencer_details_page():
    return render_template('influencer_details.html')


@app.route('/essential-oil-details')
def essential_oil_details_page():
    return render_template('essential_oil_details.html')


@app.route('/courier-details')
def courier_details_page():
    return render_template('courier_details.html')


@app.route('/influencer-details', methods=['GET', 'POST'])
def influencer_details():
    if request.method == 'POST':
        # Save influencer details to the database
        influencer_name = request.form['influencer_name']
        influencer_gender = request.form['influencer_gender']
        average_views_per_reel = request.form['average_views_per_reel']
        email_address = request.form['email_address']
        social_media_account_url = request.form['social_media_account_url']
        location = request.form['location']
        follower_count = request.form['follower_count']
        average_likes_per_post = request.form['average_likes_per_post']
        content_categories = request.form['content_categories']
        phone_number = request.form['phone_number']

        # Save data to Google Sheets
        sheet = get_public_google_sheet('Influencer Details')
        next_row = len(sheet.get_all_values())+1
        sheet.insert_row([influencer_name, influencer_gender, average_views_per_reel, email_address, social_media_account_url, location, follower_count, average_likes_per_post, content_categories, phone_number],next_row)
        #sheet.append_row([influencer_name, influencer_gender, average_views_per_reel, email_address, social_media_account_url, location, follower_count, average_likes_per_post, content_categories, phone_number])  # Add more values as needed

        # Simulate saving to a list (replace with saving to a database)
        entries = [{'influencer_name': influencer_name}, {'influencer_gender': influencer_gender}, {'average_views_per_reel': average_views_per_reel}, {'email_address': email_address}, {'social_media_account_url': social_media_account_url}, {'location': location}, {'follower_count': follower_count}, {'average_likes_per_post': average_likes_per_post}, {'content_categories': content_categories}, {'phone_number': phone_number}]
        return render_template('influencer_details.html', entries=entries)

    return render_template('influencer_details.html', entries=[])


@app.route('/essential-oil-details', methods=['GET', 'POST'])
def essential_oil_details():
    if request.method == 'POST':
        # Save essential oil details to the database
        brand_name = request.form['brand_name']
        product_name = request.form['product_name']
        size_or_volume = request.form['size/volume']
        product_price = request.form['product_price']

        # Save data to Google Sheets
        sheet = get_public_google_sheet('Essential Oil Details')
        next_row = len(sheet.get_all_values()) + 1
        sheet.insert_row([brand_name, product_name, size_or_volume, product_price], next_row)

        # Simulate saving to a list (replace with saving to a database)
        entries = [{'brand_name': brand_name}, {'product_name': product_name}, {'size_or_volume': size_or_volume}, {'product_price': product_price}]
        return render_template('essential_oil_details.html', entries=entries)

    return render_template('essential_oil_details.html', entries=[])


@app.route('/courier-details', methods=['GET', 'POST'])
def courier_details():
    if request.method == 'POST':
        # Save courier price details to the database
        courier_partner_name = request.form['courier_partner_name']
        service_type = request.form['service_type']
        average_delivery_time = request.form['average_delivery_time']
        weight_limits_per_courier = request.form['weight_limits_per_courier']
        avg_courier_price = request.form['avg_courier_price']

        # Save data to Google Sheets
        sheet = get_public_google_sheet('Courier Details')
        next_row = len(sheet.get_all_values()) + 1
        sheet.insert_row([courier_partner_name, service_type, average_delivery_time, weight_limits_per_courier, avg_courier_price], next_row)

        # Simulate saving to a list (replace with saving to a database)
        entries = [{'courier_partner_name': courier_partner_name}, {'service_type': service_type}, {'average_delivery_time': average_delivery_time}, {'weight_limits_per_courier': weight_limits_per_courier}, {'avg_courier_price': avg_courier_price}]
        return render_template('courier_details.html', entries=entries)

    return render_template('courier_details.html', entries=[])


if __name__ == '__main__':
    app.run(debug=True)
