import http.client

host = '<domain>.cognitiveservices.azure.com'
parameters = '//translator/text/batch/v1.0/batches/bf446717-b22f-4a78-9204-1a9c7efb0ddb/documents'
#parameters = '//translator/text/batch/v1.0/batches/24ef365b-3bfe-4c96-a676-a4c0137a02a1'
key =  '<add-key>'
conn = http.client.HTTPSConnection(host)
payload = ''
headers = {
  'Ocp-Apim-Subscription-Key': key
}
conn.request("GET", parameters , payload, headers)
res = conn.getresponse()
data = res.read()
print(res.status)
print()
print(data.decode("utf-8"))