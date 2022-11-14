void entradaRampa(){

    if( (millis()-tempoRampaVel)>=100 ) {
    SetpointX+=(refX/10); // Criar a rampa com 1/10 da amplitude
    SetpointY+=(refY/10);
    tempoRampaVel=millis();

    
    if( abs(SetpointX)>=(40.0/12) ){
      if(refX>0) SetpointX= 40.0/12;
      if(refX<0) SetpointX=-40.0/12;
    }
    if( abs(SetpointY)>=(40.0/12) ){
      if(refY>0) SetpointY= 40.0/12;
      if(refY<0) SetpointY=-40.0/12;
    }
    
    if(SetpointX>0) SetpointX=0;
    if(SetpointY>0) SetpointY=0;
    
/*
      // Fazer o plato da rampa.
    if( abs(SetpointX)>=(45.0/12) ){
      if(refX>0) SetpointX= 45.0/12;
      if(refX<0) SetpointX=-45.0/12;
    }
  */
   
  }
  
  
}
void entradaDegrau() {

SetpointX=refX;
SetpointY=refY;
/*
  if (SetpointX < refX) SetpointX += 0.03;
  if (SetpointX > refX) SetpointX -= 0.03;
  if (SetpointX == refX) SetpointX = refX;

  if (SetpointY < refY) SetpointY += 0.03;
  if (SetpointY > refY) SetpointY -= 0.03;
  if (SetpointY == refY) SetpointY = refY;
*/
}

void controladorPID() {

/*
refThetaX= (velX - SetpointX)*K3  +  integralErroVelX*K4;
refThetaY= (velY - SetpointY)*K3  +  integralErroVelY*K4;

double anguloMaximo = 2*PI/180;

integralErroVelX += (velX - SetpointX)*elapsedTime;
integralErroVelY += (velY - SetpointY)*elapsedTime;


  // Saturador na saída do controlador
  if (abs(refThetaX) > anguloMaximo) {
    if (refThetaX > 0)refThetaX = anguloMaximo;
    if (refThetaX < 0)refThetaX = -anguloMaximo;
  }
  if (abs(refThetaY) > anguloMaximo) {
    if (refThetaY > 0)refThetaY = anguloMaximo;
    if (refThetaY < 0)refThetaY = -anguloMaximo;
  }


Serial.print(refThetaX);
Serial.print(" , ");
Serial.println(refThetaY);
*/



  // Erro angular
  erroX = (SetpointX-ThetaX);
  erroY = (SetpointY-ThetaY);


  
// Integral do erro de velocidade
integralErroVelX += erroX*elapsedTime;
integralErroVelY += erroY*elapsedTime;

  acelX = (erroX) * K1 + (ThetaXp) * K2 +integralErroVelX*K4;
  acelY = (erroY) * K1 + (ThetaYp) * K2 +integralErroVelY*K4;

  // Saturador na saída do controlador
  if (abs(acelX) > acelMax) {
    if (acelX > 0)acelX = acelMax;
    if (acelX < 0)acelX = -acelMax;
  }
  if (abs(acelY) > acelMax) {
    if (acelY > 0)acelY = acelMax;
    if (acelY < 0)acelY = -acelMax;
  }

  // Velocidade obtida pela integração da aceleração
  velX += acelX * elapsedTime;
  velY += acelY * elapsedTime;

    // Saturador da velocidade dos motores
  if (abs(velX) > freqMax) {
    if (velX > 0)velX = freqMax;
    if (velX < 0)velX = -freqMax;
  }
  if (abs(velY) > freqMax) {
    if (velY > 0)velY = freqMax;
    if (velY < 0)velY = -freqMax;
  }

}

