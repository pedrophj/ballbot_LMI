/*
  (1) Protocolo para ajustar um parâmetro

  cXXXXX

  Onde:
     c: um caracte que executa o ajuste de um parâmetro
     XXXX: valor que deseja passar para o parâmetro.

     Exemplo: q100   (será ajustado o ganho K1 com valor 100)

*************************************************

  (2) Protocolo sem parâmetro
  Exemplo: Para calibrar a bússola basta enviar 'c'

  Tabela com as funções permitidas pela Serial / Bluetooth
  ____________________________________________________
  | Caractere   |       Função                    |
  ___________________________________________________
      q            Valor de K1
      w            Valor de K2
      a            Valor de K3
      s            Valor de K4
      u            Valor de Kp (Guinada)
      i            Valor de Ki (Guinada)
      r            Controle manual da guinada
      h            Habilitar motores
      j            Desabilitar motores
      g            Habilitar Guinada
      f            Desabilitar Guinada
      c            Calibrar a bússola
      x            Referência de velocidade em X
      y            Referência de velocidade em Y
      z            Referência da guinada
      t            Começar telemetria
      p            Parar   telemetria e visualizar ganhos
      l            Visualizar ganhos
      o            rel roda / bola
      m            modo do controle de guinda 0 (posição) ou 1 (velocidade)  
      n            modo do controle do LQR, referência 0 = Velocidade e 1 = Posição  
      b            Tipo da entrada. 0 = degrau e 1=rampa  
  |_____________|_________________________________|_____

 Para posição com rampa fazer: n1, depois b1.
*/

