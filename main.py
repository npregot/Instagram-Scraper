#!/usr/bin/python

'''
Creator: Nahuel (Noel) Pregot
Email: npregot@gmail.com


'''
# https://gist.github.com/ziadoz/3e8ab7e944d02fe872c3454d17af31a5

# +------------------------> LIBRARIES <----------------------------+

# To display the process ID & restarting Python Script
import os
import psutil
import sys

# Get the followers accounts
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome options
from selenium.webdriver.chrome.options import Options

# Exception if the account is private
from selenium.common.exceptions import NoSuchElementException

# Exception if Chrome is not reachable
from selenium.common.exceptions import WebDriverException

# In case it takes too long to load the follower
from selenium.common.exceptions import TimeoutException

# Check the current OS
from sys import platform

# Retrieve the BIO & find email
from bs4 import BeautifulSoup 
import requests 
import re 

# Reading CSV files
import csv

# Regex to find email addresses
import re 

# Sending notification Email
import smtplib

# To create the name of the file containing the 10'000 emails
import datetime

# To randomly change the browser
import random

# To run the scraper with an argument or not
import argparse

# To log into the database
import mysql.connector

# +------------------------> LIBRARIES <----------------------------+


# FUNCTIONS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# READING BIO <-------------------------

# username   = Account of the follower the bio is read from
# dictionary = Temporary storage for emails
# mother     = The account the scraper is scraping followers from
# counter    = To display the # of emails that were found

def bio_reader(username, dictionary, mother, counter):

	op = False
	if True:
		browsers = ['Internet Explorer/5.0', 'Safari/11.1.2', 'Firefox/5.0', 'Opera/53', 'OPR/25.0.1614.18']
		secure_random = random.SystemRandom()
		selection = secure_random.choice(browsers)
		op = True

	try:

		if op == True:
			# Opening a new window
			opts = Options()
			opts.add_argument(selection)
			opts.set_headless(headless=False) 
			bio_driver = webdriver.Chrome('your/location/of/chromedriver', chrome_options=opts)
											

		else:
			bio_driver = webdriver.Chrome('your/location/of/chromedriver1')

	# If Chrome is not reachable - Try with another webdriver
	except WebDriverException:

		try:

			if True:
				print('', end='\n')
				print('chromedriver1 was NOT reachable')
				print('', end='\r')
				opts = Options()
				opts.add_argument(selection)
				opts.set_headless(headless=False) 
				bio_driver = webdriver.Chrome('your/location/of/chromedriver_extra', chrome_options=opts)

			else:
				bio_driver = webdriver.Chrome('your/location/of/chromedriver_extra') # CHANGE IT TO YOUR LOCATION

		except WebDriverException:

			if op == True:
				print('', end='\n')
				print('chromedriver_extra was NOT reachable')
				print('', end='\r')
				opts = Options()
				opts.add_argument(selection)
				opts.set_headless(headless=False) 
				bio_driver = webdriver.Chrome('your/location/of/chromedriver1', chrome_options=opts)

			else:
				bio_driver = webdriver.Chrome('your/location/of/chromedriver1')


	opts.set_headless(headless=False) 

	# Process ID of browser window
	# px = psutil.Process(bio_driver.service.process.pid)

	# The Follower's Instagram home page
	url_demo = 'https://www.instagram.com/{}/?hl=en'.format(username)


	try:
		r = requests.get(url_demo)

			# If the page is NOT FOUND
		if r.status_code == 404:
			pass

		else:

			try:
				bio_driver.set_page_load_timeout(60)
				bio_driver.get(url_demo)

				# Locating the bio with its xpath
				bio = bio_driver.find_element_by_xpath("//section/main/div/header/section/div[2]/span").text

				# Searching for an email & saving it to a dictionary
				email_finder = re.findall(r'[a-zA-Z0-9_.+-]+@(?:(?:[a-zA-Z0-9-]+\.)?[a-zA-Z]+\.)?[\w\.-]+\.[\w\.-]+', bio)
				if len(email_finder) > 0:
						# Store the data into a dictionary
						dictionary[username] = email_finder
						print('', end='\n')
						print('\tNew Email Found - Tot: {} emails'.format(len(dictionary)))
						print('', end='\r')

						# Adding UTC time in db format
						form = '%Y-%m-%d %H:%M:%S (UTC)'
						now = datetime.datetime.utcnow().strftime(form)

						# Saving data to database
						try:
							 
							# # LOGGING INTO DB <--------


							# please consider storing this information into a file and read it
							db_hostname = 'your_host_name.amazonaws.com'
							Username = 'username'
							database = 'db_name'
							password = 'your_db_password'

							mydb = mysql.connector.connect(
							  host = db_hostname,
							  user = Username,
							  passwd = password,
							  database = database
							)

							# # --------> LOGGING INTO DB

							mycursor = mydb.cursor()
							sql = "INSERT INTO accounts (Email, User_Name, Source, Scrape_time) VALUES (%s, %s, %s, %s)"
							val = (', '.join(str(x) for x in email_finder), username, mother, now)
							mycursor.execute(sql, val)
							mydb.commit()
							print("\tRow addded to database")

						except Exception as g: # If it fails, save it to a csv file

							print('Database connection failed - Using csv file instead')
							print(x)

							with open('mylocal_db.csv','a') as fd:
								fd.write('{},{},{},{}\n'.format(username, email_finder, now, mother))

			except NoSuchElementException:
				pass # The profile without bio

			except TimeoutException:
				pass # If it does NOT load move on

	except Exception as q:
		# requests.exceptions.RequestException.ProtocolError:
		print('', end='\n')
		print('\tFound -> {} <-'.format(q))
		print('', end='\r')
		pass  # To avoid "requests.exceptions.ChunkedEncodingError"



	# Closing the window
	bio_driver.close()
	bio_driver.quit()

