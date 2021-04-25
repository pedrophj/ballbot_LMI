

void telemetria() {

  if ( (millis() - tempoTelemetria) >= 200 ) {
    tempoTelemetria=millis(); // Tirando o comentario irá imprimir a cada 200 ms
  
    if (habTelemetria == 1) {
      //lerLidar();

      /*
      if( habGuinadaLidar==1 ) {
         if( abs(refAngLidar-orientacao)<2*PI/180 )  // Se chegou perto de +/- 2 graus
               refAngLidar+=10*PI/180;  
         if(  abs(refAngLidar-refAngLidarFim)<2*PI/180) // Se chegou perto do fim em +/- 2 graus
              { habGuinadaLidar = 0; habTelemetria   = 0; }

          if(refAngLidar>360*PI/180) refAngLidar-=360*PI/180;
          if(refAngLidar<0)          refAngLidar+=360*PI/180;
          
          refz=refAngLidar;
          //Serial.print("RefLidar= ");
          //Serial.println(refAngLidar*180/PI);    
      }
      */
      Serial2.print(orientacao * 180 / PI, 1); // Enviar para o PC o valor da orientação
      Serial2.print(" , ");
      Serial2.println(distLidar);
      
      Serial.print(orientacao * 180 / PI, 1); // Enviar para o PC o valor da orientação
      Serial.print(" , ");
      Serial.println(distLidar);
      
      //Serial.print(Total_angle_x, 3); Serial.print(",");
      //Serial.print(Acc_angle_x, 3); Serial.print(",");
      //Serial.print(Acc_rawX, 3); Serial.print(",");
      //Serial.print(Acc_rawY, 3); Serial.print(",");
      //Serial.print(Acc_rawZ, 3); Serial.print(",");
      //Serial.println(Gyro_angle_x, 3); 
      

    }

    if (imprimeGanhos) {
      //Serial2.println("Ganhos");
      Serial.println(K1);
      Serial.println(K2);
      Serial.println(K3);
      Serial.println(K4);
      Serial.println(rel);
      Serial.println("----");

      Serial2.println(K1);
      Serial2.println(K2);
      Serial2.println(K3);
      Serial2.println(K4);
      Serial2.println(rel);
      Serial2.println("----");
      
      //Serial2.println("Ref Guinada");
      // Serial2.println(refz*180/PI,2);
      imprimeGanhos = false;
    }
  }

}

void imprimeRespostaNatural(){

    Serial.print(ThetaX* 180 / PI, 1);
    Serial.print(",");
    Serial.print(ThetaY* 180 / PI, 1);
    Serial.print(",");
    Serial.print(orientacao * 180 / PI, 1);
    Serial.print(","); 
    Serial.println(millis(), 1);
    
}


void debugar(int x) {
/* 
   Debugguer      Imprime
      1          Yaw, Ref e Saida do controlador    (guinada)
      2          vel.Yaw, ref, Saída do controlador (guinada)
      3          Vel.X, Vel.Y, Motores M1,M2 e M3
      4          PosX, PosY, ref X e ref Y.
      5          Vel.X, Vel.Y, ref X e ref Y.
      6          Theta, Pitch,  SP X e SP Y.
*/

  if (x == 1) {
    Serial.print(orientacao * 180 / PI, 1);
    Serial.print(",");
    Serial.print(refz * 180 / PI, 1);
    Serial.print(",");
    Serial.print(rel*fz, 3);
    Serial.print(",");
    Serial.print(rel*M1rs, 1);
    Serial.print(",");
    Serial.print(rel*M2rs, 1);
    Serial.print(",");
    Serial.println(rel*M3rs, 1);
  }
  if (x == 2) {
    Serial.print(GyroZ, 1);
    Serial.print(",");
    Serial.print(refz, 1); // refz
    Serial.print(",");
    Serial.println(fz, 1);
  }
  if (x == 3) {
    Serial.print(ThetaX * 180 / PI, 1);
    Serial.print(",");
    Serial.print(ThetaY * 180 / PI, 1);
    Serial.print(",");
    Serial.print(orientacao * 180 / PI, 1);
    Serial.print(",");
    Serial.print(posX*12,1);
    Serial.print(",");
    Serial.print(posY*12,1);
    Serial.print(",");
    Serial.print(rel*M1rs, 1);
    Serial.print(",");
    Serial.print(rel*M2rs, 1);
    Serial.print(",");
    Serial.println(rel*M3rs, 1);
  }
  if (x == 4) {
    Serial.print(posX*12,1);
    Serial.print(",");
    Serial.print(SetpointX*12,1);
    Serial.print(",");
    Serial.print(posY*12,1);
    Serial.print(",");
    Serial.print(SetpointY*12,1);
    Serial.print(",");
    double t= (double) millis()/1000.0;
    Serial.print(t,3);
    Serial.print(",");
    Serial.print(rel*M1rs, 1);
    Serial.print(",");
    Serial.print(rel*M2rs, 1);
    Serial.print(",");
    Serial.println(rel*M3rs, 1);
  }
  if (x == 5) {
     Serial.print(SetpointX*12);
     Serial.print(",");
     Serial.println(velX*12);
  }
  if (x == 6) {
    Serial.print(ThetaX * 180 / PI, 3);
    Serial.print(",");
    Serial.print(ThetaY * 180 / PI, 3);
    Serial.print(",");
    Serial.print(rel*M1rs, 1);
    Serial.print(",");
    Serial.print(rel*M2rs, 1);
    Serial.print(",");
    Serial.println(rel*M3rs, 1);
  }
  if (x == 7) {
    Serial.print(acelX , 3);
    Serial.print(",");
    Serial.println(acelY, 3);
  }
  if (x == 8) {
    Serial.println(posX*12, 3);
  }
  if (x == 9) {
    /*
    myFile.print(millis(), 1);
    myFile.print(",");
    myFile.print(ThetaX, 1);
    myFile.print(",");
    myFile.print(ThetaY, 1);
    myFile.print(",");
    myFile.print(orientacao, 1);
    myFile.print(",");
    myFile.print(posX*12,1);
    myFile.print(",");
    myFile.print(posY*12,1);
    myFile.print(",");
    myFile.print(rel*M1rs, 1);
    myFile.print(",");
    myFile.print(rel*M2rs, 1);
    myFile.print(",");
    myFile.println(rel*M3rs, 1);
    */

    if(contDebug==1){
    dados="";
    dados.concat(millis()-periodoLoop);     dados.concat(","); //1
    dados.concat(ThetaX);     dados.concat(",");  //2
    dados.concat(ThetaY);     dados.concat(",");  //3
    dados.concat(orientacao); dados.concat(","); //4 
    dados.concat(posX);       dados.concat(","); //5
    dados.concat(posY);       dados.concat(","); //6 
    dados.concat(velX);       dados.concat(","); //7
    dados.concat(velY);       dados.concat(","); //8
    dados.concat(fz);         dados.concat(","); //9
    dados.concat(SetpointX);       dados.concat(","); //10
    dados.concat(SetpointY);        //11 SetpointX ou AcelX
    dados.concat("\n"); //10 
    //myFile.println(dados);
    periodoLoop=millis();

    
      Serial.println(dados);
    }
    if(contDebug>=2) contDebug=0;
    contDebug++;
    
    
    
    
  }

}
