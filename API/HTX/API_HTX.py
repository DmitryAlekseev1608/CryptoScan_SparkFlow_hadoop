import subprocess


def curl_request(url):
    # Define the command to execute using curl
    command = ["curl", "-s", "-o", "-", url]

    # Execute the curl command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Return the stdout of the curl command
    return result.stdout


# Make a curl request
response = curl_request("https://api.huobi.pro/market/tickers")
print(response)
