# Authenticate requests to Translator Cognitive Services
The different modes to authenticate request sent to Translator Azure Cognitive Service.

## 1. Authenticate with subscription key
* This can be used for [single-service](https://docs.microsoft.com/en-us/azure/cognitive-services/authentication?tabs=powershell#authenticate-with-a-single-service-subscription-key) or [multi-service](https://docs.microsoft.com/en-us/azure/cognitive-services/authentication?tabs=powershell#authenticate-with-a-multi-service-subscription-key). 
* This is used when invoking the Text Translation service, Document Translation service as well as Custom Translation service.

**Authentication Headers**
| Header | Description |
| :- | :- |
| Ocp-Apim-Subscription-Key | Use this header to authenticate with a subscription key for a specific service or a multi-service subscription key. |
| Ocp-Apim-Subscription-Region | This header is only required when using a multi-service subscription key with the Translator service. Use this header to specify the subscription region. |

```bash
# Sample request
curl --location --request POST 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=hi' \
--header 'Ocp-Apim-Subscription-Key: xxxxxxxxxxxxxxxxxx' \
--header 'Ocp-Apim-Subscription-Region: canadacentral' \
--header 'Content-Type: application/json' \
--data-raw '[{
    "text": "Hello. How are you?"
}]'
```

## 2. Authenticate with a token 
> The services that support authentication tokens may change over time, please check the API reference for a service before using this authentication method.
* This is supported by Text Translation API
* Authentication tokens are included in a request as the Authorization header. The token value provided must be preceded by Bearer, for example: Bearer YOUR_AUTH_TOKEN.
* Authentication tokens are valid for 10 minutes.
```bash
# Request to get the authentication token
curl -X POST \
"https://YOUR-REGION.api.cognitive.microsoft.com/sts/v1.0/issueToken" \
-H "Content-type: application/x-www-form-urlencoded" \
-H "Content-length: 0" \
-H "Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY"
# Pass the token in request as the Authorization header
curl --location --request POST 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=hi' \
--header 'Authorization: Bearer YOUR_AUTH_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '[{
    "text": "Hello. How are you?"
}]'
```

## 3. Authentication with Azure Active Directory (Azure AD)
* It is used for scenarios that require Azure role-based access control (Azure RBAC)
* Authorization headers enable the Translator service to validate that the requesting client is authorized to use the resource and to complete the request.
* Service principal can be authenticated with a certificate or password. 
* User principal is also supported by having permissions delegated through another AAD application. In this case, instead of passwords or certificates, users would be prompted for two-factor authentication when acquiring token.

**Headers**
| Header | Description |
| :- | :- |
| Authorization | It is the access bearer token generated by Azure AD. Token is valid for 10 minutes and should be reused when making multiple calls to Translator |
| Ocp-Apim-ResourceId | It is the Resource ID for your Translator resource instance |
| Ocp-Apim-Subscription-Region | It is the region of the translator resource. This value is optional if the resource is global. |

```bash
rgName=rg-translator # Resource Group name
csName=ts-abhi-demo # Translator cognitive service name
# Get the resource id of the Translator Cognitive service
resourceID=$(az cognitiveservices account show --resource-group $rgName --name $csName --query id -o tsv)
# Create a Service Principal.
az ad sp create-for-rbac -n sp-temp
# Store the output of the above command into variables
appId=
clientSecret=
tenantId=
# Get the objectId using the app Id, The appId is in the output of previous command
spObjectId=$(az ad sp show --id $appId --query "objectId" -o tsv)
# Assign the role 'Cognitive Services User' to the service principal
az role assignment create --assignee $spObjectId --scope $resourceID --role "Cognitive Services User"

# Get the token for Translator Azure Service 
# Sample command
curl --location --request POST 'https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'client_id=<CLIENT_ID>' \
--data-urlencode 'client_secret=<CLIENT_SECRET>' \
--data-urlencode 'scope=https://cognitiveservices.azure.com/.default'
# Actual command with the output stored in variable
# variables in bash aren't interpolated when in single quotes ('). Thus, we set the variables inside double quotes (")
json=$(curl --location --request POST "https://login.microsoftonline.com/$tenantId/oauth2/v2.0/token" \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode "client_id=$appId" \
--data-urlencode "client_secret=$clientSecret" \
--data-urlencode 'scope=https://cognitiveservices.azure.com/.default')
# Extract the value of access_token
token=$(jq -r ".access_token" <<< "$json")

# Pass a bearer token generated either by Azure AD or Managed Identities, resource ID, and the region.
# variables in bash aren't interpolated when in single quotes ('). Thus, we set the variables inside double quotes (")
# Invoke the Translate Azure API endpoint
# Sample command
curl --location --request POST 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=hi' \
--header 'Authorization: Bearer <ACCESS_TOKEN>' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-ResourceId: <RESOURCE_ID>' \
--header 'Ocp-Apim-Subscription-Region: <YOUR_REGION>' \ 
--data-raw '[{"text": "Hello. How are you?"}]'

# Actual command with the variables
region=canadacentral # Set the reion where Translator cognitive service is hosted

curl --location --request POST 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=hi' \
--header "Authorization: Bearer $token" \
--header 'Content-Type: application/json' \
--header "Ocp-Apim-ResourceId: $resourceID" \
--header "Ocp-Apim-Subscription-Region: $region" \
--data-raw '[{"text": "Hello. How are you?"}]'
```

## References
* [Authenticate requests to Translator Cognitive Services](https://docs.microsoft.com/en-us/azure/cognitive-services/authentication?tabs=powershell)