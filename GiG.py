import os
import subprocess
import requests

GITHUB_REPO = "https://github.com/SCP-OMI/SCP-OMI"
LOCAL_REPO = "SCP-OMI"  # This is a relative path, not absolute

def clone_repo():
    print("Cloning the repository...")
    result = subprocess.run(["git", "clone", GITHUB_REPO], capture_output=True, text=True)
    if result.returncode == 0:
        print("Repository cloned successfully.")
    else:
        print(f"Error cloning the repository: {result.stderr}")

def edit_Readme():
    # Correct path construction without leading slash
    readme_path = os.path.join(LOCAL_REPO, "README.md")
    print(f"README path: {readme_path}")
    
    # List the contents of the directory to debug
    try:
        repo_contents = os.listdir(LOCAL_REPO)
        print(f"Contents of {LOCAL_REPO}: {repo_contents}")
    except FileNotFoundError:
        print(f"The directory {LOCAL_REPO} does not exist.")
        return

    # Check if README.md exists
    if not os.path.exists(readme_path):
        print(f"README.md not found in {readme_path}. Exiting.")
        return
    
    # Read and edit the README.md file
    with open(readme_path, "r") as file:
        lines = file.readlines()

    response = requests.get('https://api.api-ninjas.com/v1/facts', headers={'X-Api-Key': '4IFrHonWxgZE6X1+Q6E3CQ==eW7odpXPwVrlCwD4'})
    fun_fact = " " + response.json()[0]['fact']
    fun_fact_found = False
    
    # Find the "<br>⚡ Fun Fact :" line and update it
    for i, line in enumerate(lines):
        if "<br>⚡ Fun Fact :" in line:
            # Save the original line
            original_line = line.strip()
            
            # Replace only the fun fact portion
            start_index = line.index("<br>⚡ Fun Fact :") + len("<br>⚡ Fun Fact :")
            # We will only modify the part after "Fun Fact :"
            modified_line = f"{fun_fact}\n"
            
            # Replace the whole line with the modified line
            lines[i] = line[:start_index] + modified_line
            fun_fact_found = True
            # print(f"Updated fun fact in line: {lines[i].strip()}")
            break
    

    # Write the updated content back to README.md
    with open(readme_path, "w") as file:
        file.writelines(lines)
    
    print("README.md updated successfully.")


def push_changes():
    print("Pushing the changes to the repository...")
    os.chdir(LOCAL_REPO)
    subprocess.run(["git", "add", "README.md"])
    subprocess.run(["git", "commit", "-m", "Updated fun fact"])
    subprocess.run(["git", "push"])
    os.chdir("..")  # Go back to the parent directory after pushing

    print("Changes pushed successfully.")


def main():
    if os.path.exists(LOCAL_REPO):
        print("Repository already exists. Pulling the latest changes...")
        os.chdir(LOCAL_REPO)
        subprocess.run(["git", "pull"])
        os.chdir("..")  # Go back to the parent directory after pulling
    else:
        clone_repo()

    print("Running the bot...")
    edit_Readme()

    push_changes()

if __name__ == "__main__":
    main()
