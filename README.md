# 1. Introduction
There are multiple options available for publishing and subscribing messages with AWS IOT Core. The message broker supports the use of the MQTT protocol to publish and subscribe and the HTTPS protocol to publish. Both protocols are supported through IP version 4 and IP version 6. The message broker also supports MQTT over the WebSocket protocol.

Here is a simple table that shows various protocol and port options available for handshake with AWS IOT Core.
<p align="center">
<img src="/images/iotportprotocol.png">
</p>


More details are available here https://docs.aws.amazon.com/iot/latest/developerguide/protocols.html

# 2. Objective
This post covers the option #2 - ingesting to AWS IoT Core using HTTPs and X509Certificate on port 8443. The code samples are provided in NodeJs and Python, which is covered in the following sections.

# 3. Python code to publish to AWS IoT Core using HTTPs protocol and AWS Sigv4 authentication
Create a directory for solution called 'PythonSample'.

Create an environment .env file at the root of the folder  with the following configuration.

``` .env

#HTTP method should be POST
method=POST

# Content Type to be sent as a part of HTTP request is 'application/json'
contenttype = 'application/json'

# resource path
path='/topics/topic_1'

# set port for request
port=8443

# Set the AWS IoT host name specific to your AWS account

host = 'youriotendpoint.amazonaws.com'

# Set the post data message
postdata = 'Hello World'

# Set the path of the private key of the IoT Device
privatekeypath = './ALPNTestDevice.private.key'

# Set the path of the certificate of the IoT Device

devicecertificatepath='./ALPNTestDevice.cert.pem'


# Set the secret for the device certificate

certificatesecret= 'password123'

# Set value of payload
postdata = 'hello world'

# Set the value for payload
payload="{
    'Temperature': 94,
    'Pressure': 24
}"

# Set text message
message = 'hello world'




``` 

Create a python file 'devicesimulatorhttpx509.py' with the following implementation.

``` python
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
``` 

Install the required python packages and execute the above code. You should see that above code is publishing messages successfully to AWS IoT core, with a HTTP Status Code of 200. You can also very that in AWS IoT console.

# 4.NodeJs code to publish to AWS IoT Core using HTTPs protocol and AWS Sigv4 authentication
Create a directory for solution called 'NodeSample'.

Initialize the project and install required packages using npm.

``` bash 
npm init -y
npm install dotenv
``` 

Create an environment .env file at the root of the folder  with the following configuration.

``` .env
#HTTP method should be POST
method=POST

# Content Type to be sent as a part of HTTP request is 'application/json'
contenttype = 'application/json'

# resource path
path='/topics/topic_1'

# set port for request
port=8443

# Set the AWS IoT host name specific to your AWS account

host = 'a1775y1qp2whis-ats.iot.us-east-2.amazonaws.com'

# Set the post data message
postdata = 'Hello World'

# Set the path of the private key of the IoT Device
privatekeypath = './ALPNTestDevice.private.key'

# Set the path of the certificate of the IoT Device

devicecertificatepath='./ALPNTestDevice.cert.pem'


# Set the secret for the device certificate

certificatesecret= 'password123'

# Set value of payload
postdata = 'hello world'

# Set the value for payload
payload="{
    'Temperature': 94,
    'Pressure': 24
}"

# Set text message
message = 'hello world'

``` 

Create a nodejs file 'devicesimulatorhttpx509.js' with the following implementation.

``` javascript

const https = require('https');
const fs = require('fs');
const dotenv = require('dotenv')

//Load the .env file
dotenv.config();

var post_data = process.env.message;

// Set the request parameters for making Http Post using Device Certificate and Private Key
const options = {
  hostname: process.env.host,
  path: process.env.path,
  key: fs.readFileSync(process.env.privatekeypath),
  cert: fs.readFileSync(process.env.devicecertificatepath),
  port: process.env.port,
  method: process.env.method,
  
  headers: {
    'Content-Type': process.env.contenttype,
    'Content-Length': Buffer.byteLength(post_data)
      }
  
};

var post_req=https.request(options,

  function(res)
  {console.log('requested');
  }
);
console.log('succeeded');
post_req.write(post_data);

post_req.on('error', function(err)
{
  console.log(err.message);
}
);

post_req.on('response',function(res)
{
  console.log(res);
}
);


``` 


## License

This library is licensed under the MIT-O license. 
