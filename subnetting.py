
from sys import stdin
import math as m

class SubNetting():
    subRedes = []
    idRedes = []
    broadcastRedes = []
    mascaraRedes = []
    gatewayRedes = []
    def __init__(self,subRedes):
        for i in range(len(subRedes)):
            self.subRedes.append(subRedes[i])
        self.generarIdRedes()
        self.generarBroadcastRedes()
        self.generarMascaraRedes()
        self.generarGatewayRedes()
        self.getIdRedes()
        self.getBroadcastRedes()
        self.getMascaraRedes()
        self.getGatewayRedes()
    def generarIdRedes(self):
        for i in range(len(self.subRedes)):
            sR = self.subRedes[i]
            sR.idRed = self.sumar1(sR.idRed,sR.getBitRed(),1)
            while self.idRedRepetida(sR.idRed,i):
                sR.idRed = self.sumar1(sR.idRed,sR.getBitRed(),1)
    def generarGatewayRedes(self):
        for i in range(len(self.subRedes)):
            sR = self.subRedes[i]
            for i in range(len(sR.idRed)):
                sR.gateway.append(sR.idRed[i])
            sR.gateway = self.sumar1(sR.gateway,31,1)
        
    def getIdRedes(self):
        for i in range(len(self.subRedes)):
            self.idRedes.append(self.subRedes[i].getIdRed())
        return self.idRedes
    def generarBroadcastRedes(self):
        for i in range(len(self.subRedes)):
            sR = self.subRedes[i]
            for j in range(len(sR.idRed)):
                if sR.ispHostRed[j] == 'H':
                    sR.broadcast.append(1) 
                else:
                    sR.broadcast.append(sR.idRed[j])
    def getBroadcastRedes(self):
        for i in range(len(self.subRedes)):
            self.broadcastRedes.append(self.subRedes[i].getBroadcastRed())
        return self.broadcastRedes
    def generarMascaraRedes(self):
         for i in range(len(self.subRedes)):
            sR = self.subRedes[i]
            for j in range(0,sR.bitsMascara):
                sR.mascara.append(1)
            for k in range(sR.bitsMascara,32):
                sR.mascara.append(0)
    def getMascaraRedes(self):
        for i in range(len(self.subRedes)):
            self.mascaraRedes.append(self.subRedes[i].getMascaraRed())
        return self.mascaraRedes
    def getGatewayRedes(self):
        for i in range(len(self.subRedes)):
            self.gatewayRedes.append(self.subRedes[i].getGatewayRed())
        return self.gatewayRedes
    def idRedRepetida(self,idRed,index):
        for i in range(len(self.subRedes)):
            if i!=index:
                if self.subRedes[i].idRed == idRed:
                    return True
        return False
    
    def sumar1(self,lista,index,carry):
        if carry==0:
            return lista
        if lista[index] == 0:
            lista[index] = 1
            carry=0
        elif lista[index] == 1:
            lista[index] = 0
            self.sumar1(lista,index-1,1)
        return lista

    def __str__(self):
        Ciudades=["Chile Colombia 0","Chile brazil 1","Colombia usa 1","brazil españa 0","USA inglatera 0","España alemania 1","inglaterra alemania ","Usa España 0/1/0","Alemania suecia","Estocolmo","Berlin","Londres","Bogota","Murcia","Hounston","Satiago", "Brasilia","router","router","router","router","router","router","router","router","router","router","router","router",]
        string = ""
        for i in range(len(self.subRedes)):
            string += "Red: " + str(i+1) + '\n'
            string += "Id red: " + self.idRedes[i] + '\n'
            string += "Brodcast red: " + self.broadcastRedes[i] + '\n'
            string += "Mascara: " + self.mascaraRedes[i] + ' /'+str(self.subRedes[i].bitsMascara) + '\n'
            string += "Gateway: " + self.gatewayRedes[i] + '\n'
            string += "Numero host: " + str(self.subRedes[i].numeroHost) + '\n'
            string += "Nombre de la red "+Ciudades[i] + '\n'
            string += '\n'
        return string
            
class SubRed():
    
    B=[]
    mascaraIsp = 0;
    numeroHostD = 0;
    ispHostRed = []
    idRed = []
    brodcast = []
    mascara = []
    bitsMascara = 0;
    gateway =[]
    numeroHost = 0;
    def __init__(self,bits,mascaraIsp,numeroHostD):
        self.idRed = []
        self.broadcast = []
        self.mascara = []
        self.gateway = []
        self.B=[0 for i in range(32)]
        self.ispHostRed = ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""] 
        self.mascaraIsp = mascaraIsp
        self.numeroHostD = numeroHostD
        
        for i in range(len(bits)):
            self.pasarABinario(bits[i],i+1)
        self.dividirIspRH(self.mascaraIsp,self.numeroHostD)
        self.generarIdRed(self.idRed,self.B,self.ispHostRed)
    def pasarABinario(self,decimal,numeroByte):
            ultimo = 7
            for i in range((numeroByte-1)*8,8*numeroByte):
                    if decimal-2**ultimo>=0:
                            self.B[i] = 1
                            decimal -= 2**ultimo
                    else:
                            self.B[i] = 0
                    ultimo -=1
    def generarIdRed(self,idRed,B,ispHostRed):
        for i in range(0,32):
            if ispHostRed[i] == 'ISP' or ispHostRed[i] == 'R':
                idRed.append(B[i])
            else:
                idRed.append(0)
    def dividirIspRH(self,mascara,numerohost):
        numeroBitsH = m.ceil(m.log(numerohost,2))
        if numeroBitsH == 1:
            numeroBitsH += 1
        self.bitsMascara = 32 - numeroBitsH
        self.numeroHost = 2**numeroBitsH -2
        for i in range(0,mascara):
            self.ispHostRed[i] = 'ISP'
        for j in range(mascara,mascara+(32-numeroBitsH-mascara)):
            self.ispHostRed[j] = 'R'
        for k in range(mascara+(32-numeroBitsH-mascara),32):
            self.ispHostRed[k] = 'H'

    def getBitRed(self):
        return self.ispHostRed.index('H')-1
    def getIdRed(self):
        return self.getDecimal(self.idRed)
    def getBroadcastRed(self):
        return self.getDecimal(self.broadcast)
    def getMascaraRed(self):
        return self.getDecimal(self.mascara)
    def getGatewayRed(self):
        return self.getDecimal(self.gateway)
    def getDecimal(self,numeroBinario):
        aux=''
        acum=0
        conta=0
        potencia = 7
        for j in range(32):
            acum += (2**potencia)*numeroBinario[j]
            potencia -=1
            conta +=1
            if conta == 8:
                aux += str(acum)
                if j != 31:
                    aux += '.'
                acum =0
                conta=0
                potencia =7
        return aux



sn = SubNetting([
                 SubRed([187,24,96,0],21,1050),
                 SubRed([187,24,96,0],21,820),
                 SubRed([187,24,96,0],21,1790),
                 SubRed([187,24,96,0],21,2),
                 SubRed([187,24,96,0],21,2),
                 SubRed([187,24,96,0],21,2),
                 
                 ])
Ciudades=["Chile Colombia 0","Chile brazil 1","Colombia usa 1","brazil españa 0","USA inglatera 0","España alemania 1","inglaterra alemania ","Usa España 0/1/0","Alemania suecia","Estocolmo","Berlin","Londres","Bogota","Murcia","Hounston","Satiago", "Brasilia"]

print(sn)






    
        
