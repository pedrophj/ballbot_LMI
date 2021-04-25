import cv2


# Limiares obtidos para o magenta
THRESHOLD_LOW = (140,87,0);
THRESHOLD_HIGH = (163,255,255);

# Raio mínimo para detectar
MIN_RADIUS = 2
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

# Iniciar a câmera 0
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_BUFFERSIZE, 1);
# Loop infinito
while True:


    # Obter a imagem da câmera
    ret_val, img = cam.read()


    # Blur image para remover ruído da imagem
    img_filter = cv2.GaussianBlur(img.copy(), (3, 3), 0)

    # Converte BGR para HSV
    img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2HSV)

    # Ajustar pixels para brancos de está no range, e os demais serão pixels pretos
    img_binary = cv2.inRange(img_filter.copy(), THRESHOLD_LOW, THRESHOLD_HIGH)

    img_binary = cv2.dilate(img_binary, None, iterations = 1)

    # Encontrar o centro da imagem
    # http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
    img_contours = img_binary.copy()
    contours = cv2.findContours(img_contours, cv2.RETR_EXTERNAL, \
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    # Encontrar o maior contor
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

    # Desenhar um circulo verde para mostrar que o objeto foi detectado
    #if center != None:
    #    cv2.circle(img, center, int(round(radius)), (255, 255, 255))



    # Plotar no console os valores da posição do circulo
    #print("PosX= "+str(x) + " pixels")
    #print("PosY= "+str(y) + " pixels")
    # Mostrar a imagem novo com o circulo verde detectado
    cv2.imshow('webcam', img)
    output.write(img)

    tecla=cv2.waitKey(3) # Aguardar alguma tecla ESC para sair do loop
    if tecla==27:    # Se a tecla for ESC sair do loop
        break