# -------------------------> READING BIO


# FOLLOWERS <------------------------

def followers(username, dictionary):

	errors = 0

	# The driver goes to the homepage of the account being scraped
	url_demo = 'https://www.instagram.com/{}/?hl=en'.format(username)
	
	try:
		driver.get(url_demo)

		# Click the "Followers" link
		driver.find_element_by_partial_link_text('followers').click()

		try:
			# Wait for the Followers box to be loaded
			xpath ="/html/body/div[3]/div/div"
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

		except TimeoutException:
			errors+=1
			print('Follower Box NOT found - TimeoutException Exception')
			print('Check whether the xpath has changed\n')

		

		# Scrolling Down <-------------------- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

		driver.execute_script("followersbox = document.getElementsByClassName('isgrP')[0];") # >>>>>>>>>>>>>> UPDATE THIS: "isgrP"
		last_height = driver.execute_script("return followersbox.scrollHeight;")

		# --------------------> Scrolling Down


		# Getting The First 12 Followers <--------------------

		print('\tScraping the first 12 Followers')

		xpath = "/html/body/div[3]/div/div[2]/div/div[2]/ul/div/li" # this xpath might change from time to time
		followers_elems = driver.find_elements_by_xpath(xpath)

		followers_temp = [e.text for e in followers_elems]
		follower_accounts = []

		for i in followers_temp:
		    usr_name, sep, name = i.partition('\n')
		    follower_accounts.append(usr_name)
		    print(usr_name)

		for i in follower_accounts:
			bio_reader(i, dictionary, username)

		# --------------------> Getting The First 12 Followers

		time.sleep(3)

		# Getting The Other Followers <--------------------
		counter = 13
		while True:

			# Changing the User Agent
			if counter % 50 == 0:
				user_agent = ['Internet Explorer/5.0', 'Safari/11.1.2', 'Firefox/5.0', 'Opera/53', 'OPR/25.0.1614.18']
				secure_random = random.SystemRandom()
				selection = secure_random.choice(user_agent)
				options.add_argument(selection)


			# Changing the window size
			if counter % 24 == 0:
				width = [1024, 1000, 1100, 200]
				eight = [768, 400, 304, 50]
				secure_random = random.SystemRandom()
				selection_width = secure_random.choice(width)
				selection_eight = secure_random.choice(eight)
				driver.set_window_size(selection_width, selection_eight)	

			try:
				
				driver.execute_script("followersbox.scrollTo(0, followersbox.scrollHeight);")

				# Wait a number of seconds for the page to load & avoid ERROR 429 from server
				time.sleep(3.5) 

				new_height = driver.execute_script("return followersbox.scrollHeight;")


				xpath = '/html/body/div[3]/div/div/div[2]/ul/div/li[{}]'.format(counter)

				# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
				loaded_follower = driver.find_elements_by_xpath(xpath)

				# If the list is empty we restart the scraper with a different account
				if not loaded_follower:
					print('Restarting Program - Empty List Found')
					driver.close()
					driver.quit()
					python = sys.executable
					os.execl(python, python, * sys.argv)



				# SCRAPING COMPLETED
				if counter >= 170000:

					now = datetime.datetime.now()

					with open('{}.csv'.format(now.strftime('last_emails_from_{}'.format(username))), 'w') as csvfile:
						filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

						for key in dictionary.keys():
							csvfile.write('{},{}\n'.format(key, dictionary[key]))
							print('\tFinal Counter: {}'.format(counter))
					break



				flw_temp = [e.text for e in loaded_follower]
				flw_accounts = []

				# extracting the username 
				for i in flw_temp:
				    usr_name, sep, name = i.partition('\n')
				    flw_accounts.append(usr_name)
				    # print(usr_name)

				# DYNAMIC MESSAGE
				print("\033[K", end='\r') # Clears the line (for dynamic printing)
				print('Profiles Scanned: {} | Username: {}'.format(counter, flw_accounts), end='\r')
				

				# reading the bio for each follower
				for i in flw_accounts:
					# print(i)
					bio_reader(i, dictionary, username, counter)


				last_height = new_height
				counter+=1
				


			except NoSuchElementException:
				errors+=1
				pass # the account is private

		# --------------------> Getting The Other Followers 

	except NoSuchElementException:
		errors+=1
		pass # the account is private

