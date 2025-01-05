def otp_match(data):
    match_result = data.startswith("otpauth://")
    return match_result

def get_secret(data):
    secret = data.split("=")[1].split("&")[0]
    return secret
