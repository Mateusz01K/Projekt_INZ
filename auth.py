import pandas as pd
import hashlib
import os

USER_DATA_FILE = 'users.csv'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if os.path.exists(USER_DATA_FILE):
        users_df = pd.read_csv(USER_DATA_FILE)
    else:
        users_df = pd.DataFrame(columns=["username", "password"])

    if username in users_df['username'].values:
        return False

    new_user = pd.DataFrame([(username, hash_password(password))], columns=["username", "password"])
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(USER_DATA_FILE, index=False)
    return True

def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        return False

    users_df = pd.read_csv(USER_DATA_FILE)
    hashed_password = hash_password(password)

    if username in users_df['username'].values:
        stored_password = users_df[users_df['username'] == username]['password'].values[0]
        if stored_password == hashed_password:
            return True

    return False