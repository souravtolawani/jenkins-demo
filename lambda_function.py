import json
import uuid
import base64
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Registration')   

def lambda_handler(event, context):
    try:
        body = event.get('body') or '{}'

        
        if event.get('isBase64Encoded'):
            body = base64.b64decode(body).decode('utf-8')

      
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {k: v[0] for k, v in parse_qs(body).items()}

        
        data['id'] = str(uuid.uuid4())

        
        table.put_item(Item=data)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Registration successful', 'id': data['id']})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }



#--------------------------------------------------------------------------------------------------------------------
#test code :
{
  "body": "{\"name\": \"Saurav\", \"email\": \"saurav@example.com\", \"phone\": \"9876543210\"}"
}

#_______________________________________________________________________________________________________________________
#registration form 

<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Registration Form</title>
</head>
<body>
  <h2>Registration Form</h2>
  <form id="regForm">
    <input type="text" id="name" placeholder="Name" required><br><br>
    <input type="email" id="email" placeholder="Email" required><br><br>
    <input type="text" id="phone" placeholder="Phone" required><br><br>
    <button type="submit">Register</button>
  </form>

  <script>
  document.getElementById("regForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const data = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      phone: document.getElementById("phone").value
    };
    try {
      const res = await fetch("https://ijwaxlwbkugbfpewcfnja4fyqa0asddu.lambda-url.ap-south-1.on.aws/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      const result = await res.json();
      alert(result.message || result.error);
    } catch (err) {
      alert("Request failed: " + err.message);
    }
  });
  </script>
</body>
</html>
