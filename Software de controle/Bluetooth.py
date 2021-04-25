
from threading import Thread
import bluetooth
import time
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


class Bluetooth(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.device = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.sock = self.device
        self.conectado = False 
        self.ligado = True
        self.linha=""
        self.recebido = []
        self.dados = []
        self.telemetria = False
        self.listaDevices=[]
        self.orientacaoAtual=0
        self.distLidar = 0

        # Lista com os dados recebidos pela telemetria
        self.yaw = []
        #self.pitch = []
        #self.roll = []
        self.velX = []
        self.velY = []
        self.velZ = []
        self.setpointX = []
        self.setpointY = []
        self.setpointZ = []

    def registrarParaNotificacao(self,lbOrientacao, tbdados,guiagem, lbObjectTrackiingDistLidar):
        self.lbOrientacao = lbOrientacao
        self.tbdados = tbdados
        self.guiagem = guiagem
        self.lbDistLidar = lbObjectTrackiingDistLidar

    def desconectar(self):
        self.sock.close()

    def conectar(self, dispositivo):
        try:                                      
            nearby_devices = bluetooth.discover_devices()
            endereco = nearby_devices[dispositivo]
            self.sock.connect(( endereco , 1))  
            self.conectado=True          
        except:
            self.conectado=False 
            self.sock.close()
        print(self.conectado)  

    def enviarSerial(self, texto):
        self.sock.send(texto)

    def atualizarLista(self):
        nearby_devices = bluetooth.discover_devices()
        num = 0 
        self.listaDevices = []
        for i in nearby_devices:	        
	        #print num , ": " , bluetooth.lookup_name( i ) + " - "+i
            print(bluetooth.lookup_name( i ))
            self.listaDevices.append(bluetooth.lookup_name( i ))
            num+=1

    def run(self):
        while True:
            #time.sleep(0.002)
            while self.ligado == True:
                #time.sleep(0.1)
                if self.conectado==True:  
                        data=""
                        try:
                            data = str(self.sock.recv(1),'utf-8')
                            if data == "\n":
                                if self.telemetria == True:
                                    try:
                                        # Fazer separação dos dados recebidos
                                        self.recebido = self.linha.split(',')

                                        # Guardar dados para gerar TXT depois
                                        self.dados.append(self.linha)

                                        # Notificar Guiagem
                                        #self.guiagem.orientacaoAtual = float(self.recebido[0])

                                        # Para plotar gráficos
                                        #self.pitch.append(float(self.recebido[0])  )
                                        #self.roll.append(float(self.recebido[0]))
                                        #self.yaw.append(float(self.recebido[0]))

                                        # Para os Labels
                                        #self.lbPitch['text'] = self.recebido[0]
                                        #self.lbRoll['text'] = self.recebido[1]

                                        #Antigo
                                        #self.orientacaoAtual=self.recebido[0]
                                        #self.lbOrientacao['text'] =  self.recebido[0]

                                        self.orientacaoAtual =  float(self.recebido[0])
                                        self.lbOrientacao['text'] = str(self.orientacaoAtual)


                                        self.distLidar=float(self.recebido[1])
                                        self.lbDistLidar['text'] = str(self.distLidar)
                                        

                                        #self.velX.append(float(self.recebido[3]))
                                        #self.velY.append(float(self.recebido[4]))
                                        #self.velZ.append(float(self.recebido[5]))
                                        #self.setpointX.append(float(self.recebido[6]))
                                        #self.setpointY.append(float(self.recebido[7]))
                                        #self.setpointZ.append(float(self.recebido[8]))



                                    except:
                                        pass
                                else:
                                    self.tbdados.insert(tk.END,self.linha)
                                    self.tbdados.insert(tk.END,'\n')
                                self.linha=""
                            else:
                                self.linha+=data
                        except:
                            pass
                                