void controladorLQRPos() {


  // Erro angular
  erroX = (0 - ThetaX);
  erroY = (0 - ThetaY);
  erroPosX = (posX - SetpointX);
  erroPosY = (posY - SetpointY);



if(abs(erroX)>5.0*PI/180.0){
  if(erroX>0) erroX= 5.0*PI/180.0;
  if(erroX<0) erroX=-5.0*PI/180.0;
}
if(abs(erroY)>5.0*PI/180.0){
  if(erroY>0) erroY= 5.0*PI/180.0;
  if(erroY<0) erroY=-5.0*PI/180.0;
}

    
  //Converter para centrimetro. Para ficar mais intuitivo
  // Vezes raio 0.12 daria metro, vezes 100 p/ cm então multiplicar por 12.
  // Se aplicar ref. de 5000 o erro será muito alto, saturar em um erro máximo de 30 cm.


// Erro muito grande pode provocar queda, então abaixo é feito um saturador no erro
  if(tipoEntrada==0){

    // Frente é diferente da ré, por isso saturar diferente.
    if( (erroPosX*12)>12) { 
        erroPosX=12.0/12.0;
    }
     if( (erroPosX*12)<-30) { 
        erroPosX=-30.0/12.0;
    }
    
    // Saturador de Y é igual pq é simétrico o movimento esquerda e direita
    if( abs(erroPosY*18)>20) { 
        if(erroPosY>0) erroPosY= 18.0/12.0;
        if(erroPosY<0) erroPosY=-18.0/12.0;
    } 

  //Serial.println(erroPosX*12.0);
 }


 
  //if( abs(erroPosX*12)<5 && abs(erroPosY*12)<5 ) {  K4 = 0;  } 
  //else {   K4 = 2;       }

  
//if( abs(erroPosX*12)<20  &&  abs(erroPosY*12)<20) {K4=1;Serial.println("Perto");}
  //else {K4=1.5;Serial.println("Longe");}
  
  
  // Aceleração (Saída do controlador)
  acelX = (erroX) * K1 + (ThetaXp) * K2 +  (velX) * K3  +  erroPosX* K4;
  acelY = (erroY) * K1 + (ThetaYp) * K2 +  (velY) * K3  +  erroPosY* K4;

  
  /*
    // Filtro na saída do controlador
    acelX = acelXAnt*0.5 + acelX*0.5;
    acelY = acelYAnt*0.5 + acelY*0.5;
    acelXAnt =acelX;
    acelYAnt =acelY;
  */

  // Saturador na saída do controlador
  if (abs(acelX) > acelMax) {
    if (acelX > 0)acelX = acelMax;
    if (acelX < 0)acelX = -acelMax;
  }

  if (abs(acelY) > acelMax) {
    if (acelY > 0)acelY = acelMax;
    if (acelY < 0)acelY = -acelMax;
  }

  // Velocidade obtida pela integração da aceleração
  velX += acelX * elapsedTime;
  velY += acelY * elapsedTime;


  // Posição obtida pela integração da velocidade
  posX += velX * elapsedTime;
  posY += velY * elapsedTime;


 // posX = posX*0.8+posXAnt*0.2;
 // posY = posY*0.8+posYAnt*0.2;
  //posXAnt=posX; posYAnt=posY; // Salvar as posições anteriores
     
  // Saturador da velocidade dos motores
  if (abs(velX) > freqMax) {
    if (velX > 0)velX = freqMax;
    if (velX < 0)velX = -freqMax;
  }
  if (abs(velY) > freqMax) {
    if (velY > 0)velY = freqMax;
    if (velY < 0)velY = -freqMax;
  }


}

