import os
import http.client
import json
import ssl
from pathlib import Path
from dotenv import load_dotenv

# ************* Load .env file*************
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


certificate_file =os.getenv('devicecertificatepath')
key_file = os.getenv('privatekeypath')
certificate_secret= os.getenv('certificaesecret')
host=os.getenv('host')

resource_url=os.getenv('path')

final_url = 'https://'+host+resource_url

request_headers = {
    'Content-Type': os.getenv('contenttype')
}


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(certfile=certificate_file, password=certificate_secret,keyfile=key_file)

# Create a connection to submit HTTP requests
connection = http.client.HTTPSConnection(host, port=os.getenv('port'), context=context)



connection.request(method=os.getenv('method'), url=final_url, headers=request_headers, body=json.dumps(os.getenv('payload')))

response = connection.getresponse()
print(response.status, response.reason)
data = response.read()
print(data)
 










 






