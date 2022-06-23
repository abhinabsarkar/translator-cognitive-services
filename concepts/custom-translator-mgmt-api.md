# Manage Custom Translator service programmatically
[Custom Translator](https://portal.customtranslator.azure.ai/) can also be programmatically accessed through a [dedicated API](https://custom-api.cognitive.microsofttranslator.com/swagger/). The API allows users to manage creating or updating training through their own app or webservice.

A sample ASP.NET MVC application to manage the Custom Translator Cognitive service is provided - https://github.com/MicrosoftTranslator/CustomTranslatorApiSamples  

The application covers the features like creating project, training model, uploading files, etc & is well described on how to configure it.

![alt txt](/images/mvc_app_landing_page.png)

The [Custom Translator Management APIs](https://custom-api.cognitive.microsofttranslator.com/swagger/) which are used by the above application, requires authentication token.

This article describes how the authentication flow works.

## Authentication flow for the Custom Translator Management APIs
For authenticating the Custom Translator Management APIs, the Microsoft identity platform implementation of [OAuth 2.0 and Open ID Connect (OIDC)](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) is used. It is recommended to use the supported Microsoft Authentication Libraries (MSAL) to acquire tokens and call secured web APIs.
* [Scenarios and supported authentication flows](https://docs.microsoft.com/en-us/azure/active-directory/develop/authentication-flows-app-scenarios#scenarios-and-supported-authentication-flows)
* [Sample Apps that uses MSAL](https://docs.microsoft.com/en-us/azure/active-directory/develop/sample-v2-code)

**OAuth 2.0 with OIDC - Sequence UML diagram**

![alt txt](/images/OAuth2.0%20Authorization%20Code%20flow1.png)

## Steps to visualize the above UML diagram

### 1. Pre-requisite: Create and Register your Azure AD Client App
* Sign in to https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
* Click “New Registration”. Enter a name "svc-custom-translator-1" for the App ID.
* Select "Redirect URI" as Web. Enter the value as "http://localhost". 
    * To learn more about the Redirect URI, refer [Redirect URI - restrictions and limitations](https://docs.microsoft.com/en-us/azure/active-directory/develop/reply-url)
* Click Register. At this point, you will be directed to an overview page with details about your AppID. Store the client id.
* Navigate to Certificates and Secrets and click “New client secret”. Generate the secret & store it.

If you go back to the AppID "svc-custom-translator-1" & click on it beside "Managed application in local directory". 
![alt txt](/images/managed-application.png)

Click on permissions under security on the Resource Menu in left. Click on User Consent. You will find "No user consented permissions found for the application".

### 2. Send an Authorize GET request
> GET requests should be copy & pasted into a browser, since they'll require interactive user login.

Send a sign in request to begin the OAuth 2.0 code flow. Be sure to copy & paste into a browser! Running this request in Postman will just return you the HTML of our login pages.

```bash
# GET request
https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/authorize
```

**Query Params**
| Header | Description | Value | 
| :- | :- | :- |
| client_id | Application (client) ID | xxxxxxxxxxxxxxxxxxxx |
| response_type | Must include `code` for the authorization code flow | code |
| redirect_uri | redirect_uri of your app, where authentication responses can be sent and received by your app. | http://localhost |
| response_mode | Specifies how the identity platform should return the requested token to your app. `query`: Default when requesting an access token. Provides the code as a query string parameter on your redirect URI | query |
| scope |  space-separated list of [scopes](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-permissions-and-consent) that you want the user to consent to | offline_access%20email%20openid |

Refer the following links to learn more about the requests & parameters
* [Request an authorization code](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow#request-an-authorization-code)
* [Azure AD v2.0 Protocols in Postman](https://www.postman.com/lmedenred/workspace/lm-s-public-workspace/documentation/11230239-b21fae30-d087-43e9-986b-526841c50434)

The offline_access is a scope required to receive refresh token. When you redeem an authorization code in the OAuth 2.0 authorization code flow without offline_access scope, you'll receive only an access token from the /token endpoint. When this scope is included, both Access & Refresh tokens are returned. 

The request when copied & pasted on browser will request for the user's consent.

![alt txt](/images/consent.png)

Once you click on Accept, it will redirect to the url mentioned in redirect_uri. The url will return a code & session state in the browser as query parameter. Store the code which starts with 0. till the session state. 

Sample code value

`0.ARoAv4j5cvGGr0GRqy180BHbR7TwVefI2NtFsdl-iBlOWoaABU.AgABAAIAAAD--DLA3VO7QrddgJg7WevrAgDs_wQA9P8QCUfs20CeVZBoAhcrewXmTzVP_e9Wls-AitvebTwOPOaJGignMRH8DtFxLhqNuB8kzPhGsv6wY01FXYpm3ySu7PX6D3wRAipErxR6p7ey39aOx_b4wBD3cUyJ768xCBTOc0_VgwfmBW9r9QFesO3cVn71ozbsT0FS68j6tlv_FX4mHb0P17Ab4wMcHe9u35kgEpkSOI3LkhVVT9evFARNZ7IDe5AhSF_K5fVqepF4Ak3p4FIIiOttCVAFo2ao-FcdKuxNju6nwMBTIyxs1f0ETKnVF9gTzgE6xFhz8eQXjB6WKb6WoNpxghzEXuE659n-ajxaeh3ZmhleUQnOkQeyuCiCVf8x4fpjkXLLGlJ_dTmgCWgLJiKd11pMfGZsCNTcrU2Usdfs7FGnLgB6OEpFkxS2ydAcqXvnY2cZqT80R4az4-5b-ND6z_I5CkejbY4uNYl528UtqBUmXD_Rbd8mnBVstzDxEaOaZGtTeP-bXnueD6A-Mm26C6sDhJOpvb3CO5PDDqa6lq2lRFQVEKNiuQPbRqhkfXhVWc9hWxP0eTzfjVIxsp_H2LLUAXUeTetLU1N9tLQzZqmE1yEpo6NeTz1axFsDGkd_UYrdvMgsn3hQfjXW8okvtp_kDECN-RH69fRF8HX4amcrFhpdVv2F-lweH4SFyjQZ7w6ef96E5brWJL3uBXi0Y7QiONgXo1w_Pwi77gYEQ6zDP1n183LZEbx04W30p4TGBm0dcvxY4_xoXRuCjYDHRS8Ldwv-N5fgtdEldnezmTZ_kJZxKEUbIaRZFoyQ9-_Z_e3Yfd_Bfh-m1XWaIXslJpdIZ8BdsdfsCwpsWohMZw54MbP5x-x8wtvg36_3wWP1dQ`

If you check the permissions in Azure portal for the AppId "svc-custom-translator-1", it will show the below permissions delegated on behalf of the user.

![alt txt](/images/permissions.png)

### 3. POST - Token request using Auth Code
Make a POST request to exchange the auth code for the ID token. It will also return an Access Token & the Refresh Token.

```bash
POST https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token
```

**Request Headers**
| Header | Value | 
| :- | :- |
| Content-Type | application/x-www-url-form-urlencoded | 
| **Body urlencoded** |
| client_id | xxxxxxxxxxxxxxxxxxxx |
| client_secret | yyyyyyyyyyyyyyyyyyy |
| scope |  offline_access%20email%20openid |
| redirect_uri | http://localhost |
| grant_type | authorization_code |
| code | {Code copied from the browser} |

Response received is JSON containing id_token, access_token & refresh_token.

### 4. Use the token for calling the Custom Translator Management API
Go to the swagger interface  
https://custom-api.cognitive.microsofttranslator.com/swagger/#!/Regions/ApiTexttranslatorV1_0RegionsGet 

Go to the "Regions" API --> for the authorization parameter, enter the value "Bearer <id_token>".

![alt txt](/images/swagger-regions.png)

Click Try it out!. It should return the list of regions.

What this means is a workflow like this can be used for automation scenarios:
1) Log-in once interactively to get the id token and a refresh token.
2) Store both the id token and the refresh token in a cache.
3) Automation can use the id token to login without the need for user intervention.
4) When the id token expires, a new token can be retrieved and stored by using the refresh token

Refer this link for a sample desktop app to get the id_token - https://github.com/MicrosoftTranslator/CustomTranslator-API-CSharp
