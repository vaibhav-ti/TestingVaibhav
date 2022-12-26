# Social Authentication

## Usage

### Token Authentication

- `POST /auth/login/social/token/`

    Input:
    ```json
    {
      "provider": "google",
      "code": "AQBPBBTjbdnehj51"
    }
    ```
    
    Output:
    ```JSON
    {
      "token": "68ded41d89f6a28da050f882998b2ea1decebbe0"
    }
    ```

- `POST /auth/login/social/token_user/`
    
    Input:
    ```JSON
    {
      "provider": "google",
      "code": "AQBPBBTjbdnehj51"
    }
    ```

    Output:
    ```JSON
    {
      "username": "Alex",
      "email": "user@email.com",
      // other user data
      "token": "68ded41d89f6a28da050f882998b2ea1decebbe0"
    }
    ```
  

### OAuth 2.0 workflow with rest-social-auth

1. Front-end need to know following params for each social provider:

   - **client_id** # only in case of OAuth 2.0, id of registered application on social service provider
   - **redirect_uri** # to this url social provider will redirect with code
   - **scope**=your_scope # for example email
   - **response_type**=code # same for all oauth2.0 providers

2. Front-end redirect user to social authorize url with params from previous point.

3. User confirms.

4. Social provider redirects back to `redirect_uri` with param `code`. For Front-end React template the `redirect_uri` is `/login`

5. Front-end now ready to login the user. To do it, send POST request with provider name and code:

    `POST /auth/login/social/token/`

    with data (form data or json)

    `provider=google-oauth2&code=AQBPBBTjbdnehj51`

    Backend will either signin the user, either signup, either return error.
    
    Sometimes it is more suitable to specify provider in url, not in request body. It is possible, rest-social-auth will understand that. Following request is the same as above:
    
     `POST /auth/login/social/token/google-oauth2/`
    
    with data (form data or json)
    
     `code=AQBPBBTjbdnehj51`

## Redirect URI 

Set the Environment Variable 

```commandline
REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI = <frontend-social-redirect-uri>
```

If you are using the frontend template, the redirect URI is `http://localhost:3000/login` for developing locally and `https://<frontend-domain>/login` for production.


## DevConnect (OIDC)

Set the Environment Variables

```commandline
DEVCONNECT_ISSUER_URL = https://devfactory.devconnect-df.com/auth/realms/devfactory
DEVCONNECT_CLIENT_ID = <client-id>
DEVCONNECT_CLIENT_SECRET = <client-secret>
```

### For Frontend 
Send a POST request to `BASE_URL + '/auth/login/social/token/devconnect/'` with the following data:

```json
{
    "code": "5049f36d-5eac-44e0-b005-6a80a64d8802.3764078a-b103-4ec3-b28e-6092b95fb99e.104d2625-dd83-40b6-b602-6cfb1882bae2"
}
```

Response: 

```json
{
    "token": "68ded41d89f6a28da050f882998b2ea1decebbe0"
}
```


## Cognito
Cognito implemented OAuth2 protocol for their authentication mechanism. <br>

To enable python-social-auth support follow this steps:

- Go to AWS Cognito Console and select Manage User Pools.

- Choose an existing pool or create a new one following the [Cognito Pool Tutorial](https://docs.aws.amazon.com/cognito/latest/developerguide/tutorial-create-user-pool.html).

- Create an app (make sure to generate a client secret) and configure a pool domain [(Cognito App Configuration)](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-configuring-app-integration.html):
    
Set the Environment Variables

```json
SOCIAL_AUTH_COGNITO_KEY = ...
SOCIAL_AUTH_COGNITO_SECRET = ...
SOCIAL_AUTH_COGNITO_POOL_DOMAIN = ...
```

On your project settings, you should add Cognito on your AUTHENTICATION_BACKENDS:
    
```json
AUTHENTICATION_BACKENDS = (
    ...
    'social_core.backends.cognito.CognitoOAuth2',
    ...
)
```
  
## Google OAuth

#### Create authorization credentials

Any application that uses OAuth 2.0 to access Google APIs must have authorization credentials that identify the application to Google's OAuth 2.0 server. The following steps explain how to create credentials for your project.

1. Go to the [Credentials page](https://console.developers.google.com/apis/credentials)
2. Click Create credentials > OAuth client ID.
3. Select the Web application application type.
4. Fill in the form and click Create. specify authorized redirect URIs. The redirect URIs are the endpoints to which the OAuth 2.0 server can send responses.

After creating your credentials, set them as env variables

```json
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
```

setup any needed extra scope:

```json
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [...]
```

On your project settings, you should add Google on your AUTHENTICATION_BACKENDS:


```json
AUTHENTICATION_BACKENDS = (
    ...
    'social_core.backends.google.GoogleOAuth2',
    ...
)
```

## GitHub

Register a new application at [GitHub Developers](https://github.com/settings/applications/new), set the callback URL to http://example.com/complete/github/ replacing example.com with your domain and your redirect endpoint. This will generate a Client Key and a Client Secret.

Add these values of Client ID and Client Secret from GitHub as Environment Variables.

```json
SOCIAL_AUTH_GITHUB_KEY = 'a1b2c3d4'
SOCIAL_AUTH_GITHUB_SECRET = 'e5f6g7h8i9'
```

Also it’s possible to define extra permissions with:

```json
SOCIAL_AUTH_GITHUB_SCOPE = [...]
```

On your project settings, you should add Github on your AUTHENTICATION_BACKENDS:

```json
AUTHENTICATION_BACKENDS = (
    ...
    'social_core.backends.github.GithubOAuth2',
)
```
