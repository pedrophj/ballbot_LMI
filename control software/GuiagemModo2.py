import math
import time
from threading import Thread

MIN_ERRO_ANG = 10 # Era 10
MIN_ERRO_POS = 5
RAIO_WP = 10 # Era 15

TEMPOENVIO  = 0.4 # Era 0.2

class Guiagem(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.waypoints = [] # waypoints desejados
        self.ligado = False # Para iniciar a guiagem
        self.contWaypoint = 0 # Contador do waypoint atual
        self.refGuinada = 0
        self.orientacaoNorte = 0
        self.orientacaoAtual =0
        self.ang = 0
        self.dist = 0
        self.p0 = [0,0]
        self.pw = [0,0]
        self.erroPosX = 0
        self.erroPosY = 0
        self.acaoX = 0
        self.acaoY = 0

    def encerrar(self):
        self.webcam.ligado = False
        self.bluetooth.ligado = False
        self.ligado = False
        self.btnTrajetoria.configure(text='''Iniciar trajetória''')
        self.btnTrajetoria.configure(background="#339933")
        self.lbNumWaypointAtual['text'] = "FIM"
        self.webcam.gravarVideo = False
        self.webcam.pararGravacao()
        file = open("dadosa.txt", "w")
        for x in self.webcam.dados:
            file.write(x)
        file.close()
        self.webcam.ligado = True  # Voltar com a thread webcam
        self.bluetooth.ligado = True

    def registrarParaNotificacao(self,bluetooth,lbErroPosicaoBallbot,lbErroOrientacao,lbRefGuinada,lbNumWaypointAtual, lbRefVel, btnTrajetoria, webcam):
        self.bluetooth = bluetooth
        self.lbErroPosicaoBallbot = lbErroPosicaoBallbot
        self.lbErroOrientacao = lbErroOrientacao
        self.lbRefGuinada = lbRefGuinada
        self.lbNumWaypointAtual = lbNumWaypointAtual
        self.lbRefVel = lbRefVel
        self.btnTrajetoria = btnTrajetoria
        self.webcam = webcam

    def run(self):
        while True:
            time.sleep(0.1)
            while self.ligado == True:
                time.sleep(0.05)
                try:
                    #if len(self.waypoints) - 1 != self.contWaypoint:
                    i = self.contWaypoint
                    self.pw[0] = float(self.waypoints[i][0])  # waypoint X desejado
                    self.pw[1] = float(self.waypoints[i][1])  # waypoint Y desejado

                    self.erroPosX = self.pw[0] - self.p0[0]
                    self.erroPosY = self.pw[1] - self.p0[1]

                    # Distância euclidiana
                    self.dist = math.sqrt((self.pw[0] - self.p0[0]) ** 2 + (self.pw[1] - self.p0[1]) ** 2)
                    # Obter o Ângulo entre a posição atual e o próximo waypoint
                    self.ang = math.atan2((self.pw[1] - self.p0[1]), (self.pw[0] - self.p0[0]))
                    # Converter rad para graus
                    self.ang = (self.ang * 180 / math.pi) - 90  # 90 - atual para considerar que 90 será o norte

                    # Calcular a ref de orientação (considerando o norte da bússola)
                    self.refGuinada = self.orientacaoNorte + (self.ang)

                    if self.refGuinada >360:
                        self.refGuinada = self.refGuinada - 360
                    if self.refGuinada < 0:
                        self.refGuinada = 360 + self.refGuinada

                    self.lbRefGuinada['text'] = "{:.{}f}".format( self.refGuinada, 2 )
                    self.lbErroPosicaoBallbot['text'] =  str(self.erroPosX) + " , " + str(self.erroPosY)
                    self.lbErroOrientacao['text'] = "{:.{}f}".format( (self.orientacaoAtual - self.refGuinada) , 2 )
                    #print(self.orientacaoAtual)
                    #self.bluetooth.sock.send("z" + str(float(self.refGuinada)) + "\n")

                    #if abs(self.orientacaoAtual - self.refGuinada) > MIN_ERRO_ANG:
                    #    self.bluetooth.sock.send("x0\n")
                    #while abs(self.orientacaoAtual - self.refGuinada) > MIN_ERRO_ANG:
                    #self.bluetooth.sock.send("z" + str(float(self.refGuinada)) + "\n")
                        #self.bluetooth.sock.send("x0\n")
                        #time.sleep(0.2)

                    #print(self.dist)
                    # Se o erro de orientação for menor que o mínimo então andar...

                    #if abs(self.orientacaoAtual - self.refGuinada) <= MIN_ERRO_ANG:

                        #if abs(self.erroPosX) < MIN_ERRO_POS and abs(self.erroPosY) < MIN_ERRO_POS:
                    if abs(self.erroPosX) > RAIO_WP:
                        if(int(self.erroPosX)>0):
                            self.bluetooth.sock.send("x-8\n")
                            self.bluetooth.sock.send("y-8\n")
                            self.lbRefVel['text'] = "D "
                            print("D")
                            time.sleep(TEMPOENVIO)  # era 0.2
                            self.acaoX=1

                        if (int(self.erroPosX) < 0):
                            self.bluetooth.sock.send("x8\n")
                            self.bluetooth.sock.send("y8\n")
                            self.lbRefVel['text'] = "E "
                            print("E")
                            time.sleep(TEMPOENVIO)  # era 0.2
                            self.acaoX=-1

                    else:
                        #self.bluetooth.sock.send("y0\n")
                        #self.bluetooth.sock.send("x0\n")
                        #self.lbRefVel['text'] = "V"
                        #print("V")
                        #self.acaoX=0
                        time.sleep(TEMPOENVIO)  # era 0.2

                        if abs(self.erroPosY) > RAIO_WP:
                            if (int(self.erroPosY) > 0):
                                #self.bluetooth.sock.send("x14\n") # Era 16
                                self.bluetooth.sock.send("x11\n") # 12 e 5 foi reto
                                self.bluetooth.sock.send("y-5\n")
                                self.lbRefVel['text'] = "F "
                                print("F")
                                self.acaoY=1
                                time.sleep(TEMPOENVIO)  # era 0.2

                            if (int(self.erroPosY) < 0):
                                self.bluetooth.sock.send("x-7\n") # Era 10 na reta
                                self.bluetooth.sock.send("y3\n")  # Era 4 na reta
                                self.lbRefVel['text'] = "T "
                                print("T")
                                self.acaoY = -1
                                time.sleep(TEMPOENVIO)  # era 0.2
                        else:
                            self.bluetooth.sock.send("x0\n")
                            self.bluetooth.sock.send("y0\n")
                            self.lbRefVel['text'] = "P "
                            self.acaoY = 0
                            print("P")
                            time.sleep(4)  # era 0.2

                    #if abs(self.erroPosX) < MIN_ERRO_POS and abs(self.erroPosY) < MIN_ERRO_POS:
                    if abs(self.dist) <= RAIO_WP:
                        self.acaoY = 0 # Para registrar em .csv
                        # Se o contador chegar no último ponto FINALIZADO
                        if len(self.waypoints) - 1 == self.contWaypoint:
                            self.bluetooth.sock.send("x0\n")
                            self.bluetooth.sock.send("y0\n")
                            print("P")
                            time.sleep(TEMPOENVIO)  # era 0.2
                            self.acaoY = 0
                            self.bluetooth.sock.send("d0\n")
                            self.encerrar()

                        else:  # Senão incrementa e vai para o próximo ponto
                            self.contWaypoint = self.contWaypoint + 1
                            self.lbNumWaypointAtual['text'] = self.contWaypoint + 1
                            self.bluetooth.sock.send("x0\n")
                            self.bluetooth.sock.send("y0\n")
                            print("P")
                            time.sleep(3)  # era 0.2
                            self.acaoY = 0
                    time.sleep(0.01)
                except:
                    print("Erro aqui")
                    self.ligado = False
                    pass
