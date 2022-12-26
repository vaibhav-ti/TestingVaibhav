# EYK Deployment

## Download and install the EYK CLI tool for your OS:
It's recommended to do the initial set-up of EYK from your local machine

### Mac/Linux:
Open your CLI and execute the following to download and run the installation script:

```bash
$ curl -ssl https://eyk-assets.ey.io/eyk/eyk-installer.sh | bash
```

### Windows:
Use your browser to download the script, then use PowerShell to install it:
Navigate to: https://eyk-assets.ey.io/eyk/eyk-installer.ps1

[More Details](https://support.cloud.engineyard.com/hc/en-us/articles/360057913834-Download-the-Kontainers-CLI-Tool)

### Login to EYK

After the installation, open https://eyk.ey.io/app in your default browser and login to the web console.

Then, run the following in your shell. 

```bash
./eyk ssologin https://eyk.central-staging-qa.eyk-central.ey.io
```
This will log you into the central-staging-qa cluster. 

### Create an EYK App

- Using CLI
  - Run `./eyk apps:create {EYK_APP_NAME}` to create an EYK app

- Using Web Console
    - Click on the `+` icon on the top right corner of the web console
    - Select the cluster and enter the name of the app and click on `Create`

### Getting EYK HOST:

Assuming you have setup EYK cli locally on your machine,
Run following command to get command for Add EYK remote step
`git remote show eyk`
 
It would give you Push URL like this :
Push  URL: `ssh://git@eyk-builder.central-staging-qa.eyk-central.ey.io:2222/api-backend.git`

If it fails, you can get the EYK SSH host from the cluster information and then run the following commands to set the remote url.

```commandline
git remote add eyk 'ssh://git@{EYK_SSH_HOST}:2222/{EYK_APP_NAME}.git'
git push -u eyk main
```

### Getting SSH Keys:
For generating ssh keys follow [EYK docs](https://support.cloud.engineyard.com/hc/en-us/sections/360009109134-Engine-Yard-Kontainers-New-User-Guide).

If you have already setup eyk on local machine then you can use already generated private keys.

### EYK Push

```commandline
git push eyk
```

**Tips for Environment Variables:**
Use this command if you want to push all env variables stored in .env  to EYK.
```commandline
./eyk config:push
```

### Open the deployed EYK app

```commandline
./eyk open
```

### Configure Custom Domain SSL Certificate 

- Add you custom domain to the app by following the instructions from [Change DNS records](Pointing CD Pipeline Scripts to EYK)  
- Add certificate to the cluster

`./eyk certs:add <cert-name> <publickey.pem> <privkey.pem>`
    
`E.g ./eyk certs:add wildcard-eytest-link pubkey.pem privkey.pem`

- Attach the certificate to the custom domain

`./eyk certs:attach <cert-name> <custom-domain>`

`E.g. ./eyk certs:attach wildcard-eytest-link sabhttps.eytest.link`

[Full Documentation](https://docs.google.com/document/d/1oTKZriTJlJr4DpIhWxtb7JSQXQzCcFIbXY2ZIi2bsMY/)
