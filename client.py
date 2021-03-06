import socket, select, string, sys, os, base64
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.schemes.abenc import abenc_waters09
from charm.core.engine.util import objectToBytes,bytesToObject
from Crypto.Cipher import AES
from Crypto import Random
from charm.core.math.pairing import hashPair as sha1

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

def encapsulate(cpkey):
    key = groupObj.random(GT)
    return key, cpabe.encrypt(pk, key, policy)

def xorString(s1,s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))     

def generateSessionKey(encaps):
    key=sha1(cpabe.decrypt(pk, cpkey, encaps.pop()))
    for encap in encaps:
        key = xorString(key,sha1(cpabe.decrypt(pk, cpkey, encap)))
    return key

#padding functions for the encryption.
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

#AES encryption functions
def encrypt(key, raw ):
    raw = pad(raw)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return base64.b64encode( iv + cipher.encrypt( raw ) ) 

def decrypt( self, enc ):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return unpad(cipher.decrypt( enc[16:] ))

def connect(server, port):
    try :
        server.connect((host, port))
        policy = server.recv(4096)
        print('Received room policy from server: {}'.format(policy))
        pk = bytesToObject(server.recv(4096), groupObj)
        cpkey = bytesToObject(server.recv(4096), groupObj)
        print('Key attributes:  {}'.format(cpkey['attributes']))
        return pk, cpkey, policy
    except :
        print 'Unable to connect'
        sys.exit()

def receiveEncapsulations() :
    #sys.stdout.write("\n\nReceived encapsulations ")
    encapsulations = []
    for i in xrange(0,int(data[7])): 
        try: 
            encapsulations.append(bytesToObject(server.recv(4096), groupObj))
            #sys.stdout.write(str(i+1) + ", ")
        except:
            print("RECEIVE ENCAP EXCEPTION ON RUN # {}, RETRYING ONCE".format(i))
            encapsulations.append(bytesToObject(server.recv(4096), groupObj))
            continue
    print('\nEncapsulations received: {}. Generating session key.'.format(len(encapsulations)-1))
    return encapsulations 

def printMessage(data):
    sender = data.split("]",1)[0] + "]"
    msg = data.split("]",1)[1]
    if sender!='[server]':
        msg = sender + "   " + decrypt(key, msg)
    sys.stdout.write(msg) 
    sys.stdout.flush()
    prompt()

#main function
if __name__ == '__main__':
    groupObj = PairingGroup('SS512')
    cpabe = abenc_waters09.CPabe09(groupObj)
    policy=''
    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(2)
    print("Chat name: (leave blank to be completely anonymous) ")
    nickName = sys.stdin.readline().strip()

    # connect to remote host 
    pk, cpkey, policy = connect(server, port) 
    print 'Connected to remote host. Uploading and downloading encapsulations'
    key, encap = encapsulate(cpkey)
    server.send(objectToBytes(encap, groupObj))
    
    key = None
    AESobj = None 

    #Start main loop
    while 1:
        socket_list = [sys.stdin, server]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        for sock in read_sockets:
            #incoming message from remote server
            if sock == server:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                elif data[:7] == "1000001": #unique tag notifying about a new client
                    encapsulations = receiveEncapsulations()
                    key = generateSessionKey(encapsulations)[-16:]
                    print('Generated session key: {}'.format(key))
                    AESobj = AES.new(key, AES.MODE_CBC, 'This is an IV456')
                    prompt()
                else :
                    printMessage(data)
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                server.send(encrypt(key, msg.encode('utf-8')))
                prompt()
