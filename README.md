# VHOSTbusters
Bustin' Virtual Hosts

This is a Python script that helps identify whether an IP address is associated with a target domain, especially when the domain is behind a firewall or Content Delivery Network (CDN).

## How It Works

This script checks whether a given domain is reachable from a list of IP addresses. It verifies whether the IP address is linked to the target domain by examining the responses. This can be valuable for identifying the true origin of a domain that may be obscured by firewall or CDN services.

## Usage

1. **Clone or Download:** Download or clone the repository to your local machine.

2. **Install Dependencies:** Ensure you have the necessary dependencies installed, including Python 3.x, pycurl and BeautifulSoup  
```shell
pip install pycurl beautifulsoup4
```

3. **Create IP List:** Prepare a text file containing a list of IP addresses you want to check. Each IP address should be on a separate line.

4. **Run the Script:** Execute the script with the following command:

```shell
python vhostbusters.py <domain> <ip_list_file>
```

## Note
This script is most effective for domains hosted under virtual hosts.

It is intended to provide insights into the origin of a domain and can be especially useful for identifying the true IP address when the domain is shielded by a firewall or CDN.
