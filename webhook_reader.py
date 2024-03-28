'''
from flask import Flask, request
import urllib.parse
import json  # Import the json module

app = Flask(__name__)

@app.route("/circle", methods=["POST"])
def webhook():
  # Check if the request content type is URL-encoded form
  if request.content_type == "application/json":
    # Get the form data
    form = request.form
    
    # Check if 'payload' parameter exists
    if 'payload' in form:
      # Get the encoded payload
      encoded_payload = form['payload']
      
      # Decode the payload (URL-decode)
      try:
        payload = urllib.parse.unquote_plus(encoded_payload)
        print("Webhook request received!")
        # Assuming the payload is JSON, try parsing it
        try:
          data = json.loads(payload)
          print(json.dumps(data, indent=4))  # Pretty print JSON data
        except json.JSONDecodeError:
          print("Error: Could not parse payload as JSON")
      except Exception as e:  # Catch any exceptions (better practice)
        print(f"Error: {e}")
    else:
      print("Error: Missing 'payload' parameter")
      return "Missing 'payload' parameter", 400  # Bad request

  else:
    print("Request content type is not application/x-www-form-urlencoded")
    return "Unsupported content type", 415  # Unsupported media type

  return "Success", 200

if __name__ == "__main__":
  app.run(debug=True)
'''

from flask import Flask, request
import urllib.parse
import json

app = Flask(__name__)

@app.route("/circle", methods=["POST"])
def webhook():
  # Check if request has JSON data
  if request.is_json:
    # Get the JSON data directly
    try:
      data = request.get_json()
      print("Webhook request received!")
      print(json.dumps(data, indent=4))  # Pretty print JSON data
      return "Success (JSON payload)", 200
    except json.JSONDecodeError:
      print("Error: Could not parse request body as JSON")
      return "Invalid JSON format", 400  # Bad request

  # Check if request has URL-encoded form data (fallback)
  elif request.content_type == "application/x-www-form-urlencoded":
    # Get the form data
    form = request.form
    
    # Check if 'payload' parameter exists
    if 'payload' in form:
      # Get the encoded payload
      encoded_payload = form['payload']
      
      # Decode the payload (URL-decode)
      try:
        payload = urllib.parse.unquote_plus(encoded_payload)
        print("Webhook request received!")
        # Assuming the decoded payload is JSON, try parsing it
        try:
          data = json.loads(payload)
          print(json.dumps(data, indent=4))  # Pretty print JSON data
        except json.JSONDecodeError:
          print("Error: Could not parse payload as JSON")
          return "Invalid JSON format", 400  # Bad request
      except Exception as e:  # Catch any exceptions (better practice)
        print(f"Error: {e}")
        return "Error processing payload", 500  # Internal server error
    else:
      print("Error: Missing 'payload' parameter")
      return "Missing 'payload' parameter", 400  # Bad request

  else:
    print("Unsupported content type:", request.content_type)
    return "Unsupported content type", 415  # Unsupported media type

if __name__ == "__main__":
  app.run(debug=True)
