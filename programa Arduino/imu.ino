void ler_IMU() {

  timePrev = time;                        // the previous time is stored before the actual time read
  time = millis();                        // actual time read
  elapsedTime = (time - timePrev) / 1000.0; //divide by 1000 in order to obtain seconds

  //////////////////////////////////////Gyro read/////////////////////////////////////

  Wire.beginTransmission(0x68);            //begin, Send the slave adress (in this case 68)
  Wire.write(0x43);                        //First adress of the Gyro data
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 6, true);         //We ask for just 4 registers

  Gyr_rawX = Wire.read() << 8 | Wire.read(); //Once again we shif and sum
  Gyr_rawY = Wire.read() << 8 | Wire.read();
  Gyr_rawZ = Wire.read() << 8 | Wire.read();

  /*---X---*/
  Gyr_rawX = (Gyr_rawX / 131) - (Gyr_rawXBias / 131);
  /*---Y---*/
  Gyr_rawY = (Gyr_rawY / 131) - (Gyr_rawYBias / 131);
  // Z 
  Gyr_rawZ = (Gyr_rawZ / 131) - (Gyr_rawZBias / 131);

  GyroZ = Gyr_rawZ*0.01 + GyroZAnt*0.99;
  GyroZAnt= GyroZ;
  
  /*Now we integrate the raw value in degrees per seconds in order to obtain the angle
    If you multiply degrees/seconds by seconds you obtain degrees */
  /*---X---*/
  Gyro_angle_x = Gyr_rawX * elapsedTime;  // não é a integração += , apenas para o filtro complementar
  /*---X---*/
  Gyro_angle_y = Gyr_rawY * elapsedTime;

 // Aqui sim é feito a integração com +=, veja q em cima é feito com = . Obs - Gyro_angle_x é o termo do filtro complementar, já GyroAngleX é os ângulo obtidos pela integração 
  GyroAngleX +=  Gyr_rawX * elapsedTime;
  GyroAngleY +=  Gyr_rawY * elapsedTime;
  //phi += Gyr_rawY * elapsedTime;
  
  //////////////////////////////////////Acc read/////////////////////////////////////

  Wire.beginTransmission(0x68);     //begin, Send the slave adress (in this case 68)
  Wire.write(0x3B);                 //Ask for the 0x3B register- correspond to AcX
  Wire.endTransmission(false);      //keep the transmission and next
  Wire.requestFrom(0x68, 6, true);  //We ask for next 6 registers starting withj the 3B

  Acc_rawX = (Wire.read() << 8 | Wire.read()) / 16384.0 ; //each value needs two registres
  Acc_rawY = (Wire.read() << 8 | Wire.read()) / 16384.0 ;
  Acc_rawZ = (Wire.read() << 8 | Wire.read()) / 16384.0 ;

  Acc_rawX = Acc_rawX - Acc_rawXBias ;
  Acc_rawY = Acc_rawY - Acc_rawYBias ;
  // Acc_rawZ = Acc_rawZ - Acc_rawZBias ;

  if (abs(Acc_rawX) < 0.00001) {
    if (Acc_rawX >= 0) Acc_rawX = 0.00001;
    if (Acc_rawX < 0) Acc_rawX = -0.00001;
  }
  if (abs(Acc_rawY) < 0.00001) {
    if (Acc_rawY >= 0) Acc_rawY = 0.00001;
    if (Acc_rawY < 0) Acc_rawY = -0.00001;
  }
  if (abs(Acc_rawZ) < 0.00001) {
    if (Acc_rawZ >= 0) Acc_rawZ = 0.00001;
    if (Acc_rawZ < 0) Acc_rawZ = -0.00001;
  }

  // QUando os valores do Accel eram 0 travou o programa
  //Serial.println("Rodando");
  //Acc_rawX=0;
  //Acc_rawY=0;
  //Acc_rawZ=0;

  Acc_angle_x = (atan((Acc_rawY) / sqrt(pow((Acc_rawX), 2) + pow((Acc_rawZ), 2))) * rad_to_deg) ;
  Acc_angle_y = (atan(-1 * (Acc_rawX) / sqrt(pow((Acc_rawY), 2) + pow((Acc_rawZ), 2))) * rad_to_deg) ;

    

  ///////////////////////   Complementary Filter  ///////////////////////
  /*---X axis angle---*/
  Total_angle_x = alfa * (Total_angle_x + Gyro_angle_x) + alfa_1 * Acc_angle_x ;
  Total_angle_y = alfa * (Total_angle_y + Gyro_angle_y) + alfa_1 * Acc_angle_y ;






  // Gerar resultados do filtro complementar, comparação.
 // Serial.print(GyroAngleX);
 // Serial.print(",");
 // Serial.print(Acc_angle_x);
 // Serial.print(",");
 // Serial.println(Total_angle_x);
    
  // Obter a velocidade em rad
  ThetaX = (double) (Total_angle_x * PI / 180.0) ;
  ThetaY = (double) (Total_angle_y * PI / 180.0) ;


  ThetaXp = (-Gyr_rawX) * PI / 180; //(erroX-erroXAnt)/elapsedTime    ;// (-Gyr_rawX)*PI/180;
  ThetaYp = (-Gyr_rawY) * PI / 180; //(erroY-erroYAnt)/elapsedTime    ;// (-Gyr_rawY)*PI/180;
  //erroXAnt = erroX;
  //erroYAnt = erroY;

  // Filtro do Gyro
  ThetaXp = ThetaXp * 0.1 + ThetaXpAnt * 0.9; // Funcionando bem com 0,9 
  ThetaYp = ThetaYp * 0.1 + ThetaYpAnt * 0.9;
  ThetaXpAnt = ThetaXp;
  ThetaYpAnt = ThetaYp;

 


}
