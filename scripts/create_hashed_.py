import bcrypt
import yaml

# Function to hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Load YAML file
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Hash all passwords and update YAML structure
for username, user_data in config["credentials"]["usernames"].items():
    if "password" in user_data and not user_data["password"].startswith("$2b$"):
        user_data["password"] = hash_password(user_data["password"])

# Save the updated YAML file with hashed passwords
with open('./config.yaml', 'w') as file:
    yaml.dump(config, file)
