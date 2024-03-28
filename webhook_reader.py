from flask import Flask, request
import urllib.parse
import json  # Import the json module

app = Flask(__name__)

@app.route("/circle", methods=["POST"])
def webhook():
  # Check if the request content type is URL-encoded form
  if request.content_type == "application/x-www-form-urlencoded":
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
