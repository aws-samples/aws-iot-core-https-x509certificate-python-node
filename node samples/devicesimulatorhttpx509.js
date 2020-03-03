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