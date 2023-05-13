import subprocess
import os
from flask import Flask, jsonify, request
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Set up the OpenAI SDK with your API keys
openai.api_key = "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"
model = "text-davinci-002"

terraform_path = "C:\Terraform"
os.environ["PATH"] += os.pathsep + terraform_path

# Define the prompt for generating Terraform templates
prompt = (
    "Generate a Terraform template for {provider} to deploy a {type} infrastructure with {num_instances} instances, each with the following configuration:\n"
"Instance type: {instance_type}\n"
"Disk size: {disk_size} GB\n"
"Region: {region}\n"
"Security group: {security_group}\n"
"Subnet: {subnet}\n"
"VPC: {vpc}\n"
)

@app.route('/api/submit', methods=['POST'])
def submit():
    # Get the selected values from the request
    selected_values = request.json['values']

    # Replace the variables in the prompt with the selected values
    prompt_with_input = prompt.format(
        provider=selected_values[0],
        type=selected_values[1],
        num_instances=selected_values[2],
        instance_type=selected_values[3],
        disk_size=selected_values[4],
        region=selected_values[5],
        security_group=selected_values[6],
        subnet=selected_values[7],
        vpc=selected_values[8]
    )

    # Call the OpenAI API to generate the Terraform template
    response = openai.Completion.create(
        engine= model,
        prompt=prompt_with_input,
        temperature=0.5,
        max_tokens=2048,
        n=1,
        stop=None,
        timeout=60,
    )

    # Extract the generated Terraform template from the API response
    template = response.choices[0].text

    with open("template.tf", "w") as f:
        f.write(template)

    #subprocess.run(["terraform", "init"], stdout=open('output.txt', 'w'), stderr=subprocess.PIPE)
    #subprocess.run(["terraform", "apply", "-auto-approve"])

    # Return the Terraform template as a JSON response
    return jsonify(template=template)

if __name__ == '__main__':
    app.run()