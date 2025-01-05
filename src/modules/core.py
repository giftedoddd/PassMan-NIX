from pathlib import Path
import json, pyotp, secrets, string

DATA_PATH = Path("/home/giftedodd/IdeaProjects/Pycharm/PassMan-NIX/test/secure.enc")


def create_password(website, username, password, is_otp):
    password_sample = {
        website: {
            username: {
                "password": password,
                "OTP": is_otp
            }
        }
    }

    if not DATA_PATH.exists():
        DATA_PATH.touch()

    try:
        with DATA_PATH.open("r") as password_json:
            password_dict = json.load(password_json)
    except json.decoder.JSONDecodeError:
        with DATA_PATH.open("w") as password_list_:
            json.dump(password_sample, password_list_, indent=4)
    else:
        with DATA_PATH.open("w") as password_list__:
            password_dict.update(password_sample)
            json.dump(password_dict, password_list__, indent=4)


def search_password(website, username):
    try:
        with DATA_PATH.open("r") as password_list:
            passwords_dict = json.load(password_list)
            is_otp = passwords_dict[website][username]["OTP"]
    except json.decoder.JSONDecodeError:
        return False, "Create A Password First"
    except KeyError:
        return False, "Username Not Found"
    else:
        if not is_otp:
            output = passwords_dict[website][username]["password"]
            clipboard_stack(username, output)
            return True, "Password Copied"
        secret = passwords_dict[website][username]["password"]
        output = pyotp.TOTP(secret)
        clipboard_stack(username, output)
        return True, "OTP Pass Copied"

def clipboard_stack(username, password):
    pass

def generate_random_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(16))

    return password