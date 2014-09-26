import socket, select, string, sys, os
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.schemes.abenc import abenc_waters09
from charm.core.engine.util import objectToBytes,bytesToObject



def prompt(msg=None) :
    if msg:
        sys.stdout.write(msg)
    else:
        sys.stdout.write('<You> ')
    sys.stdout.flush()


def encapsulate(cpkey):
    #can only encrypt group members, so sym key will be the hash of a group element.
    key = groupObj.random(GT)
    print('Random group object  {} \n Policy: {}'.format(key, policy))
    return key, cpabe.encrypt(pk, key, policy)


#main function
if __name__ == '__main__':
    groupObj = PairingGroup('SS512')

    cpabe = abenc_waters09.CPabe09(groupObj)
    #While testing clients create their own keys.
    attr_dict = {'Anders': ['THREE', 'ONE', 'TWO'], 'Alice': ['THREE', 'TWO', 'FOUR'], 'Bob': ['ONE', 'THREE', 'FIVE']}
    (msk, pk) = cpabe.setup()
    policy=''

    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    prompt("Who are You?: ")
    nickName = sys.stdin.readline().strip()
    cpkey = cpabe.keygen(pk, msk, attr_dict[nickName])

    #modes: 1 - key exchange, 2 - chat
    mode = 1


    # connect to remote host
    try :
        s.connect((host, port))
        policy = s.recv(4096)
        print('Received policy: {}'.format(policy))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Uploading and downloading encapsulations'
    key, encap = encapsulate(cpkey)
    s.send(objectToBytes(encap, groupObj))
    print('Encaplsulation sent: {}'.format(encap))
    encapsulations = bytesToObject(s.recv(4096), groupObj)
    print('Encapsulations received: {}'.format(encapsulations))



    mode=2
    print 'Connected to remote host. Chat initialized'
    prompt()

    while 1 and mode==2:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()





