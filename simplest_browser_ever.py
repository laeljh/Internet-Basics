
from queue import Empty
import socket
import re


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
        print(f'Sending GET request for file {domain_name}/{filepath}')
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
        body = file[0]
        return body if not verbose else response
    
def show_website(html):
        lines = {}
        for index, html_line in enumerate(html):
            lines += {index : html_line}
            print(f'{index}. {html_line}')
        return lines    

def show_links(html):
    #find patterns of <a ** href="http://">LINK</a>
    #unpack to links = [(link, name)] 
    #use regular expressions to find all links
    print('Select a link to follow...')
    links = re.findall(r'<a.*href="(.*)">(.*)</a>', html)
    urls = [url for url, _ in links]
    #show numbered urls and names
    for index, link in enumerate(links):
        url, name = link
        print(f'{index}. {name} -> ({url})')
    return urls

def select_url(number, urls):
    url = urls[number]
    return url

def follow_link(link):
    #split link into https, domain, path
    parts = link.split('//')
    link_core = parts[-1]
    domain, path = link_core.split('/', 1)
    print(f'Following link {link}')
    print(f'Detected domain: {domain}')
    print(f'Detected file: {path}')
    browse(domain_name, filepath=path)
    
    
    



#browse(domain_name, connection_port, file_to_get)
#test_response = browse('google.com')
#test_processed_response = process_response(test_response)
some_html = "<html><body><h1>Title</h1></br><p>Paragraph</p><a href=\"https://google.com/index.html\">Home</a></body><html>"
print(some_html)
some_urls = show_links(some_html)
for url in some_urls:
    follow_link(url)
