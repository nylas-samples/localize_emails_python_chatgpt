# Import your dependencies
from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_session.__init__ import Session
import os
import openai
import csv
import re
from nylas import Client

# Load your env variables
from dotenv import load_dotenv
load_dotenv()

# Create the app
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize your Nylas API client
nylas = Client(
    api_key = os.environ.get("V3_API_KEY")
)

def get_completion(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "user", "content": f"{prompt}"}
        ]        
    )
    return response.choices[0].message.content

def get_prompt(language, to_replace):
    prompt = """
    Translate the following message into language
    text_here
    """
    
    prompt = re.sub("language", language, prompt)
    prompt = re.sub("text_here", to_replace, prompt)
    return prompt

# Initialize your Open API client
openai.api_key = os.environ.get("OPEN_AI")

# This the landing page
@app.route("/", methods=['GET','POST'])
def index():
# We're using a GET, displat landing page
    if request.method == 'GET':
        return render_template('main.html')
# Get parameters from form
    else:
        subject = request.form["subject"]
        body = request.form["body"]
        mergefile = request.form["mergefile"]
# Session variables		
        session["subject"] = subject
        session["body"] = body
# Make sure all fields are filled		
        if not subject or not body or not mergefile:
            flash('You must specify all fields')
            return redirect(url_for('index'))
        else:
            session["subject"] = None
            session["body"] = None	
# Auxiliary variables
            email = ""
            emails = []
            row_header = {}
            i = 0
            subject_replaced = subject
            body_replaced = body
# Open the CSV file			
            file = open(mergefile)
# Read the CSV contents			
            mergemail_file = csv.reader(file)
# Read and save the headers			
            headers = []
            headers = next(mergemail_file)
            for header in headers:
                row_header[header] = i
                i += 1
# Read all rows of the CSV file				
            for row in mergemail_file:
# Assign parameters to auxiliary variables				
                subject_replaced = subject
                body_replaced = body
# Read all headers 
                for header in headers:
# Search for header and replace them with
# the content on the CSV file
                    if re.search("{"+f"{header}"+"}", subject):
                        subject_replaced = re.sub("{"+f"{header}"+"}", row[row_header[f"{header}"]], subject_replaced)
                    if re.search("{"+f"{header}"+"}", body):
                        body_replaced = re.sub("{"+f"{header}"+"}", row[row_header[f"{header}"]], body_replaced)					
#Try to get the Name and Last_Name
                    try:
                        full_name = row[row_header["Name"]] + row[row_header["Last_Name"]]
                    except Exception as e:
                        full_name = row[row_header["Name"]]
                        print(f'{e}')
# Translate only email where target language is not English
                if row[row_header["Language"]] != "English":
# Prompt for ChatGPT to add the body response
                    prompt = get_prompt(row[row_header["Language"]], body_replaced) 
# Call ChatGPT
                    response = get_completion(prompt)
# Add response to the body of the email
                    body_replaced = body_replaced + "\n\n---" + f'{row[row_header["Language"]]}' + " translation follows---\n\n" + response
# Replace carriage returns with break lines
                    body_replaced = re.sub('\n', '<br>', body_replaced)
# Prompt for ChatGPT to add the subject response
                    prompt = get_prompt(row[row_header["Language"]], subject_replaced)
# Call ChatGPT
                    response = get_completion(prompt)
                    subject_replaced = subject_replaced + ' / ' + response
                else:
                    body_replaced = re.sub('\n', '<br>', body_replaced)
# Try to send an email
                try:
                    email_body = {"subject" : subject_replaced, 
                                           "body": body_replaced,
                                           "to":[{"name": full_name,
                                           "email": row[row_header["Email"]]}]}
                               
                    nylas.messages.send(os.environ.get("GRANT_ID"), request_body = email_body)
# It was successful, added to the emails array					
                    email = row[row_header["Email"]]
                    emails.append(email)
                except Exception as e:
# There's a problem					
                    print(f'{e}')
# Call the results page					
    return redirect(url_for('results', emails = emails))	
				
# Show recipients emails
@app.route("/results", methods=['GET'])
def results():
# Get the list of emails	
    emails = request.args.getlist('emails')
# Call the results page passing emails as parameters	
    return render_template('results.html', emails = emails)
				
# Run our application  
if __name__ == "__main__":
    app.run()
