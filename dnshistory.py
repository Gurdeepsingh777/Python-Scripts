import requests

def get_dns_history(domain, api_key):
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"
    
    headers = {
        "Accept": "application/json",
        "API-Key": api_key
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for record in data.get('records', []):
            print(f"IP:{record['values'][0]['ip']}, Last Seen: {record['last_seen']}")
    else:
        print(f"Error: {response.status_code}")