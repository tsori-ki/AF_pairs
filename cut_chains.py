import requests
import json

sequence = "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGP..."
prediction_type = "long"  # or "short", "structured"

url = "https://iupred2a.elte.hu/iupred3/api/predict"  # Verify the correct endpoint
headers = {"Content-Type": "application/json"}
payload = {
    "sequence": sequence,
    "type": prediction_type
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    data = response.json()
    score = data.get("score")
    print(score)
else:
    print(f"Error {response.status_code}: {response.text}")
