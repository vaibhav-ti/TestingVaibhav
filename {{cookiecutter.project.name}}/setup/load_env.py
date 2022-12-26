import os
import sys
if len(sys.argv)<2:
    encrypted_file_path = "env/.env.prod.enc"
else:
    encrypted_file_path = sys.argv[1]
    
if not os.path.isfile("keys/private_key.pem"):
    rsa_key = os.getenv("RSA_PRIVATE_KEY")
    if rsa_key is None:
        print("RSA Private Key not found.")
        exit(1)

    with open("keys/private_key.pem", "w+", encoding="utf-8") as file:
        file.write(rsa_key)

if not os.path.isfile(encrypted_file_path):
    print("encrypted secrets not Found, cannot run without secrets")
    exit(1)

try:
    os.system("openssl rsautl -decrypt -inkey keys/private_key.pem -in keys/symmetric_keyfile.key.enc -out keys/symmetric_keyfile.key")
except Exception as ex:
    print(f"Failed to decrypt key. RSA Private key invalid! {str(ex)}")

try:
    os.system(
        f"openssl enc -in {encrypted_file_path} -out .env -d -aes256 -k keys/symmetric_keyfile.key")

except Exception as ex:
    print(f"Failed to decrypt prod environment. {str(ex)}")
