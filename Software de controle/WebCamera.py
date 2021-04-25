from threading import Thread
import cv2
from tkinter import NW
import PIL.Image, PIL.ImageTk
import time


#Magenta MELHOR para NAVEGAÇÃO (MAGENTA)
#THRESHOLD_LOW = (145,65,163)
#THRESHOLD_HIGH = (186,157,255)

# MELHOR MAGENTA
#THRESHOLD_LOW = (139,80,101)
#THRESHOLD_HIGH = (255,255,255)

#Verde Chroma key USAR NO RASTREAMENTO DE OBJETO
THRESHOLD_LOW = (49,56,36)
THRESHOLD_HIGH = (74,250,255)

MIN_RADIUS = 2 # Era 2 mas pegava qqr ruido da pele
PERIODO = 0.01
RAIO = 1
RAIOW = 3
class WebCamera(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.dados = []
        self.camera = cv2.VideoCapture(0)
        self.gravarVideo = False
        self.codec = cv2.VideoWriter_fourcc(*'XVID')
        self.output = cv2.VideoWriter('videoOk.avi', self.codec, 10, (340, 240))
        self.ambienteAlterado = False
        self.caminhoTXT = ""
        self.ligado = False
        #self.url = "0/shot.jpg"
        self.matrix = None
        self.tamX = 0
        self.tamY = 0
        self.cont = 0
        self.objectTrackX=0
        self.objectTrackSize=0

    def registrarParaNotificacao(self,canvas1, canvas2, lbPosicaoBallbot, guiagem):
        self.canvas1 = canvas1
        self.canvas2 = canvas2
        self.lbPosicaoBallbot = lbPosicaoBallbot
        self.guiagem = guiagem
    def pararGravacao(self):
        self.output.release()
    def recomecarGravacao(self):
        self.codec = cv2.VideoWriter_fourcc(*'XVID')
        self.output = cv2.VideoWriter('videoOk.avi', self.codec, 10, (340, 240))
    def imprimeWaypoints(self):
        try:
            f = open(self.caminhoTXT, "r")
            for i in f:
                x = i.split(',')
                x[0] = float(x[0])
                x[1] = float(x[1])
                self.canvas2.create_oval(x[0] - RAIOW, x[1] - RAIOW, x[0] + RAIOW, x[1] + RAIOW, width=2, fill='blue')
        except:
            print("Erro no way")
            pass

    def run(self):
            while True:
                time.sleep(PERIODO)
                while self.ligado==True:
                        time.sleep(PERIODO)




                        ret, captura = self.camera.read() #Obter a captura (um frame) da camera
                        captura = cv2.resize(captura, (320, 240))


                        if ret==True:
                            # Blur image to remove noise
                            img_filter = cv2.GaussianBlur(captura.copy(), (3, 3), 0)
                            img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2HSV)
                            img_binary = cv2.inRange(img_filter.copy(), THRESHOLD_LOW, THRESHOLD_HIGH)
                            img_binary = cv2.dilate(img_binary, None, iterations=1)
                            img_contours = img_binary.copy()
                            contours = cv2.findContours(img_contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                            center = None
                            radius = 0

                        if len(contours) > 0:
                            c = max(contours, key=cv2.contourArea)
                            ((x, y), radius) = cv2.minEnclosingCircle(c)
                            M = cv2.moments(c)
                            if M["m00"] > 0:
                                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                            if radius < MIN_RADIUS:
                                center = None

                        if center != None:
                            #self.lbObjectTrackingX['text'] = str(center[0])
                            self.objectTrackX = center[0]
                            self.objectTrackSize= radius

                        #cv2.circle(captura, center, int(round(radius)), (255, 255, 255))

                        #cv2.imshow('webcam', captura)


                        if self.ambienteAlterado == True:
                            captura2 = cv2.warpPerspective(captura, self.matrix, (self.tamX, self.tamY))
                            captura2 = cv2.cvtColor(captura2, cv2.COLOR_BGR2RGB)

                            # Blur image to remove noise
                            img_filter = cv2.GaussianBlur(captura2.copy(), (3, 3), 0)
                            img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2HSV)
                            img_binary = cv2.inRange(img_filter.copy(), THRESHOLD_LOW, THRESHOLD_HIGH)
                            img_binary = cv2.dilate(img_binary, None, iterations=1)
                            img_contours = img_binary.copy()
                            contours = cv2.findContours(img_contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                            center = None
                            radius = 0

                            if len(contours) > 0:
                                c = max(contours, key=cv2.contourArea)
                                ((x, y), radius) = cv2.minEnclosingCircle(c)
                                M = cv2.moments(c)
                                if M["m00"] > 0:
                                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                                if radius < MIN_RADIUS:
                                    center = None
                            if center != None:
                                cv2.circle(captura2, center, int(round(radius)), (0, 255, 0))
                                self.canvas2.create_rectangle(0, 0, self.tamX, self.tamY, outline='white')
                                self.canvas2.create_oval(float(center[0]) - RAIO, float(center[1]) - RAIO,
                                                             float(center[0]) + RAIO, float(center[1]) + RAIO, fill="green")
                                self.lbPosicaoBallbot['text']=str(center[0])+" , "+str(center[1])
                                self.guiagem.p0 = [float(center[0]) , float(center[1]) ]

                                self.dados.append(  str(center[0]) +","+ str(center[1]) + ',' + str(round(time.time() * 1000))  +','+str(self.guiagem.acaoX)+','+str(self.guiagem.acaoY)+','+str(self.guiagem.orientacaoAtual)+"\n" )


                            #photo2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(captura2))
                            #self.canvas2.create_image(0, 0, image=photo2, anchor=NW)
                            #self.canvas2.image = photo2
                        try:
                            captura = cv2.cvtColor(captura, cv2.COLOR_BGR2RGB)
                            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(captura))
                            self.canvas1.create_image(0, 0, image=photo, anchor=NW)
                            self.canvas1.image = photo
                        except:
                            pass


                        if self.gravarVideo == True:
                            self.output.write(captura)

                        del captura
                        tecla = cv2.waitKey(3)  # Aguardar alguma tecla ESC para sair do loop
                        if tecla == 27:  # Se a tecla for ESC sair do loop
                            break








