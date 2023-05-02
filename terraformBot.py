from flask import Flask, jsonify, request
import openai
from flask_cors import CORS

# Set up the OpenAI SDK with your API keys
openai.api_key = "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"

# Define the prompt for generating Terraform templates
prompt = (
    "Generate a Terraform template to deploy a {type} infrastructure with {num_instances} instances, each with the following configuration:\n"
    "Instance type: {instance_type}\n"
    "Disk size: {disk_size} GB\n"
    "Region: {region}\n"
    "Security group: {security_group}\n"
    "Subnet: {subnet}\n"
    "VPC: {vpc}\n"
)


# Define a function to generate Terraform templates based on user input
def generate_terraform_template():
    # Get user input for the requirements
    infrastructure_type = input("Enter the type of infrastructure to deploy (e.g. web server, database server): ")
    num_instances = int(input("Enter the number of instances to deploy: "))
    instance_type = input("Enter the instance type (e.g. t2.micro): ")
    disk_size = int(input("Enter the disk size in GB: "))
    region = input("Enter the region to deploy to (e.g. us-west-1): ")
    security_group = input("Enter the security group ID: ")
    subnet = input("Enter the subnet ID: ")
    vpc = input("Enter the VPC ID: ")

    # Replace the variables in the prompt with the user input
    prompt_with_input = prompt.format(
        type=infrastructure_type,
        num_instances=num_instances,
        instance_type=instance_type,
        disk_size=disk_size,
        region=region,
        security_group=security_group,
        subnet=subnet,
        vpc=vpc
    )

    # Call the OpenAI API to generate the Terraform template
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_with_input,
        temperature=0.7,
        max_tokens=2048,
        n=1,
        stop=None,
        timeout=60,
    )

    # Extract the generated Terraform template from the API response
    template = response.choices[0].text

    # Print the generated template
    print("\nGenerated Terraform template:\n")
    print(template)


# Call the function to generate a Terraform template
generate_terraform_template()
