from socket import socket, getaddrinfo, AF_UNSPEC, SOCK_DGRAM, AI_PASSIVE
from sys import exc_info, version_info
from traceback import format_exc
from threading import Thread
from paths import ENGINE_PATH, NET_PATH, TEXT_EXT
import time

from engineinterface import EngineInterface

from tools import LoopCounter, getFormattedTime, OptiClock

#Protocol = EENP = EpiEngine Network Protocol

TIMEOUT = 35
TIMEOUT_MIN = 5
TIMEOUT_PACKET = 10

BASE = 256

def base256(value):
    result = ""
    
    #Negation
    negate = False
    
    if value < 0:
        negate = True
        value *= -1
        
    #Convert
    largestUnit = 1
    places = 1
    
    while largestUnit < value:
        largestUnit *= BASE
        places += 1
        
    while places > 0:
        result += chr(int(value/largestUnit))
        value -= int(value/largestUnit)*largestUnit
        
        largestUnit /= BASE
        places -= 1
        
    #Negation
    if negate:
        result = "-"+result
        
    return result
    
def base10(value):

    #Negation
    negate = False
    
    if value[0] == "-":
        negate = True
        value = value[1:]

    #Convert
    result = 0
    value = value[::-1]
    
    unit = 1
    
    for char in value:
        result += ord(char)*unit
        unit *= 256
    
    if negate:
        result *= -1
        
    return result

def byt(s):
    if version_info[0] != 2:
        return bytes(s, "UTF-8")
    else:
        return bytes(s)
    
def string(s):
    if version_info[0] != 2:
        return str(s, "UTF-8")
    else:
        return str(s)

class Packet():
    def __init__(self, data, addr, mode, headers=None):
        if headers:
            self.headers = headers
        else:
            self.headers = {}
        self.addr = addr
        self.__payload = ""
        self.__packet = ""
        
        if mode == "PACKET":
            self.__packet = string(data)
            self.__extractPayload()
            
        elif mode == "PAYLOAD":
            self.payload = self.__compressPayload(data)
            self.__makePacket()
            
    def __str__(self):
        return "Network Packet #%i - %s" % (self.headers["PACKETID"], str(self.addr))
            
    def __repr__(self):
        return "Network Packet #%i - %s" % (self.headers["PACKETID"], str(self.addr))
            
    def __compressPayload(self, data):
        try:
            result = eval(data)
            evaled = True
        except:
            evaled = False
        
        if evaled and type(result) == type({}):
            d = "{"
            
            for key in result.keys():
                if type(result[key]) != type(""):
                    d += "'%s':%s," % (str(key), str(result[key]).replace(" ", ""))
                else:
                    d += "'%s':'%s'," % (str(key), str(result[key]))
                    
            if d[len(d)-1] == ",":
                d = d[:len(d)-1]
            
            d += "}"
            return d
        else:
            return str(data)
            
    def __decompileHeaders(self):
        divider = self.__packet.index("\\")
        index = self.__packet.index("\n\n")
        
        self.headers["PROTOID"] = base10(self.__packet[0:3])
        self.headers["CONN"] = int(self.__packet[3])
        self.headers["NEEDACK"] = int(self.__packet[4])
        self.headers["DISCARD"] = int(self.__packet[5])
        self.headers["ACK"] = base10(self.__packet[6:divider])
        self.headers["PACKETID"] = base10(self.__packet[divider+1:index])
        
    def __compileHeaders(self):
        #PROTOID - CONN - ACK - NEEDACK - DISCARD - PACKETID
        if "PROTOID" in self.headers:
            return base256(self.headers["PROTOID"]) + str(self.headers["CONN"]) + str(self.headers["NEEDACK"]) + str(self.headers["DISCARD"]) + base256(self.headers["ACK"]) + "\\" + base256(self.headers["PACKETID"])
        else:
            return ""
            
    def __makePacket(self):
        self.__packet = self.__compileHeaders() + "\n\n" + self.payload
        self.__packet = self.__packet.replace("&", "&&")
    
    def __extractPayload(self):
        self.__packet = self.__packet.replace("&&", "&")
        self.__decompileHeaders()
        self.__payload = self.__packet[self.__packet.index("\n\n")+2:]
        
    def getPacket(self):
        self.__makePacket()
        return byt(self.__packet)
    
    def getPayload(self):
        self.__extractPayload()
        return self.__payload
    
    def length(self):
        return len(self.getPacket())
    