# ------------------------> FOLLOWERS



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNCTIONS


Format = '%Y-%m-%d %H:%M:%S UTC'
UTCtime = datetime.datetime.utcnow().strftime(Format)
print('\n\t{}'.format(UTCtime))
# Displays the process id of the execution
pid = os.getpid()
print('\tProcess ID: {}'.format(pid))


# STARTING SELENIUM <--------


if platform == "darwin" or platform == "linux" or platform == "linux2":  # mac

	user_agent = ['Internet Explorer/5.0', 'Safari/11.1.2', 'Firefox/5.0', 'Opera/53', 'OPR/25.0.1614.18']
	secure_random = random.SystemRandom()
	selection = secure_random.choice(user_agent)
	
	options = Options()
	options.set_headless(headless=False) 

	# Using a different User Agent every time
	options.add_argument("user-agent={}".format(selection))
	print('\tUser Agent: {}'.format(selection))

	# Using Firefox
	# driver = webdriver.Firefox(firefox_options = options, executable_path = '/usr/local/bin/geckodriver')

	# Using Chrome , desired_capabilities=capabilities
	driver = webdriver.Chrome("/Users/nahuelpregot/Desktop/coding_files/swish/chromedriver", chrome_options=options) # /Users/nahuelpregot/Desktop/swish/

	# Process ID of browser window
	p = psutil.Process(driver.service.process.pid)
	print('\tProcess ID Main Browser Window: {}'.format(p.pid))



elif platform == 'win32':  # windows
	# post_driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=options)
	xprint(' Windows Operating System not supported yet')

# --------> STARTING SELENIUM



# LOGGING IN <------------------------

# Loading login page

log_in_url = "https://www.instagram.com/accounts/login/"
driver.get(log_in_url)

# Sometimes the log in url is being redirected somewhere else
while True:
	time.sleep(1)
	c = driver.current_url
	if c == log_in_url:
		break
	else:
		driver.get(log_in_url)



# Choosing a random Instagram to log with:
with open('login_accounts.csv','r') as longishfile:
    reader = csv.reader(longishfile)
    rows = [r for r in reader]


random_index = random.randint(0,4)

username = rows[random_index][2] # put your username here
print('\tLogging in with -> ', username)
psw = rows[random_index][1] # put your password here

# Wait until the username & password field are loaded 
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@name="username"]')))
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@name="password"]')))

driver.find_element_by_xpath('//*[@name="username"]').send_keys(username)
driver.find_element_by_xpath('//*[@name="password"]').send_keys(psw)
# driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button').click() # <<<<<<<<< ERROR HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div').click()


# If the two pop up windows appear
try:
	# Closing 1st popup window
	button1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button[2]")))
	button1.click()

except TimeoutException:
	pass

try:
	# Closing 2nd popup window
	button2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/button")))
	button2.click()

except TimeoutException:
	pass

print('\n\t+--------------------------------+')
print('\t|  Login Completed Successfully  |')
print('\t+--------------------------------+\n')

# ------------------------> LOGGING IN 


# SCRAPING LIST OF ACCOUNTS <------------------------

try:
	username = ''
	email_dict = {} # Where the found emails will be temporary stored


	parser = argparse.ArgumentParser()

	parser.add_argument("-a", help="Given an username of an Instagram account, it scrapes the followers of such profile")
	args = parser.parse_args()

	if args.a == None:
		username = 'lotstar' # by default the script scrapes lotstar's account
		
	else:
		username = args.a
		
		while True:
			url_demo = 'https://www.instagram.com/{}/?hl=en'.format(username)
			r = requests.get(url_demo)

			if r.status_code == 404:
				print('{} profile page NOT found'.format(username))
				selection = input('\nType new account to scrape or type "d" or "default" to scrape the default account: ')
				username = selection

				if selection.lower() == 'd' or selection.lower() == 'default':
					username = 'lotstar'
					
			else:
				break

	print('\n\tScraping {}\n'.format(username))
	followers(username, email_dict)


except Exception as e:
	print('Restarting Scraper due to: {}'.format(e))
	driver.close()
	driver.quit()
	python = sys.executable
	os.execl(python, python, * sys.argv)

# ------------------------> SCRAPING LIST OF ACCOUNTS


# TERMINATING SCRIPT & Closing the Window
# driver.close()
# driver.quit()


