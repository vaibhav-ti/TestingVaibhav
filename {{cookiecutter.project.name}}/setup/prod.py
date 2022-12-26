import os
from common import update_env_template

root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
os.chdir(root_dir)

if os.path.isfile("env/.env.prod.enc"):
    os.system("openssl rsautl -decrypt -inkey keys/private_key.pem -in keys/symmetric_keyfile.key.enc -out keys/symmetric_keyfile.key")
    os.system(
        "openssl enc -in env/.env.prod.enc -out .env.prod -d -aes256 -k keys/symmetric_keyfile.key"
    )
    os.remove("keys/symmetric_keyfile.key")

update_env_template(
    env_path="env/.env.prod",
    template_path="env/.env.prod.template"
)
