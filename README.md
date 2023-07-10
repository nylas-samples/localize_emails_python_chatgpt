# localize_emails_python_chatgpt

This sample will show you to localize your emails using ChatGPT and mail merge templates.

You can follow along step-by-step in our blog post ["Localize Your Emails With ChatGPT and Python"](https://www.nylas.com/blog/localize-your-emails-with-chatgpt-and-python/).

## Setup

### System dependencies

- Python v3.x

### Gather environment variables

You'll need the following values:

```text
CLIENT_ID = ""
CLIENT_SECRET = ""
ACCESS_TOKEN = ""
```

Add the above values to a new `.env` file:

```bash
$ touch .env # Then add your env variables
```

### Install dependencies

```bash
$ pip3 install openai # OpenAI package
$ pip3 install python-dotenv # Environment variables
$ pip3 install Flask # Micro framework
$ pip3 install Flask-session # Sessions for Flask
```

Create a .csv file similar to this one:

<img width="728" alt="image" src="https://github.com/nylas-samples/localize_emails_python_chatgpt/assets/1071110/1bd1238e-feac-4aff-a557-ed0d02b63009">

## Usage

Run the file **localized_emails.py**:

```bash
$ python3 localized_emails.py.py
```

NiceGUI will open up your browser on port 5000.

## Learn more

Visit our [Nylas Python SDK documentation](https://developer.nylas.com/docs/developer-tools/sdk/python-sdk/) to learn more.