void serialEvent() {
  if (Serial.available()) {
    // Obter um novo caractere
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;

    // Se pressionar o enter (quebra de linha) então ler a string
    if (inChar == '\n') {
      stringComplete = true;
    }

    if (stringComplete) {

      if (inputString[0] == 'q') {
        inputString = inputString.substring(1, inputString.length());
        K1 = inputString.toFloat();
      }
      if (inputString[0] == 'w') {
        inputString = inputString.substring(1, inputString.length());
        K2 = inputString.toFloat();
      }
      if (inputString[0] == 'a') {
        inputString = inputString.substring(1, inputString.length());
        K3 = inputString.toFloat();
      }
      if (inputString[0] == 's') {
        inputString = inputString.substring(1, inputString.length());
        K4 = inputString.toFloat();
      }
      if (inputString[0] == 'o') {
        inputString = inputString.substring(1, inputString.length());
        rel = inputString.toFloat();
      }
      if (inputString[0] == 'h') {
        digitalWrite(enb, LOW);
      }
      if (inputString[0] == 'j') {
        digitalWrite(enb, HIGH);  // Desabilita os motores e reduz o valor máximo do saturador velocidade dos motores em 1 rad/s
        freqMax = 1;
      }
      if (inputString[0] == 'g') {
        habGuinada = true;
      }
      if (inputString[0] == 'f') {
        habGuinada = false;
        fz = 0;
      }
      if (inputString[0] == 'd') {
        inputString = inputString.substring(1, inputString.length());
        debug = inputString.toFloat();
        if(debug==0) {//myFile.close();
          Serial.println("*Fechou SD*");}
        if(debug==9) { //myFile = SD.open("test.txt", FILE_WRITE); 
        Serial.println("*Gravando SD*");}
      }
      if (inputString[0] == 'c') {
        digitalWrite(enb, HIGH);
        Serial.println("** Calibração da Bussola **");
        delay(3000);
        calibrarBussola();
      }
      if (inputString[0] == 'm') {
        inputString = inputString.substring(1, inputString.length());
        modoGuinada = inputString.toFloat() ;
      }
      if (inputString[0] == 'n') {
        inputString = inputString.substring(1, inputString.length());
        modoVelPos = inputString.toFloat() ;
        if(modoVelPos==0) {K4 = 0;}  // Altera para controle de velocidade
        else  {K4 = 1.2; posX=0; posY=0; SetpointX=0; SetpointY=0; }; 
      }
      if (inputString[0] == 'b') {
        inputString = inputString.substring(1, inputString.length());
        tipoEntrada = inputString.toFloat() ;
      }
      if (inputString[0] == 'x') {
        
        inputString = inputString.substring(1, inputString.length());
        if(modoVelPos==0)    refX = inputString.toFloat() /12; //  Controle de Velocidade
        if(modoVelPos==1)    refX = inputString.toFloat() /12;     //  Converte em cm (Controle de posição)
        
        //refX = inputString.toFloat() *PI/180.0; 
      }
      if (inputString[0] == 'y') {
        inputString = inputString.substring(1, inputString.length());
        if(modoVelPos==0)    refY = inputString.toFloat() /12; //  Controle de Velocidade
        if(modoVelPos==1)    refY = inputString.toFloat() /12;    // Converte em cm (Controle de posição)
      }
      if (inputString[0] == 'z') {
        inputString = inputString.substring(1, inputString.length());
        if(modoGuinada==0)    refz = inputString.toFloat() * PI / 180;
        if(modoGuinada==1)    refz = inputString.toFloat() ;
      }
      if (inputString[0] == 'r') {
        inputString = inputString.substring(1, inputString.length());
        fz = inputString.toFloat();
      }
      if (inputString[0] == 'u') {
        inputString = inputString.substring(1, inputString.length());
        posX=inputString.toFloat()/12;
      }
      if (inputString[0] == 'p') {
        habTelemetria = 0;
        freqMax = 3.5; // Seta o valor máximo do saturador velocidade dos motores
        tempoPisca = millis();
        posX = 0; posY = 0;
        SetpointX=0;SetpointY=0;
        
      }
      if (inputString[0] == 't') habTelemetria  = 1;
      if (inputString[0] == 'l') {

        //zeroBussola=orientacao;
        imprimeGanhos = true;
        freqMax = 3.5; // Era 3.5 Seta o valor máximo do saturador velocidade dos motores
      }
      if (inputString[0] == 'v') { // Visão usando o LIDAR
        // Primeiro obter angulo atual para fazer varredura de 60 graus.
        // Na telemetria sera feito a medição do lidar e incrementa o refAngLidar para varrer
        
           //Serial.println((orientacao * 180 / PI));
           
                             // Orientação atual - 30
           refAngLidar =(orientacao * 180 / PI)- 30; // Em graus aqui
           
           if(refAngLidarInicio<0) refAngLidar = 360 + refAngLidar;
           refAngLidarInicio = refAngLidar; // Foi usado angulo Inicio para saber quando terminar +60

           refAngLidarFim = refAngLidarInicio+60; // Final será range de 60 graus a varredura 
           if(refAngLidarFim>360) refAngLidarFim = refAngLidarFim-360; // Se for maior q 360, subtrair
           
           Serial.println(refAngLidarInicio);
           Serial.println(refAngLidarFim);
           
           modoGuinada=0; // Manter guinada o modo de controle por posição
           
           // Atualizar a referencia de guinada rad/s
           refAngLidarFim   =refAngLidarFim*PI/180;
           refAngLidarInicio=refAngLidarInicio*PI/180;
           
           refAngLidar = refAngLidarInicio;  // Começar com o ref. Inicio
           refz=refAngLidar; // Setar a referencia no controlador
           
           habGuinada = true; // Habiltiar o controlador de guinada
           habGuinadaLidar = 1; // Começar varredura de 60 graus
           habTelemetria   = 1; // Hab. telemetria para enviar angulo e distancia
      }
      inputString = ""; // Apagar a string recebida
      stringComplete = false; // Permitir a leitura de uma nova string
    }


  }
}






