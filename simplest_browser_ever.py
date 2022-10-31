
from queue import Empty
import socket
import re
#TODO SEPARATE CONNECTING TO HOST FROM SENDING A REQUEST
#1. CONNECT TO HOST
#2. SEND REQUEST
#3. RECEIVE RESPONSE
#4. PROCESS RESPONSE
#5. SHOW WEBSITE IN CODE
#6. SHOW WEBSITE AS TEXT
#7. SHOW LINKS
#8. SELECT LINK
#9. FOLLOW LINK 
#   -> IF LEAVING CURRENT DOMAIN CLOSE CONNECTION AND START FROM 1
#   -> IF STAYING ON CURRENT DOMAIN START FROM 2



#creates a simple cli browser that connects to specific server 
#and port to read get a file and returns it as text
def browse(domain_name, port=80, filepath=None):
    filepath = 'index.html' if filepath is None else filepath
    filepath = '/'+filepath if filepath[0] != '/' else filepath
    print('Setting up a socket...')
    #create connection socket for comunication
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'Connecting to {domain_name}:{port}...')
    response = '' 
    try:
        #tell socket to try to connect socket to specific domain at port
        mysock.connect((domain_name, port))
        print(f'Connection established!')
        #generate a GET request that will sent to the server
        #along with the http standard
        print(f'Sending GET request for file {domain_name}{filepath}')
        cmd = f'GET http://{domain_name}{filepath} HTTP/1.0\r\n\r\n'.encode()
        mysock.send(cmd)
        
        while True:
            data = mysock.recv(9999)
            response+=(data.decode())
            if len(data) < 1:
                break
        #print(response)
        print('Data received.')
        mysock.close()
    except TimeoutError:
        print(f'Connection to {domain_name} timed out')
    except socket.gaierror:
        print(f'Resolution error, please check your connection...')
    return response

#in reasponse split connection infromation from the actual file    
def process_response(response, verbose=False):
    if response and response is not Empty:
        print('Processing response...')
        #Split response into reply header and html body
        parts=response.split(sep='\r\n\r\n')
        (header,*file) = parts 
        body = file if not verbose else response
        return body
    
def show_website(html_source):
    try:
        html_lines = [line for line in html_source[0].split(sep='\n')]
        for index, html_line in enumerate(html_lines):
            print(f'{index}. {html_line}')  
    except TypeError:
        print("Wrong type")
    return html_source[0].lower()

def show_links(html):
    #find patterns of <a ** href="http://">LINK</a>
    #unpack to links = [(link, name)] 
    #use regular expressions to find all links
    print('Detected links...')
    #to lower case
    links = re.findall(r'<a.*href="(.*)">(.*)</a>', html)
    urls = [url for url, _ in links]
    #show numbered urls and names
    for index, link in enumerate(links):
        url, name = link
        print(f'{index}. {name} -> ({url})')
    return urls

def select_url(i, urls):
    url = urls[i]
    return url

def follow_link(link):
    #split link into https, domain, path
    parts = link.split('//')
    link_core = parts[-1]
    domain, path = link_core.split('/', 1)
    print(f'Following link {link}')
    print(f'Detected domain: {domain}')
    print(f'Detected file: {path}')
    return browse(domain_name=domain, filepath=path)
    
def start_browser(link):
    resp = follow_link(link)
    html = process_response(resp)
    html = show_website(html)
    urls = show_links(html)
    #url = select_url(int(input("Provide link number: ")), urls)
    #start_browser(url)
    
start_browser('google.com/index.html')   
