import openai

# Set OpenAI API key
openai.api_key = "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"

# Define the BUILD/RELEASE scenario prompt
prompt = """Generate a Jenkins pipeline script with groovy code written for each step for the following BUILD/RELEASE scenario:
- A developer pushes code to the main branch of a GitHub repository https://github.com/gauravjakhar/TerraformBot.
- Jenkins should automatically run tests and build the application.
- If the tests pass, Jenkins should deploy the application to a test environment which is based on Kubernetes Helm charts.
- If the deployment to the test environment is successful, Jenkins should deploy the application to a production environment."""

# Define the Jenkinsfile name
jenkinsfile_name = "Jenkinsfile"

# Define the Jenkinsfile location
jenkinsfile_path = f"./{jenkinsfile_name}"

# Generate text using the ChatGPT API
def generate_jenkinsfile():
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text

# Write the generated Jenkinsfile to a file
def write_jenkinsfile(jenkinsfile_text):
    with open(jenkinsfile_path, "w") as f:
        f.write("Jenkinsfile:\n```groovy\n")
        f.write(jenkinsfile_text)
        f.write("\n```\n")

# Run the bot
def run_bot():
    jenkinsfile_text = generate_jenkinsfile()
    write_jenkinsfile(jenkinsfile_text)
    print(f"Jenkinsfile created at {jenkinsfile_path}")

if __name__ == "__main__":
    run_bot()
