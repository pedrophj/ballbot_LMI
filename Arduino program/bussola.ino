
void leituraBussola() {

  ///////////// Leitura do bussola /////////////
  Wire.beginTransmission(addr); //Open a channel to the QMC5883L
  Wire.write(0x00); //select register 0, which is the X-axis MSB register
  Wire.endTransmission();
  Wire.requestFrom(addr, 6); //Read data from each axis, 2 registers per axis, 6 bytes in total
  while (Wire.available())
  {
    //Get X-Axis value
    LSBnum = Wire.read() ; //X-axis LSB byte
    MSBnum = Wire.read() ; //X-axis MSB byte
    Xaxis = (MSBnum << 8) + (LSBnum) ;
    //Serial.print("x val: "); Serial.println(Xaxis);

    //Get Y-Axis value
    LSBnum = Wire.read() ; //Y-axis LSB byte
    MSBnum = Wire.read() ; //Y-axis MSB byte
    Yaxis = (MSBnum << 8) + (LSBnum) ;
    // Serial.print("y val: "); Serial.println(Yaxis);

    //Get Z-Axis value
    LSBnum = Wire.read() ; //Z-axis LSB byte
    MSBnum = Wire.read() ; //Z-axis MSB byte
    Zaxis = (MSBnum << 8) + (LSBnum) ;
    //Serial.print("z val: "); Serial.println(Zaxis);


    // Valores Corrigidos
    magx = (Xaxis - mx_bias) * 100 / mx_ganho;   magy = (Yaxis - my_bias) * 100 / my_ganho;
    orientacao = atan2(-magy, -magx);
    orientacao +=  (-22.6) * PI / 180;

    // Apagar para testar mais que 360 graus

    // Para nao aumentar o ângulo, manter de 0 a 360 graus (até 2*PI)
    if (orientacao < 0) orientacao += 2 * PI;
    if (orientacao > 2 * PI) orientacao -= 2 * PI;

    orientacao = 2 * PI - orientacao;

    // Se mudar bruscamente o ângulo, exemplo 0 a 360, ignorar o filtro, pois a a defasagem causava problemas.
    if (  (abs(orientacaoAnt - orientacao) * 180 / PI) < 30) {
      orientacao = orientacao * 0.01 + orientacaoAnt * 0.99; // Média dos últimos dois valores era 0.05
    }
    orientacaoAnt = orientacao;

  }

  ///////////////////////////////////////////////////////////

}


void calibrarBussola() {

  Wire.beginTransmission(addr); //open communication with GY273
  Wire.write(0x0A); //select Status register 0A
  Wire.write(0x00); //set as required (likely always 00h)
  Wire.endTransmission();


  //Register 0x0Bh is Set/Reset Period.  Datasheet recommends setting this to 01h without explanation
  Wire.beginTransmission(addr); //open communication with GY273
  Wire.write(0x0B); //select Set/Reset period register 0B
  Wire.write(0x01); //Recommended for Set/Reset Period by datasheet
  Wire.endTransmission();



  //Register 0x09h is the most important. The byte sets Over Sample Rate (OSR), Range(RNG), Output Data Rate (ODR) and the Mode
  //Eah setting is 2 bits and the values are as follows:
  //
  //        OSR     RNG     ODR       Mode
  //00      512     2G      10Hz      Standby
  //01      256     8G      50Hz      Continuous
  //10      128     n/a     100Hz     n/a
  //11      64      n/a     200Hz     n/a
  //
  //So, for 128 over sample, 8G range, 50Hz output rate and continuous mode
  //the binary number would be 10 01 01 01 = 95 in hex (and 149 in decimal)
  //
  //or for 256 over samplr rate, 2G range, 10Hz data rate and continuous mode
  //the binary number would be 01 00 00 01 = 41 in hex (and 65 in decimal)
  //Set register 09h to whatever hex value you calculate for your desired settings

  Wire.beginTransmission(addr); //open communication with GY273
  Wire.write(0x09); //select status register 09
  Wire.write(0x95); //this is the hex value you calculated above based on your required settings
  Wire.endTransmission();




  Serial.println("Iniciando a Calibração...");
  //Serial2.println("Iniciando a Calibração");
  leituraBussola();
  max_mx = Xaxis;
  min_mx = Xaxis;
  max_my = Yaxis;
  min_my = Yaxis;

  for (int i = 0; i < 1500; i++) {

    leituraBussola();

    magx = Xaxis;
    magy = Yaxis;
    Serial.print(magx); Serial.print(","); Serial.println(magy);
    Serial2.print(magx); Serial2.print(","); Serial2.println(magy);
    if (magx > max_mx) max_mx = magx;
    if (magx < min_mx) min_mx = magx;
    if (magy > max_my) max_my = magy;
    if (magy < min_my) min_my = magy;
    delay(10);
  }

  // Cálculo do bias
  mx_bias  = (max_mx + min_mx) / 2;
  my_bias  = (max_my + min_my) / 2;
  // Ganho de escala
  mx_ganho = (max_mx - min_mx) / 2;
  my_ganho = (max_my - min_my) / 2;


  Serial.print("mx_bias = ");  Serial.println(mx_bias);
  Serial.print("my_bias = ");  Serial.println(my_bias);
  Serial.print("mx_ganho = "); Serial.println(mx_ganho);
  Serial.print("my_ganho = "); Serial.println(my_ganho);

  //Serial2.print("mx_bias = ");  Serial2.println(mx_bias);
  //Serial2.print("my_bias = ");  Serial2.println(my_bias);
  //Serial2.print("mx_ganho = "); Serial2.println(mx_ganho);
  //Serial2.print("my_ganho = "); Serial2.println(my_ganho);
}
