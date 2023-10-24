import sys
import pycurl
import time
import re
import argparse
import random
from io import BytesIO
from bs4 import BeautifulSoup

# List of user agents to rotate through
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61",
    "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.80 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/118.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 EdgiOS/118.2088.52 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/118.0.5993.92 Mobile/15E148 Safari/604.1",
]

# Function to pick a random user agent
def pick_random_user_agent():
    return random.choice(user_agents)


# Function to perform the HTTP request and check if the domain is in the response
def check_domain_in_response(url, host_header, user_agent):
    try:
        response = BytesIO()

        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPHEADER, [host_header, f"User-Agent: {user_agent}"])
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.CONNECTTIMEOUT, 10)
        c.setopt(pycurl.WRITEDATA, response)

        c.perform()
        response_code = c.getinfo(pycurl.RESPONSE_CODE)
        c.close()

        response_text = response.getvalue().decode("utf-8")

        domain = host_header.split("Host: ")[-1]

        if response_code == 200:
            title = get_website_title(response_text)
            return f"\r{url} - Response 200 - {title}"
        else:
            return f"\r{url} - Response {response_code}"

    # zzzzzzzzzzzzzzzzzzzzzzzzzzzzz
    except pycurl.error as e:
        if "Connection timed out" in str(e):
            return None
        elif "Connection refused" in str(e):
            return None

# Function to extract the website title from HTML
def get_website_title(html):
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    if title_tag:
        return title_tag.string.strip()
    return "No Title"


# Loading animation
def loading_animation():
    animation = "|/-\\"
    for _ in range(10):
        for char in animation:
            sys.stdout.write(f"\rSearching... {char}")
            sys.stdout.flush()
            time.sleep(0.1)


# Modify the print_match_result function
def print_match_result(ip_address, result):
    if result:
        print(f"{ip_address} - {result}")


# Modify the check_multiple_ip_addresses function
def check_multiple_ip_addresses(ip_addresses, domain, host_header):
    for ip_address in ip_addresses:
        http_url = f"http://{ip_address}"
        https_url = f"https://{ip_address}"

        user_agent = pick_random_user_agent()

        loading_animation()

        result_http = check_domain_in_response(http_url, host_header, user_agent)
        result_https = check_domain_in_response(https_url, host_header, user_agent)

        if result_http:
            print_match_result(ip_address, result_http)
        if result_https:
            print_match_result(ip_address, result_https)


# Main function
def main(domain, ip_file):
    host_header = f"Host: {domain}"

    with open(ip_file, "r") as file:
        ip_addresses = [line.strip() for line in file]
    check_multiple_ip_addresses(ip_addresses, domain, host_header)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script checks whether a given domain is reachable from a list of IP addresses. It verifies whether the IP address is linked to the target domain by examining the responses. This can be valuable for identifying the true origin of a domain that may be obscured by firewall or CDN services."
    )
    parser.add_argument("domain", help="The domain to check")
    parser.add_argument(
        "ip_file", help="A text file with a list of IP addresses to check"
    )
    args = parser.parse_args()
    main(args.domain, args.ip_file)
