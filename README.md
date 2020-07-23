# GPT3-Categorize-Twitter-Users
A wrapper with interactive CLI that provides light prompt programming to enable categorizing Twitter users by description content



### Setup

Install pip (if necessary)
```py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py
```
Install the OpenAI library and a CLI helper library
```py
pip install openai inquirer
```

### Usage

You'll need a list of Twitter users exported to CSV with the following headers:
* name
* handle
* description

Start the execution with
```py
python3 gpt_categorize_twitter_users.py.py
```
The rest is done by interactive CLI. 
```text
[?] What is the name of the file you want to read from?: example.csv
[?] What temperature do you want to set for the queries? Range is 0.0-1.0: 0.3
[?] How many samples do you want to manually categorize first? Range is 5-20: 8
[it will then iterate through the number of samples you specify, printing the description and prompting you to label:]
Alec Barrett-Wilsdon (@contextify1) - Opinions about ads, microservices, startups, and oxford commas.\nFormer growth software @curologyusa, SaaS VC @acceleprise, @ucberkeley\nlearnings 👉🏻 https://alec.fyi
[?] What categories does this fit in? Separate by commas: ads, ecom, SaaS, VC, tech, etc, etc
[then it will iterate through the full file, saving output to CSV every 25 rows]
```
