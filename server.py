import socket, select, json
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.schemes.abenc import abenc_waters09
from charm.core.engine.util import objectToBytes,bytesToObject

 
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

 


def prompt(msg) :
    sys.stdout.write(msg)
    sys.stdout.flush()
     
if __name__ == '__main__':

    groupObj = PairingGroup('SS512')

    cpabe = abenc_waters09.CPabe09(groupObj)
    (msk, pk) = cpabe.setup()
    roomPolicy = '((ONE or THREE) and (TWO or FOUR))'

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    #list of current encapsulations for the room
    encapsulations = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                sockfd.send(roomPolicy) #send the room policy
                encap = bytesToObject(sockfd.recv(RECV_BUFFER), groupObj) #receive the encapsulation
                print 'Received one encapsulation: {}'.format(encap)
                sockfd.send(objectToBytes(encapsulations, groupObj)) #send all the current encapsulations
                encapsulations.append(encap) #add the encapsulation to current list
                print "Client {} connected".format(addr)
                 
                broadcast_data(sockfd, "{} entered room\n{}".format(addr, encap))

            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        print sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)                
                 
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
