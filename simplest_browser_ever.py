
from queue import Empty
import socket


#creates a simple cli browser that connects to specific server 
#and port to read get a file and returns it as text
def browse(domain_name, port=80, filepath='index.html'):
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
        cmd = f'GET http://{domain_name}/{filepath} HTTP/1.0\r\n\r\n'.encode()
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
    links = re.findall(r'href=+',html)
    print(links)



#browse(domain_name, connection_port, file_to_get)
#test_response = browse('google.com')
#test_processed_response = process_response(test_response)
some_html = "<html><body><h1>Title</h1></br><p>Paragraph</p><a href=\"index.html\">Home</a></body><html>"
#print(test_processed_response)