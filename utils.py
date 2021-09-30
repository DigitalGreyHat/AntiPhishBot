#imports
import requests

def check_if_red(url):
    #Make a request to the Google Safe Browsing API and validate it!
    resp = requests.get('https://www.google.com/transparencyreport/api/v3/safebrowsing/status?site={}'.format(url)).text
    if 'sb.ssr",6' in resp or 'sb.ssr",4' in resp or 'sb.ssr",1' in resp:
        return False; #URL is not in database or not a phishing page
    elif 'sb.ssr",2' in resp:
        return True; #URL is a phishing page
    else:
        print("Something with the request went wrong");