class MultiPacket():
    def __init__(self, addr):
        self.packets = []
        self.addr = addr
        self.ids = []
        
    def addPacket(self, packet):
        self.packets.append(packet)
        self.ids.append(packet.headers["PACKETID"])
    
    def getPacket(self):
        combined = byt("")
        
        for packet in self.packets:
            combined += byt("&") + packet.getPacket()
            
        return combined[1:]

    def length(self):
        return len(self.getPacket())
    
class SubSocket():
    
    def __init__(self, master, addr):
        self.master = master
        self.addr = addr
        self.rq = []
        self.lastreceived = -1
        
        self.__packetIDIn = -1
        self.receivedIDs = []
        
        self.userProps = {"confirmed":False, "synced":False, "player":None}#FIXME
        self.disconnectFunc = None
        
        self.master.pr("New client object created for %s." % (str(addr)))
    
    def __str__(self):
        return "Client Socket %s" % str(self.addr)
    
    def __repr__(self):
        return "Client Socket %s" % str(self.addr)
    
    def send(self, payload, mode):
        packet = Packet(payload, self.addr, "PAYLOAD")
        
        self.master.send(packet, mode)
    
    def recv(self):
        if self.rq:
            msg = self.rq[0]
            self.rq = self.rq[1:]
            return msg
        return None
    
    def disconnect(self):
        self.master.pr("Sending disconnect.")
        self.master.send(Packet("", self.addr, "DISCONN"))
        
    def pushRecv(self, packet):
        self.rq.append(packet)
        
    def getInPacketID(self):
        return self.__packetIDIn
    
    def setInPacketID(self, packetID):
        self.__packetIDIn = packetID

