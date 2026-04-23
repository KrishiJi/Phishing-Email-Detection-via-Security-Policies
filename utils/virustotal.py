<<<<<<< HEAD
import requests

API_KEY = "your_api_key_here"

HEADERS = {
    "x-apikey": "0e3785b20178e2f58d05394f47edf3870ac7c519187385b1719fcd7010244d87"
}


# -------------------------------
# IP CHECK
# -------------------------------
def check_ip(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    
    stats = data["data"]["attributes"]["last_analysis_stats"]
    return stats


# -------------------------------
# URL CHECK
# -------------------------------
def check_url(url_to_check):
    url = "https://www.virustotal.com/api/v3/urls"
    
    data = {"url": url_to_check}
    response = requests.post(url, headers=HEADERS, data=data)
    
    if response.status_code != 200:
        return None
    
    analysis_id = response.json()["data"]["id"]

    # Fetch result
    result_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    result = requests.get(result_url, headers=HEADERS)

    if result.status_code != 200:
        return None

    stats = result.json()["data"]["attributes"]["stats"]
    return stats


# -------------------------------
# FILE HASH CHECK
# -------------------------------
def check_file_hash(file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None

    data = response.json()
    stats = data["data"]["attributes"]["last_analysis_stats"]

    return stats
=======
import requests

API_KEY = "your_api_key_here"

HEADERS = {
    "x-apikey": API_KEY
}


# -------------------------------
# IP CHECK
# -------------------------------
def check_ip(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    
    stats = data["data"]["attributes"]["last_analysis_stats"]
    return stats


# -------------------------------
# URL CHECK
# -------------------------------
def check_url(url_to_check):
    url = "https://www.virustotal.com/api/v3/urls"
    
    data = {"url": url_to_check}
    response = requests.post(url, headers=HEADERS, data=data)
    
    if response.status_code != 200:
        return None
    
    analysis_id = response.json()["data"]["id"]

    # Fetch result
    result_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    result = requests.get(result_url, headers=HEADERS)

    if result.status_code != 200:
        return None

    stats = result.json()["data"]["attributes"]["stats"]
    return stats


# -------------------------------
# FILE HASH CHECK
# -------------------------------
def check_file_hash(file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None

    data = response.json()
    stats = data["data"]["attributes"]["last_analysis_stats"]

    return stats
>>>>>>> c5df351399b66f378090fa9d86ad08b85a9527ef
