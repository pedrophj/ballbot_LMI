import math
import time
from threading import Thread
import csv
import tela_support

class ObjectTracking(Thread):
    def __init__(self):
        Thread.__init__(self)
    def registrarParaNotificacao(self,bluetooth,webcam,lbObjectTrackiingDist, lbObjectTrackiingX, lbOrientacao2):
        self.bluetooth = bluetooth
        self.webcam = webcam
        self.lbObjectTrackiingDist = lbObjectTrackiingDist
        self.lbObjectTrackiingX = lbObjectTrackiingX
        self.lbOrientacao = lbOrientacao2
        self.ligado = False
        self.saida=0
        self.saidaAnt=0
        self.dados = []
        self.tempo = []
        self.posX=0
        self.refX = 160 # Referencia em pixel (sempre metade da tela). Ver a linha que fiz o resize da WebCam.py
        self.refD = 50
        self.seg = 0
        self.segAnt = 0
        self.avancar=0
        self.distancia = 0
        self.distanciaAnt = 0

    def run(self):
        while True:
            time.sleep(0.002)
            while self.ligado == True:
                time.sleep(0.002)
                #try:
                ###################
                self.posX= float(self.webcam.objectTrackX)
                if int(self.webcam.objectTrackX)!=-1:

                    #tempoAtual = time.localtime().tm_hour*60*60 + time.localtime().tm_min*60 + time.localtime().tm_sec
                    # Ocorria umerro de plotar varios milisegundos iguais, então esse IF é para evitar duplicidade na medição
                    #if tempoAtual != self.segAnt:

                    self.saida= (self.posX-self.refX)*float( tela_support.varKg.get() )

                    self.distancia = (-0.001 * (self.webcam.objectTrackSize ** 3)) + ( 0.171 * (self.webcam.objectTrackSize ** 2)) + (-9.298 * self.webcam.objectTrackSize) + 201

                    # Filtro da distância
                    self.distancia =  self.distancia*0.2 + self.distanciaAnt*0.8
                    self.distanciaAnt = self.distancia


                    #if(self.webcam.objectTrackSize>26):
                    #    self.webcam.objectTrackSize=26

                    #self.distancia = (-4.8*self.webcam.objectTrackSize)+171.0

                    if self.distancia<0:
                        self.distancia=0



                    # Imprimir o valor nos Labels
                    self.lbObjectTrackiingDist['text'] = str( round(self.distancia,2) )
                    self.lbObjectTrackiingX['text'] = str( round(self.webcam.objectTrackX,2))

                    #self.saida = self.saidaAnt * 0.7 + self.saida * 0.4

                    if abs(self.saida)>0.2:
                        if(self.saida>0):
                            self.saida=0.2
                        if(self.saida<0):
                            self.saida=-0.2

                    try:
                        self.saida=round(self.saida,4)
                        if(abs(self.saida)>0.001):
                            self.bluetooth.sock.send("r"+str(self.saida)+"\n")
                            print("Girando")
                            time.sleep(0.1)
                    except:
                        pass
                    #print(self.saida)

                    # Se tiver centralizado parar o robô (Proximo a 10 pixels do centro) entõa permite mover o robô...
                    if abs(self.posX - self.refX) < 10:
                        if (tela_support.cbObjectT_Dist.get() == 1):
                            self.erroDistancia = float(self.distancia) - float(self.refD)

                            # Se maior que 0 (robô está se afastando da distância desejada), se menor q 0 ele está perto.
                            if self.erroDistancia>0:
                                try:
                                    self.bluetooth.sock.send("x12\n") #Era 15 msm
                                    self.bluetooth.sock.send("y-5\n")  #
                                    print("Avançar") # Ir pra frente no sentido da câmera
                                    self.avancar=1
                                    time.sleep(0.2)
                                except:
                                    pass
                            # Senão tiver centralizado parar o robô
                            else:
                                try:
                                    self.bluetooth.sock.send("x0\n")
                                    self.bluetooth.sock.send("y0\n")
                                    time.sleep(0.1)
                                    print("Parar")
                                    self.avancar = 0
                                except:
                                    pass
                    if abs(self.posX - self.refX) > 20:
                        try:
                            self.bluetooth.sock.send("x0\n")
                            self.bluetooth.sock.send("y0\n")
                            time.sleep(0.1)
                            print("Parar")
                            self.avancar = 0
                        except:
                            pass

                            #self.dados.append('{:.2f}'.format(self.posX)+   ","  +'{:.2f}'.format(self.distancia)+   ","  +'{:.2f}'.format(self.saida)+  ","  +'{:.2f}'.format(self.avancar)+  ","  +'{:.2f}'.format(self.lbOrientacao)  ) # Array para salvar no CSV depois
                    self.dados.append('{:.2f}'.format(self.posX) + " , " + '{:.2f}'.format(self.distancia) + " , " + '{:.2f}'.format(self.saida) + "  , " + '{:.2f}'.format(self.avancar)  +" , " + str(self.lbOrientacao['text']).replace('\r', '') +" , "+ str(round(time.time() * 1000)))
                                   #  posX, Dist, Saida, Translação, orientação

                    #self.tempo.append(  str(round(time.time() * 1000))  )  # Array para salvar no CSV depois

