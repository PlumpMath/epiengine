#EENP Protocol specification#  
  
##Preamble##  
  
	Title:      EENP Protocol Specification  
	Author: 	Asper Arctos  
	Version: 	1.1  
	Date: 	    21/12/2014  
  
##Introduction##  
  
    This document hopes to explain the specifics of the EENP (EpiEngine Network Protocol).  

##Contents##  
  
    Preamble  
    Introduction  
    Contents  
	Packet Structure  
	Headers  
	Contents  
	Chaining  
	Base256  
  
##Packet Structure##  
  
	EENP packets consist of a packet header of a non-standard length followed by a body. There is no terminating character or anything else, just the end of the transmission.  
  
##Headers##  
  
	The packet headers are written at the start of each packet. They are formatted as follows:  
		PROTOID (2 bytes, Base256)  
		CONN (1 byte, Integer)  
		NEEDACK (1 byte, Integer)  
		DISCARD (1 byte, Integer)  
		ACK (Variable length, Base256)  
		Seperator (2 bytes, '\\')  
		PACKETID (Variable length, Base256)  
		Terminator (2 bytes, '\n\n')  
	PROTOID  
		The protocol ID, used to verify this is an EENP packet. This field is two bytes long and always contains the number 540 in Base256.  
	CONN  
		This byte is either 0, 1 or 2. If the byte is 0 it is ignored. If it is 1 this is treated as a connection request packet. If this is byte is 2 it is treated as a disconnection request packet.  
	NEEDACK  
		This byte is either 0 or 1. If it is 0 it is ignored. If it is 1  an acknowledgement will be sent for the packet.  
	DISCARD  
		This byte is either 0 or 1. It specifies if the packet should be discarded if it is out of order.  
	ACK  
		This contains the sequence ID of the packet that this packet is acknowledging.  
	PACKETID  
		This byte contains the sequence ID of the packet. This number increases by 1 every time a packet is sent from the originating end of the connection (i.e. there are two different sequence counters, one on each end of the connection).  
  
##Contents##  
  
	There are no requirements for the data inside the packet except that it is a series of bytes/ASCII characters.  
  
##Chaining##  
  
	EENP packets can be chained to fill up the buffer size. This is done by putting two packets back to back separated by a '&' character. Because of this, any packets sent via EENP require any '&' characters in the actual data to be delimited by replacing them with a double '&&'.  
  
##Sending modes##  
  
	EENP supports two basic transmission modes. Reliable Transmission and  Fire and Forget transmission. In RT mode the packets must be acknowledged by the receiver, the sender can retransmit this packet as many times as desired. In FAF mode the packets do not have to be acknowledged.  
  
##Connecting##  
  
	EENP connections are established by sending a packet with the CONN header set to 1. These packets should be acknowledged using a normal acknowledgement with the CONN header set to 1.  
  
##Disconnecting##  
  
	EENP disconnections are done by sending a packet with the CONN header set to 2. A unit that receives this should acknowledge it with a normal acknowledgement with the CONN header set to 2.  
  
##Stream Security##  
  
	Packets in EENP will be rejected if they are out of order (i.e. they have a packet ID lower than the packet ID of the last packet received) unless they have the DISCARD header set to 1.   

##Base256##  
  
	EENP PacketIDs and the protocol ID are encoded as Base256 numbers. This is done using ASCII characters instead of digits using their ASCII table assignment. Each character corresponds to the number of it's ASCII table position. These numbers are otherwise written in normal notation (1st place is 1's, 2nd place is 256's etc.).