#!/usr/local/bin/python
import sys, getopt
import requests
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

# Open the google sheet
# Get the credentials
json_key = json.load(open(''))
scope = ['https://spreadsheets.google.com/feeds']

# Authorize
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)


# Open the workbook and get the first sheet
wks = gc.open('Rapid Response Test').sheet1

# Get the phone numbers column
phone_nums = wks.col_values(4)

# Get the text permissions
text_perms = wks.col_values(5)

# Remove header for phone number column
phone_nums.pop(0)

# EDIT THE MESSAGE HERE
# Create the message
message = "THIS IS A TEST. I am working on the program and this text is a test."

# TextBelt url
url = "http://textbelt.com/text"

def main(argv):
	try: 
		opts, args = getopt.getopt(argv, "tm:", ["message"])
	except getopt.GetoptError:
		print("To run test:\npython rapid_response.py -tm \"<message>\"")
		print("To run actual rapid response:\npython rapid_response.py -m \"<message>\"")
	# Go through phone numbers
	for number in phone_nums:
		num_cell = wks.find(number)
		row = num_cell.row
		next_col = num_cell.col + 1
		if wks.cell(row, next_col).value != 'Yes':
			print(number + ' does not wish to recieve texts.')
		else:
			contact = {'number': number, 'message': message}
			r = requests.post(url, data=contact)
			print(number +':\n'+r.text+'\n')
