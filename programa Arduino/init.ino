void iniciar() {
  
  delay(2000); // Esperar a vibração do aperto do botão de reset.
  inputString.reserve(200); // Reserva espaço para a serial

  Serial.begin(115200); // baudrate 230400 bits per second
  Serial2.begin(115200);
  Serial2.println("Inicializado");
  Serial.println("Inicializado");

  // PinMode configuration
  pinMode(led, OUTPUT);
  pinMode(stp1, OUTPUT); pinMode(stp2, OUTPUT);  pinMode(stp3, OUTPUT);
  pinMode(dir1, OUTPUT); pinMode(dir2, OUTPUT);  pinMode(dir3, OUTPUT);
  pinMode(enb, OUTPUT);  digitalWrite(enb, HIGH); // desliga motores

  digitalWrite(led, HIGH);

  Wire.setClock(400000l);    //increases I2C frequency to 400kHz
  Wire.begin();                           //begin the wire comunication

  //configuraIMU();
  delay(100);
  Wire.beginTransmission(0x68);           //begin, Send the slave adress (in this case 68)
  Wire.write(0x6B);                       //make the reset (place a 0 into the 6B register)
  Wire.write(0x80);
  Wire.endTransmission(true);             //end the transmission
  delay(100);
  Wire.beginTransmission(0x68);           //begin, Send the slave adress (in this case 68)
  Wire.write(0x6B);                       //make the reset (place a 0 into the 6B register)
  Wire.write(0x00);
  Wire.endTransmission(true);             //end the transmission
  delay(100);
  Wire.beginTransmission(0x68);           //begin, Send the slave adress (in this case 68)
  Wire.write(0x6B);                       //make the reset (place a 0 into the 6B register)
  Wire.write(0x80);
  Wire.endTransmission(true);             //end the transmission
  delay(100);
  Wire.beginTransmission(0x68);           //begin, Send the slave adress (in this case 68)
  Wire.write(0x6B);                       //make the reset (place a 0 into the 6B register)
  Wire.write(0x00);
  Wire.endTransmission(true);             //end the transmission

  delay(1);
  Wire.beginTransmission(0x68);
  Wire.write(0x19);  // the config address
  Wire.write(0x01);  // 0x01 para 500 hz e 0x03 para 250 hz
  Wire.endTransmission(true);

  delay(1);
  Wire.beginTransmission(0x68);
  Wire.write(0x1A);  // the config address
  Wire.write(0x01);  // the config value
  Wire.endTransmission(true);
  
  delay(1);
  //Gyro config
  Wire.beginTransmission(0x68);           //begin, Send the slave adress (in this case 68)
  Wire.write(0x1B);                       //We want to write to the GYRO_CONFIG register (1B hex)
  Wire.write(0x00);                       //Set 250/s
  Wire.endTransmission(true);             //End the transmission with the gyro
  
  delay(1);
  //Acc config
  Wire.beginTransmission(0x68);           //Start communication with the address found during search.
  Wire.write(0x1C);                       //We want to write to the ACCEL_CONFIG register
  Wire.write(0x00);                       // 0x00=2g (16384 ) 0x08=4g (8192) 0x10=8g (4096 )
  Wire.endTransmission(true);

  delay(1);
  //FIFO
  Wire.beginTransmission(0x68);           //Start communication with the address found during search.
  Wire.write(0x6A);                       //We want to write to the ACCEL_CONFIG register
  Wire.write(0x00);                       // 0x00=2g (16384 ) 0x08=4g (8192) 0x10=8g (4096 )
  Wire.endTransmission(true);

  delay(1);
  //FIFO
  Wire.beginTransmission(0x68);           //Start communication with the address found during search.
  Wire.write(0x6A);                       //We want to write to the ACCEL_CONFIG register
  Wire.write(0x04);                       // 0x00=2g (16384 ) 0x08=4g (8192) 0x10=8g (4096 )
  Wire.endTransmission(true);

  delay(1);
  //FIFO
  Wire.beginTransmission(0x68);           //Start communication with the address found during search.
  Wire.write(0x6A);                       //We want to write to the ACCEL_CONFIG register
  Wire.write(0x40);                       // 0x00=2g (16384 ) 0x08=4g (8192) 0x10=8g (4096 )
  Wire.endTransmission(true);

  delay(1);
  //FIFO
  Wire.beginTransmission(0x68);           //Start communication with the address found during search.
  Wire.write(0x23);                       //We want to write to the ACCEL_CONFIG register
  Wire.write(0xF8);                       // 0x00=2g (16384 ) 0x08=4g (8192) 0x10=8g (4096 )
  Wire.endTransmission(true);



  
  time = millis();                        //Start counting time in milliseconds

  /*Here we calculate the acc data error before we start the loop
     I make the mean of 200 values, that should be enough*/
  if (acc_error == 0)
  {
    for (int j = 0; j <= amostras; j++)
    {
      Wire.beginTransmission(0x68);
      Wire.write(0x3B);                       //Ask for the 0x3B register- correspond to AcX
      Wire.endTransmission(false);
      Wire.requestFrom(0x68, 6, true);

      Acc_rawX = (Wire.read() << 8 | Wire.read()) / 16384.0 ; //each value needs two registres
      Acc_rawY = (Wire.read() << 8 | Wire.read()) / 16384.0 ;
      Acc_rawZ = (Wire.read() << 8 | Wire.read()) / 16384.0 ;

      Acc_rawXBias = Acc_rawXBias + Acc_rawX;
      Acc_rawYBias = Acc_rawYBias + Acc_rawY;
      Acc_rawZBias = Acc_rawZBias + Acc_rawZ;

      if (j == amostras)
      {
        Acc_rawXBias = Acc_rawXBias / amostras;
        Acc_rawYBias = Acc_rawYBias / amostras;
        Acc_rawZBias = 1 - (Acc_rawZBias / amostras);
      }
    }
  }//end of acc error calculation

  Serial.println("Bias Accel");
  Serial.println(Acc_rawXBias);
  Serial.println(Acc_rawYBias);
  Serial.println(Acc_rawZBias);

  Serial2.println("Bias Accel");
  Serial2.println(Acc_rawXBias);
  Serial2.println(Acc_rawYBias);
  Serial2.println(Acc_rawZBias);

  /*Here we calculate the gyro data error before we start the loop
     I make the mean of 200 values, that should be enough*/
  if (gyro_error == 0)
  {
    for (int i = 0; i <= amostras; i++)
    {
      Wire.beginTransmission(0x68);            //begin, Send the slave adress (in this case 68)
      Wire.write(0x43);                        //First adress of the Gyro data
      Wire.endTransmission(false);
      Wire.requestFrom(0x68, 6, true);         //We ask for just 4 registers

      Gyr_rawX = Wire.read() << 8 | Wire.read(); //Once again we shif and sum
      Gyr_rawY = Wire.read() << 8 | Wire.read();
      Gyr_rawZ = Wire.read() << 8 | Wire.read();

      Gyr_rawXBias = Gyr_rawXBias + Gyr_rawX;
      Gyr_rawYBias = Gyr_rawYBias + Gyr_rawY;
      Gyr_rawZBias = Gyr_rawZBias + Gyr_rawZ;

      if (i == amostras)
      {
        Gyr_rawXBias = Gyr_rawXBias / amostras;
        Gyr_rawYBias = Gyr_rawYBias / amostras;
        Gyr_rawZBias = Gyr_rawZBias / amostras;
      }
    }
  }//end of gyro error calculation

  Serial.println("Bias Gyro");
  Serial.println(Gyr_rawXBias);
  Serial.println(Gyr_rawYBias);
  Serial.println(Gyr_rawZBias);

  
  Serial2.println("Bias Gyro");
  Serial2.println(Gyr_rawXBias);
  Serial2.println(Gyr_rawYBias);
  

  // Iiniciarlizar a bússola
  Wire.beginTransmission(addr); //open communication with GY273
  Wire.write(0x0A); //select Status register 0A
  Wire.write(0x00); //set as required (likely always 00h)
  Wire.endTransmission();

  //Register 0x0Bh is Set/Reset Period.  Datasheet recommends setting this to 01h without explanation
  Wire.beginTransmission(addr); //open communication with GY273
  Wire.write(0x0B); //select Set/Reset period register 0B
  Wire.write(0x01); //Recommended for Set/Reset Period by datasheet
  Wire.endTransmission();

  Wire.beginTransmission(addr); //open communication with GY273
  Wire.write(0x09); //select status register 09
  Wire.write(0x95); //this is the hex value you calculated above based on your required settings
  Wire.endTransmission();

  // Valores default p/ calibração da bússola. Para atualizar bastar enviar pela serial o caractere "c" para calibrar
  mx_bias = -2785.50;
  my_bias = 564.00;
  mx_ganho = 539.50;
  my_ganho = 554.00;





  ler_IMU();
  ThetaX = (double) (Total_angle_x * PI / 180.0) ; //-offX;
  ThetaY = (double) (Total_angle_y * PI / 180.0) ; //-offY;

  Serial.println("Angulos");
  Serial.println(Total_angle_x);
  Serial.println(Total_angle_y);


  Serial2.println("Angulos");
  Serial2.println(Total_angle_x);
  Serial2.println(Total_angle_y);
  

  //Timer1.initialize(1000);
  Timer3.initialize(1000000);
  Timer4.initialize(1000000);
  Timer5.initialize(1000000);

  //Timer1.attachInterrupt(mySerialEvent);
  Timer3.attachInterrupt(callback1);
  Timer4.attachInterrupt(callback2);
  Timer5.attachInterrupt(callback3);
 
  //iniciarSDCard();
  delay(2000);

}