void Teste_serialEvent3() {
  if (Serial2.available()) {
    // Obter um novo caractere
    char inChar = (char)Serial2.read();
    // add it to the inputString:
    inputString += inChar;

    // Se pressionar o enter (quebra de linha) então ler a string
    if (inChar == '\n') {
      stringComplete = true;
    }

    if (stringComplete) {

      if (inputString[0] == 'q') {
        inputString = inputString.substring(1, inputString.length());
        K1 = inputString.toFloat();
      }
      if (inputString[0] == 'w') {
        inputString = inputString.substring(1, inputString.length());
        K2 = inputString.toFloat();
      }
      if (inputString[0] == 'a') {
        inputString = inputString.substring(1, inputString.length());
        K3 = inputString.toFloat();
      }
      if (inputString[0] == 's') {
        inputString = inputString.substring(1, inputString.length());
        K4 = inputString.toFloat();
      }
      if (inputString[0] == 'o') {
        inputString = inputString.substring(1, inputString.length());
        rel = inputString.toFloat();
      }
      
      if (inputString[0] == 'h') {
        digitalWrite(enb, LOW);
      }
      if (inputString[0] == 'j') {
        digitalWrite(enb, HIGH);  // Desabilita os motores e reduz o valor máximo do saturador velocidade dos motores em 1 rad/s
        freqMax = 1;
      }
      if (inputString[0] == 'g') {
        habGuinada = true;
      }
      if (inputString[0] == 'f') {
        habGuinada = false;
        fz = 0;
      }
      if (inputString[0] == 'd') {
        inputString = inputString.substring(1, inputString.length());
        debug = inputString.toFloat();
        if(debug==0) {//myFile.close();
          Serial2.println("*Fechou*");}
        if(debug==9) { //myFile = SD.open("test.txt", FILE_WRITE); 
          Serial2.println("*Gravando SD*");}
        
      }
      if (inputString[0] == 'c') {
        digitalWrite(enb, HIGH);
        Serial2.println("** Calibração da Bussola **");
        delay(3000);
        calibrarBussola();
      }
      if (inputString[0] == 'm') {
        inputString = inputString.substring(1, inputString.length());
        modoGuinada = inputString.toFloat() ;
      }
      if (inputString[0] == 'n') {
        inputString = inputString.substring(1, inputString.length());
        modoVelPos = inputString.toFloat() ;
        if(modoVelPos==0) {K4 = 0;}  // Altera para controle de velocidade
        else  {K4 = 2; posX=0; posY=0; SetpointX=0; SetpointY=0; }; 
      }
      if (inputString[0] == 'b') {
        inputString = inputString.substring(1, inputString.length());
        tipoEntrada = inputString.toFloat() ;
      }
      if (inputString[0] == 'x') {
        inputString = inputString.substring(1, inputString.length());
        if(modoVelPos==0)    refX = inputString.toFloat() /12; //  Controle de Velocidade
        if(modoVelPos==1)    refX = inputString.toFloat() /12;     //  Converte em cm (Controle de posição)
        //refX = inputString.toFloat() *PI/180.0; 
      }
      if (inputString[0] == 'y') {
        inputString = inputString.substring(1, inputString.length());
        if(modoVelPos==0)    refY = inputString.toFloat() /12; //  Controle de Velocidade
        if(modoVelPos==1)    refY = inputString.toFloat() /12;    // Converte em cm (Controle de posição)
      }
      if (inputString[0] == 'z') {
        inputString = inputString.substring(1, inputString.length());
        if(modoGuinada==0)    refz = inputString.toFloat() * PI / 180;
        if(modoGuinada==1)    refz = inputString.toFloat() ;
      }
      if (inputString[0] == 'r') {
        inputString = inputString.substring(1, inputString.length());
        fz = inputString.toFloat();
      }
      if (inputString[0] == 'p') {
        habTelemetria = 0;
        freqMax = 3.5; // Seta o valor máximo do saturador velocidade dos motores
        tempoPisca = millis();
        posX = 0; posY = 0;
        SetpointX=0;SetpointY=0;
      }
      if (inputString[0] == 't') habTelemetria  = 1;
      if (inputString[0] == 'l') {

        //zeroBussola=orientacao;
        imprimeGanhos = true;
        freqMax = 3.5; // Seta o valor máximo do saturador velocidade dos motores
      }

      inputString = ""; // Apagar a string recebida
      stringComplete = false; // Permitir a leitura de uma nova string
    }


  }
}
