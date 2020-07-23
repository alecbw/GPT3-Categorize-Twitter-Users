from gpt_utils import * # local import

import os
import sys
import random
import csv

import inquirer
import openai



def read_input_csv(filename, necessary_csv_headers):
    with open(filename) as f:
        file_as_list_of_dictionaries = [{k:v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)] # LOD

    if any(x for x in necessary_csv_headers if x not in file_as_list_of_dictionaries[0].keys()):
        sys.exit(f"Exiting. Your CSV needs to have these headers: {necessary_csv_headers}")
    return file_as_list_of_dictionaries

def write_output_csv(filename, output_lod):
    with open("Output " + filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, output_lod[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(output_lod)
    print("Write to csv was successful\n")

def prompt_user_response(response_type):
    question_bank = {
        "GPT": "Enter your secret GPT Key (to disable this, set it as an environment variable)",
        "filename": "What is the name of the file you want to read from?",
        "tags": "What categories does this fit in? Separate by commas",
        "temperature": "How creative do you want the tag results to be? Range is 0.0-1.0. 0.3 seems to work well",
        "training_samples": "How many samples do you want to manually categorize first? Range is 5-20",
    }

    questions = [inquirer.Text(response_type, message=question_bank[response_type])]

    answers = inquirer.prompt(questions)
    return answers[response_type.lower()]


if __name__ == "__main__":
    GPT_KEY = os.getenv("GPT_KEY") if os.getenv("GPT_KEY") else prompt_user_response('GPT')
    set_openai_key(GPT_KEY)

    filename = prompt_user_response('filename')
    filename = filename + ".csv" if ".csv" not in filename else filename

    necessary_csv_headers = ["name", "handle", "description"]
    users_lod = read_input_csv(filename, necessary_csv_headers)
    print(f"Length of input CSV is: {len(users_lod)}")

    temperature = prompt_user_response('temperature')
    training_samples = prompt_user_response('training_samples')

    gpt = GPT(engine="davinci",
          temperature=float(temperature),
          max_tokens=20)

    # We pick random rows to manually tag as examples
    random_row_numbers = random.sample(range(0, len(users_lod)), int(training_samples))
    for n in random_row_numbers:
        print(f"{users_lod[n]['name']} ({users_lod[n]['handle']}) - {users_lod[n]['description']}")
        tags = prompt_user_response("tags")
        gpt.add_example(Example(users_lod[n]['description'], tags))

    for n, row in enumerate(users_lod):
        gpt_result = gpt.submit_request(row['description'])
        gpt_tags = gpt_result.get("choices", [])[0].get("text").replace("output: ", "")
        users_lod[n]["GPT-Tags"] = gpt_tags
        print(row['description'] + " - " + gpt_tags)

        if n != 0 and n % 25 == 0:
            write_output_csv(filename, users_lod)

        write_output_csv(filename, users_lod)