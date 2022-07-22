# Document translation service

Refer this [Microsoft documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/document-translation/get-started-with-document-translation?tabs=python)

> The sample json payload in MS site was erroring out during testing. Updated in the sample code shown here.

## Sample code
### Translate a file or batch of files in Azure storage account in a container.
* [translate.py](translate.py) 

Sample response
```bash
response status code: 202
response status: Accepted
response headers: {'Content-Length': '0', 'Set-Cookie': 'ARRAffinity=33fbf50c6ad4c582ac8004aca68642f10adb04fe054ff8458eeabba45ade526c;Path=/;HttpOnly;Secure;Domain=mtbatch.nam.microsofttranslator.com, ARRAffinitySameSite=33fbf50c6ad4c582ac8004aca68642f10adb04fe054ff8458eeabba45ade526c;Path=/;HttpOnly;SameSite=None;Secure;Domain=mtbatch.nam.microsofttranslator.com', 'X-RequestId': 'a07af38a-e5b1-4faa-ab23-a1459b0555ac', 'Operation-Location': 'https://mydomain.cognitiveservices.azure.com/translator/text/batch/v1.0/batches/01ec76aa-9d85-4fde-baad-1db3d8e8bc87', 'X-Powered-By': 'ASP.NET', 'apim-request-id': 'a07af38a-e5b1-4faa-ab23-a1459b0555ac', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload', 'x-content-type-options': 'nosniff', 'Date': 'Fri, 22 Jul 2022 15:22:34 GMT'}
```

### Get the job status of the translation
* [job-status.py](job-status.py)

Sample response - 200 OK
```json
{
    "id": "bf446717-b22f-4a78-9204-1a9c7efb0ddb",
    "createdDateTimeUtc": "2022-07-21T21:22:08.5826539Z",
    "lastActionDateTimeUtc": "2022-07-21T21:22:34.0893925Z",
    "status": "Succeeded",
    "summary": {
        "total": 3,
        "failed": 1,
        "success": 2,
        "inProgress": 0,
        "notYetStarted": 0,
        "cancelled": 0,
        "totalCharacterCharged": 40622744
    }
}
```

### List the status of all the documents in the batch process
* [list-documents-status.py](list-documents-status.py)

Sample response - 200 OK
```json
{
    "value": [
        {
            "path": "https://rgabhilogicapps8be9.blob.core.windows.net/target-translator/sample-English-German-Training-de-38mb.txt",
            "sourcePath": "https://rgabhilogicapps8be9.blob.core.windows.net/source-translator/sample-English-German-Training-de-38mb.txt",
            "createdDateTimeUtc": "2022-07-21T21:22:12.5761664Z",
            "lastActionDateTimeUtc": "2022-07-21T21:24:14.9940975Z",
            "status": "Succeeded",
            "to": "en",
            "progress": 1,
            "id": "0045cab7-0000-0000-0000-000000000000",
            "characterCharged": 37792218
        },
        {
            "path": "https://rgabhilogicapps8be9.blob.core.windows.net/target-translator/Customer-sample-English-German-Training-de.txt",
            "sourcePath": "https://rgabhilogicapps8be9.blob.core.windows.net/source-translator/Customer-sample-English-German-Training-de.txt",
            "createdDateTimeUtc": "2022-07-21T21:22:12.5683717Z",
            "lastActionDateTimeUtc": "2022-07-21T21:22:30.1170792Z",
            "status": "Succeeded",
            "to": "en",
            "progress": 1,
            "id": "0045cab6-0000-0000-0000-000000000000",
            "characterCharged": 2830526
        },
        {
            "sourcePath": "https://rgabhilogicapps8be9.blob.core.windows.net/source-translator/sample-English-German-Training-de-gt40mb.txt",
            "lastActionDateTimeUtc": "2022-07-21T21:22:09.5794298Z",
            "status": "Failed",
            "to": "en",
            "error": {
                "code": "InvalidRequest",
                "message": "The maximum document file size has been exceeded.",
                "target": "Document",
                "innerError": {
                    "code": "MaxDocumentSizeExceeded",
                    "message": "The maximum document file size has been exceeded."
                }
            },
            "progress": 0,
            "id": "0045cab8-0000-0000-0000-000000000000",
            "characterCharged": 0
        }
    ]
}
```

### Get the status of a document
* [document-status.py](document-status.py) 

Sample response - 200 OK
```json
{
    "path": "https://rgabhilogicapps8be9.blob.core.windows.net/target-translator/sample-English-German-Training-de-38mb.txt",
    "sourcePath": "https://rgabhilogicapps8be9.blob.core.windows.net/source-translator/sample-English-German-Training-de-38mb.txt",
    "createdDateTimeUtc": "2022-07-21T21:22:12.5761664Z",
    "lastActionDateTimeUtc": "2022-07-21T21:24:14.9940975Z",
    "status": "Succeeded",
    "to": "en",
    "progress": 1,
    "id": "0045cab7-0000-0000-0000-000000000000",
    "characterCharged": 37792218
}
```