void controladorLQRVel() {

double erroVelX=0;
double erroVelY=0;

 // Erro angular
  erroX = (0 - ThetaX);
  erroY = (0 - ThetaY);

erroVelX = velX - SetpointX;
erroVelY = velY - SetpointY;

// Se inclinar muito o erro será grande, saturar em 4 graus
 if( abs(erroX)> (4.0*PI/180.0) ) { 
      if(erroX>0) erroX= 4.0*PI/180.0;
      if(erroX<0) erroX=-4.0*PI/180.0;
  }
 if( abs(erroY)> (4.0*PI/180.0) ) { 
      if(erroY>0) erroY= 4.0*PI/180.0;
      if(erroY<0) erroY=-4.0*PI/180.0;
  }

   if ( (erroVelX*180.0/PI) >  30 )  erroVelX = 30.0*PI/180.0;
   if ( (erroVelX*180.0/PI) < -90 ) erroVelX = -90.0*PI/180.0;
   if ( (erroVelY*180.0/PI) >  90 )  erroVelY = 90.0*PI/180.0;
   if ( (erroVelY*180.0/PI) < -90 ) erroVelY = -90.0*PI/180.0;
   
  //Serial.println(erroVelX*180.0/PI);
       
  acelX = (erroX) * K1 + (ThetaXp) * K2 +  (erroVelX) * K3  +  (posX) * K4;
  acelY = (erroY) * K1 + (ThetaYp) * K2 +  (erroVelY) * K3   + (posY) * K4;

 /*
  // Filtro na saída do controlador
   acelX = acelXAnt*0.5 + acelX*0.5;
   acelY = acelYAnt*0.5 + acelY*0.5;
   acelXAnt =acelX;
   acelYAnt =acelY;
*/

  // Saturador na saída do controlador
  if (abs(acelX) > acelMax) {
    if (acelX > 0)acelX = acelMax;
    if (acelX < 0)acelX = -acelMax;
  }

  if (abs(acelY) > acelMax) {
    if (acelY > 0)acelY = acelMax;
    if (acelY < 0)acelY = -acelMax;
  }

  // Velocidade obtida pela integração da aceleração
  velX += acelX * elapsedTime;
  velY += acelY * elapsedTime;

  // Defasa demais é péssimo TIRAR
  //velX = velXAnt*0.5 + velX*0.5;
  //velY = velYAnt*0.5 + velY*0.5;
  //velXAnt=velX;  velYAnt=velY;

  // Posição obtida pela integração da velocidade
  posX += velX * elapsedTime;
  posY += velY * elapsedTime;

  // Saturador da velocidade dos motores
  if (abs(velX) > freqMax) {
    if (velX > 0)velX = freqMax;
    if (velX < 0)velX = -freqMax;
  }
  if (abs(velY) > freqMax) {
    if (velY > 0)velY = freqMax;
    if (velY < 0)velY = -freqMax;
  }


}




void controladorYawPos() {

  erroYaw = (refz - orientacao);

  // Controlador de Guinada
  if (habGuinada) {
    if ( abs(erroYaw) >= PI ) { // 3.14 =180 graus   5.23 rad == 300 graus
      if (erroYaw < -PI) {
        //if(refz>orientacao)
        erroYaw =    ( (2 * PI) + erroYaw);
      }
      if (erroYaw >= PI) {
        //if(refz>orientacao)
        erroYaw =   -1 * ( (2 * PI) - erroYaw);
      }
    }
    fz = erroYaw * 0.2; // era 0.3
    fz *= -1;

    // Saturador do Yaw em 0.2
    if (abs(fz) > 0.2) {
      if (fz > 0) fz = 0.2;
      if (fz < 0) fz = -0.2;
    }
  }

}
void controladorYawVel() {
  erroYaw = (refz - GyroZ);
  integralErroYaw += erroYaw*elapsedTime;
  
  // Controlador de Guinada
  if (habGuinada) {

    fz = erroYaw * 0.03 +  integralErroYaw* 0.02 ; // era 0.3
    fz *= -1;

    // Saturador do Yaw em 0.5
    if (abs(fz) > 0.9) {
      if (fz > 0) fz = 0.9;
      if (fz < 0) fz = -0.9;
    }
  }

}

void timekeeper() {
  // Calculate time since loop began
  float timeChange = millis() - loopStartTime;
  //Serial.println(timeChange);
  // If the required loop time has not been reached, please wait!
  if (timeChange < STD_LOOP_TIME) {
    delay(STD_LOOP_TIME - timeChange);
  }
  // Update loop timer variables
  loopStartTime = millis();
}
