import socket

class SolarMax():
    def __init__(self, host: str, port: int) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #type: socket.socket
        #self.connect(host, port)
    
    def connect(self, host:str , port: int) -> None:
        try:
            self.socket.connect((host, port))
        except:
            self.socket.close()
            self.socket = None
            raise Exception("Could not connect to host: {}".format(host))
    
    def hexValue(self, i: int) -> str:
        return (hex(i)[2:]).upper()
    
    def checksum(self, text: str) -> str:
        total = 0
        for c in text:
            total += ord(c)
        crc = self.hexValue(total)
        while len(crc) < 4:
            crc = '0'+crc
        return crc
    
    def createQueryString(self, inverterIndex: int, code: str) -> str:
        # For the structure see 1.1

        # FB is hex for 251 wich is the reserved aress for an outsite host wich we are see 1.3
        srcAddress = "FB"

        # inverterIndex is the index of the inverter we want to query wich is converted to hex wich has to be 2 characters long see 1.1
        destAddress = self.hexValue(inverterIndex)
        if len(destAddress) < 2:
            destAddress = '0'+destAddress

        # this the "port" in hex wich for data query is always 100 see 1.4
        queryType = "64"

        lenght = 1 + 3 + 3 + 3 + 3 + len(code) + 1 + 4 + 1
        lenght = self.hexValue(lenght)
        preCrcString = f"{srcAddress};{destAddress};{lenght}|{queryType}:{code}|"

        # this is the checksum of the query see 1.1
        crc = self.checksum(preCrcString)
        queryString = "{" + preCrcString + crc + "}"

        return queryString

    def query(self, inverterIndex: int, code: str):
        queryString = self.createQueryString(inverterIndex, code)

        respones = self.socket.send(queryString.encode())