import base64

with open('resume.pdf', 'rb') as file:
    resume_content = file.read()

encoded_resume = base64.b64encode(resume_content).decode('utf-8')

data = {
    'name': 'William Marcus',
    'email': 'john.doe@example.com',
    'file': encoded_resume
}

# Save the JSON object to a file
with open('resume_data.json', 'w') as json_file:
    json.dump(data, json_file)

print("File 'resume_data.json' saved successfully.")