class NetCore():
    def __init__(self):
        
        #Socket
        self.__s = None
        
        #Queues
        self.__sq = []
        self.__rq = []
        
        #Incremental IDs
        self.__packetIDOut = -1
        
        #Clients
        self.clients = []
        
        #Acknowledgements
        self.__requiredAcks = {}
        
        #Shutdown
        self.killThread = False
        self.killQueue = []
        
        #Logging
        self.NAME = ""
        self.DEBUG = False
        self.VERBOSE = False
        self.DATADUMP = False
        
        #Network
        self.BUFFER = 1024
        self.HOST = "0.0.0.0"
        self.PORT = 7777
        
        #Config
        self.PROTO = ""
        self.DUPLEX = True
        self.FORCESEND = False
        self.FORCERECV = False
        
        #Blocking/Timeout
        self.BLOCK = 0
        self.TIMEOUT = 0.001
        
        #FIXME REMOVE FOR RE-USE
        self.eI = EngineInterface()
        self.pingcount = 1
        
        self.pr("Started NetCore.")
        
    def configure(self, name, value):
        '''Changes a configuration property of the NetCore.'''
        if type(name) == type("") and hasattr(self, name):
            setattr(self, name, value)
            self.pr("%s configured to %s." % (name, str(value)))
            return True
        
        self.pr("Configuration failed.")
        return False
        
    def setProtocol(self, proto):
        '''Sets the protocol used to a particular protocol.'''
        self.pr("Setting protocol...")
        if type(proto) == type(""):
            if proto.lower() == "udp":
                self.PROTO = SOCK_DGRAM
                self.pr("Protocol set successful.")
                return True
            elif proto.lower() == "tcp":
                self.PROTO = SOCK_STREAM
                self.pr("Protocol set successful.")
                return True
        
        self.pr("Protocol set failed.")
        return False
    
    def clear(self):
        '''Resets the NetCore and shuts down the network.'''
        if self.__s:
            self.__s.close()
            
        self.__s = None
        
        self.__sq = []
        self.__rq = []
        self.clients = []
        self.__packetIDOut = -1
        self.__packetIDIn = -1
        self.__requiredAcks = {}
        self.killQueue = []
        
        self.pr("Purged system.")
        
    def destroy(self):
        '''Exits the NetCore thread.'''
        self.killThread = True
        self.pr("NetCore scheduled to be destroyed.")
    
    def initialize(self):
        '''Initializes the socket.'''
        self.__startSocket()
        self.__bind()
        self.__configSocket()
        #self.__startLoop()
    
    def pullKillQueue(self):
        '''Pulls a kill handler from the queue.'''
        if self.killQueue:
            i = self.killQueue[0]
            self.killQueue = self.killQueue[1:]
            return i
        
    def pushKillQueue(self, i):
        '''Pushs a kill callback to the queue.'''
        self.killQueue.append(i)
    
    def __removeClient(self, cli):
        '''Removes a client from the NetCore, queues it's kill callback.'''
        if cli.disconnectFunc:
            self.pushKillQueue(cli.disconnectFunc)
        self.clients.remove(cli)
    
    def __selectIPVersion(self):
        '''Gets the current IP version.'''
        for res in getaddrinfo(self.HOST, self.PORT, AF_UNSPEC, self.PROTO, 0, AI_PASSIVE):
            return res
    
    def __startSocket(self):
        '''Initializes the socket.'''
        self.pr("Initializing socket...")
        try:
            res = self.__selectIPVersion()
            self.__s = socket(res[0], res[1])
            self.pr("Socket initialized.")
            return True
        except:
            self.pr("Socket initialization failed.", True)
            return False
    
    def __bind(self):
        '''Binds the socket.'''
        if self.DUPLEX:
            try:
                self.__s.bind((self.HOST, self.PORT))
                self.pr("Bind succeeded.")
                return True
            except:
                self.pr("Bind failed.", True)
                return False
        else:
            self.pr("Bind not completed because NetCore is not set to DUPLEX.")
            return False

    def __configSocket(self):
        '''Configures the block and timeout properties of the socket.'''
        self.pr("Configuring socket...")
        self.__s.setblocking(self.BLOCK)
        self.__s.settimeout(self.TIMEOUT)
        self.pr("Socket configured.")
        
    def __startLoop(self):
        '''Starts the NetCore loop.'''
        self.pr("Starting loop...")
        t = Thread(target=self.loop, name="NetCore Loop")
        t.start()
        self.pr("Loop started.")
        
    def deconstructMultiPacket(self, packet, source):
        '''Takes apart a multi-packet to recover the original packets.'''
        packets = []
        
        lastSplit = 0
        counter = 0
        
        skip = False
        
        for char in packet:
            if not skip:
                if char == byt("&")[0] and packet[counter+1] == byt("&")[0]:
                    skip = True
                elif char == byt("&")[0] and not packet[counter+1] == byt("&")[0]:
                    packetData = packet[lastSplit:counter]
                    packets.append(Packet(packetData, source, "PACKET"))
                    
                    lastSplit = counter+1
            else:
                skip = False 
            counter += 1
            
                
        packets.append(Packet(packet[lastSplit:], source, "PACKET"))
        
        return packets
        
    def removeUsedPackets(self, mP):
        '''Clears out any queued packets used to make a multipacket.'''
        for ID in mP.ids:
            counter = 0
            while counter < len(self.__sq):
                if self.__sq[counter].headers["PACKETID"] == ID:
                    self.__sq = self.__sq[:counter] + self.__sq[counter+1:]
                    break
                counter += 1
        
    def __recv(self):
        '''Socket level receipt of data.'''
        try:
            packet, source = self.__s.recvfrom(self.BUFFER)
            self.pr("Packet received from %s." % (str(source)))
            self.pr("Packet recv contents: "+str(packet), v=True)
            self.pr("Packet received size %i." % (len(packet)), v=True)
            packets = self.deconstructMultiPacket(packet, source)
            return packets
        except:
            #self.pr("Packet receive failed, Error: %s" % (format_exc()), v=True)
            return None
        
    def __send(self, packet):
        '''Socket level transmission of data.'''
        try:
            self.__s.sendto(packet.getPacket(), packet.addr)
            self.pr("Packet #%i sent to %s." % (packet.packets[0].headers["PACKETID"], str(packet.addr)))
            self.pr("Packet sent size %i." % (len(packet.getPacket())), v=True)
            self.pr((("Packet #%i sent contents: "% (packet.packets[0].headers["PACKETID"])) +str(packet.getPacket())) , v=True)
            return True
        except:
            self.pr("Packet #%i failed to send. Error: %s" % (packet.packets[0].headers["PACKETID"], str(format_exc())), v=True)
            return False
        
    def loop(self):
        '''The main loop of the NetCore.'''
        
        #SEND
        while len(self.__sq) > 0:
            #Combine packets together
            mP = None
            
            if self.__sq[0].length() < self.BUFFER:
                destination = self.__sq[0].addr
                key = 0
                mP = MultiPacket(self.__sq[0].addr)
                mP.addPacket(self.__sq[0])
                
                for packet in self.__sq:
                    if key != 0 and packet.addr == destination:
                        if mP.length() + packet.length() + 1 < self.BUFFER:
                            mP.addPacket(packet)
                    key += 1
            if mP:
                self.writeLog(mP, 1)
                self.__send(mP)
                self.removeUsedPackets(mP)
            else:
                self.__send(self.__sq[0])
                self.__sq = self.__sq[1:]
                
            if not self.FORCESEND:
                break
        
        #RECV
        if self.DUPLEX:
            while 1:
                packets = self.__recv()
                
                if packets:
                    for packet in packets:
                        self.writeLog(packet, 0)
                        self.__rq.append(packet)
                else:
                    break
                
                if not self.FORCERECV:
                    break
            
            while self.__rq:
                self.__processPacket(self.__rq[0])
                self.__rq = self.__rq[1:]
            
        #TIMEOUT
        for cli in self.clients:
            #FIXME REMOVE FOR RE-USE
            if time.time() - cli.lastreceived > TIMEOUT_MIN and cli.lastreceived != -1:
                self.eI.getGlobal("drawDisconnect")(cli.addr[0], cli.addr[1], TIMEOUT - (time.time() - cli.lastreceived))
            else:
                self.eI.getGlobal("clearDisconnect")()
            
            if time.time() - cli.lastreceived > TIMEOUT and cli.lastreceived != -1:
                self.send(Packet("", cli.addr, "PAYLOAD"), "DISCONN")
                try:
                    self.__removeClient(cli)
                except:
                    self.pr("Client could not be removed.")
                self.pr("Client %s was disconnected for inactivity." % (str(cli.addr)))
                self.eI.getGlobal("clearDisconnect")()
        
        #Acknowledgements
        for key in self.__requiredAcks.keys():
            try:
                msg = self.__requiredAcks[key]
                
                if time.time() - msg["timesent"] > TIMEOUT_PACKET:
                    del self.__requiredAcks[key]
                    packet = msg["packet"]
                    self.pr("Resending packet #%i." % key)
                    if msg["tries"] == -1:
                        self.__resend(packet)
                    elif msg["tries"] > 0:
                        self.__resend(packet, msg["tries"]-1)
                    break
            except:
                pass
                
    def __getNextPacketID(self):
        '''Gets and increments the outgoing packet ID.'''
        self.__packetIDOut += 1
        
        return self.__packetIDOut
        
    def send(self, packet, mode, ack=0):
        '''Called by SubSockets when they need to send.'''
        h = {}
        
        h["PROTOID"] = 540
        
        h["PACKETID"] = self.__getNextPacketID()
        
        if mode == "FAF":
            h["ACK"] = -1
            h["NEEDACK"] = 0
            h["CONN"] = 0
            h["DISCARD"] = 1
            
        elif mode == "RT":
            h["ACK"] = -1
            h["NEEDACK"] = 1
            h["CONN"] = 0
            h["DISCARD"] = 0
            
        elif mode == "ACK":
            h["ACK"] = ack
            h["NEEDACK"] = 0
            h["CONN"] = 0
            h["DISCARD"] = 0
            
        elif mode == "CONN":
            h["ACK"] = -1
            h["NEEDACK"] = 1
            h["CONN"] = 1
            h["DISCARD"] = 0
            
        elif mode == "DISCONN":
            h["ACK"] = -1
            h["NEEDACK"] = 2
            h["CONN"] = 2
            h["DISCARD"] = 0
            
        packet.headers = h
        
        if h["NEEDACK"] == 1:
            self.__requiredAcks[h["PACKETID"]] = {"packet":packet, "timesent":time.time(), "tries":-1}
        elif h["NEEDACK"] == 2:
            self.__requiredAcks[h["PACKETID"]] = {"packet":packet, "timesent":time.time(), "tries":3}
        
        self.__sq.append(packet)
        
    def __resend(self, packet, tries=-1):
        '''Queues a packet for retransmission.'''
        packet.headers["PACKETID"] = self.__getNextPacketID()
        
        self.__requiredAcks[packet.headers["PACKETID"]] = {"packet":packet, "timesent":time.time(), "tries":tries}
        
        self.__sq.append(packet)
    
    def __sendAcknowledgement(self, addr, packetID):
         if self.__sq:
             for packet in self.__sq:
                  if packet.headers["ACK"] == -1:
                      packet.headers["ACK"] = packetID
                      break
         else:
             self.send(Packet("", addr, "PAYLOAD"), "ACK", packetID)
    
    def __processPacket(self, packet):
        '''Handles a received packet.'''
        h = packet.headers
        
        self.pr("Processing packet...", v=True)
        if "PROTOID" in h:
            self.pr("Packet headers are intact.", v=True)
            if h["PROTOID"] == 540:
                self.pr("Protocol is correct.", v=True)
                
                #Check if this packet comes from a pre-existing client
                done = False
                for cli in self.clients:
                    if cli.addr == packet.addr:
                        cli.lastreceived = time.time()
                        done = True
                        break
                        
                if not done or ((h["PACKETID"] > cli.getInPacketID() or not h["DISCARD"]) and not h["PACKETID"] in cli.receivedIDs):
                    self.pr("Packet #%i is in order and is not a duplicate." % (h["PACKETID"]), v=True)
                    
                    #Client only stream security
                    if done:
                        if h["PACKETID"] > cli.getInPacketID():
                            cli.setInPacketID(h["PACKETID"])
                            
                        cli.receivedIDs.append(h["PACKETID"])
                    
                    #Acknowledge sendback
                    if h["NEEDACK"]:
                        self.pr("Packet #%i being acknowledged." % (h["PACKETID"]))
                        self.__sendAcknowledgement(packet.addr, h["PACKETID"])
                           
                    #Check for onboard acks
                    if h["ACK"] != -1:
                        self.pr("Packet #%i is carrying an acknowledgement." % h["PACKETID"], v=True)
                        if h["ACK"] in self.__requiredAcks.keys():
                            #Connection ack
                            if self.__requiredAcks[h["ACK"]]["packet"].headers["CONN"] == 1:
                                self.pr("Connection to %s acknowledged." % (str(packet.addr)))
                            #Disconnection ack
                            elif self.__requiredAcks[h["ACK"]]["packet"].headers["CONN"] == 2:
                                self.pr("Disconnection from %s acknowledged." % (str(packet.addr)))
                            #General acks
                            else:
                                entry = self.__requiredAcks[h["ACK"]]
                                
                                #FIXME Remove for reuse
                                if self.pingcount:
                                    self.eI.getGlobal("drawPing")(packet.addr[0], packet.addr[1], (time.time() - entry["timesent"])*1000)
                                else:
                                    self.eI.getGlobal("clearPing")()
                
                                del self.__requiredAcks[h["ACK"]]
                                self.pr("Packet #%i acknowledged on #%i accepted." % (h["ACK"], h["PACKETID"]))
                    
                    #Handle other packets
                    else:
                        #Normal Packets
                        if h["CONN"] == 0:
                            self.pr("Packet #%i is normal, sending to client object." % h["PACKETID"], v=True)
                            for cli in self.clients:
                                if cli.addr == packet.addr:
                                    cli.pushRecv(packet)
                                    break
                                
                        #Connect packets
                        elif h["CONN"] == 1:
                            self.pr("Connect packet #%i received from %s." % (h["PACKETID"], str(packet.addr)))
                            alreadyExists = False
                            for cli in self.clients:
                                if cli.addr == (packet.addr[0], int(packet.getPayload())):
                                    alreadyExists = True
                                    break
                            if not alreadyExists:
                                self.clients.append(SubSocket(self, (packet.addr[0], int(packet.getPayload()))))
                        
                        #Disconnect packets
                        elif h["CONN"] == 2:
                            self.pr("Disconnect packet #%i received from %s." % (h["PACKETID"], str(packet.addr)))
                            for cli in self.clients:
                                if cli.addr == packet.addr:
                                    self.__removeClient(cli)
                else:
                    pass
                    self.pr("Packet #%i rejected for being out of order." % h["PACKETID"], v=True)
            else:
                pass
                self.pr("Packet rejected for incorrect PROTOID.")
        else:
            self.pr("Packet rejected for incorrect headers.")
            return False
        
    def connect(self, addr):
        '''Attempts to connect to a remote socket.'''
        self.pr("Connecting to %s." % (str(addr)))
        self.send(Packet(str(self.PORT), addr, "PAYLOAD"), "CONN")
        self.clients.append(SubSocket(self, addr))
        
    def writeLog(self, packet, direction):
        '''Writes statistics logging data to a file.'''
        if self.DATADUMP:
            #Open the file
            try:
                f = open(NET_PATH+"netdata_"+str(self.PORT)+"_"+self.NAME+TEXT_EXT, "a")
            except:
                f = open(NET_PATH+"netdata_"+str(self.PORT)+"_"+self.NAME+TEXT_EXT, "w")
                
            #Write the data
            if not hasattr(packet, "packets"):
                f.write("{'id':%i, 'size':%i, 'time':%.3f, 'direction':%i}\n" % (packet.headers["PACKETID"], len(packet.getPayload()), time.time(), direction))
            else:
                for packet in packet.packets:
                    f.write("{'id':%i, 'size':%i, 'time':%.3f, 'direction':%i}\n" % (packet.headers["PACKETID"], len(packet.getPayload()), time.time(), direction))
            
            #Close the file
            f.close()
        
    def pr(self, msg, err=False, v=False):
        '''Outputs to the console and/or log file.'''
        if self.DEBUG and (not v or self.VERBOSE):
            try:
                f = open(NET_PATH+"net_"+str(self.PORT)+"_"+self.NAME+TEXT_EXT, "ab")
            except:
                f = open(NET_PATH+"net_"+str(self.PORT)+"_"+self.NAME+TEXT_EXT, "wb")
                
            msg = "Net%s - %s - %s\n" % (self.NAME, getFormattedTime(), str(msg))
                
            f.write(bytes(msg, "UTF-8"))
            f.close()
            
            if 1:
                print("Net%s - %s" % (self.NAME, str(msg.replace("\n", "\\n"))))
                
            if err:
                print(exc_info())