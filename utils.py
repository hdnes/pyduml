import sys, socket, struct, fcntl
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd = sock.fileno()
SIOCGIFADDR = 0x8915
SIOCSIFADDR = 0x8916

def iface_exists(iface):
    ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00'*14)
    try:
        res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
    except:
        sys.exit("Error: "+iface+" device not found.")
        #ip = struct.unpack('16sH2x4s8x', res)[2]
    return True

def set_ip_addr(iface, ip):
    try:
        bin_ip = socket.inet_aton(ip)
        ifreq = struct.pack('16sH2s4s8s', iface, socket.AF_INET, '\x00'*2, bin_ip, '\x00'*8)
        fcntl.ioctl(sock, SIOCSIFADDR, ifreq)
    except:
        sys.exit("Error setting " +ip+ " to " +iface+ ". Is your DJI device connected?\n")
    return True
