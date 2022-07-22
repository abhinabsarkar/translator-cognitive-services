import requests

endpoint = "https://<domain>.cognitiveservices.azure.com/translator/text/batch/v1.0"
key =  '<add-key>'
path = '/batches'
constructed_url = endpoint + path

payload= {
    "inputs": [
        {
            #"storageType": "File",
            "source": {
                "sourceUrl": "https://rgabhilogicapps8be9.blob.core.windows.net/source-translator?sp=rl&st=2022-07-21T20:38:32Z&se=2022-07-22T04:38:32Z&spr=https&sv=2021-06-08&sr=c&sig=M1%2BUt4%2Fwz%2BfH8a9uzDsAQVSZeuthCK8jmmMMyMbyNKo%3D",
                "storageSource": "AzureBlob",
                "language": "de"
            },
            "targets": [
                {
                    "targetUrl": "https://rgabhilogicapps8be9.blob.core.windows.net/target-translator?sp=rwl&st=2022-07-21T20:14:13Z&se=2022-07-22T04:14:13Z&spr=https&sv=2021-06-08&sr=c&sig=SRGi9Awi1RaVqRABu6wk2DrB6DR6F3UsX1cH1wXiSss%3D",
                    "storageSource": "AzureBlob",
                    "category": "general",
                    "language": "en"
                }
            ]
        }
    ]
}
headers = {
  'Ocp-Apim-Subscription-Key': key,
  'Content-Type': 'application/json'
}

response = requests.post(constructed_url, headers=headers, json=payload)

print(f'response status code: {response.status_code}\nresponse status: {response.reason}\nresponse headers: {response.headers}')