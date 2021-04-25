
void converVel() {

  // Conversão das velocidades (converte velX e velY em M1, M2 e M3). Obs - rs = rad/s
  M1rs = (velX) *0.766  + fz; // 0.766
  M2rs = ((double) - 0.50 * velX  -  (double)0.86 * velY) * 0.766 + fz;
  M3rs = ((double) - 0.50 * velX  +  (double)0.86 * velY) * 0.766 + fz;


  // Verificar se a velocidade é 0, pois pode causar erro no Timer, então quando 0 setar 0.00001 (pequeno próximo a zero)
  if (abs(M1rs) <= minimoVel) {
    if (M1rs >= 0) M1rs = minimoVel;
    if (M1rs < 0) M1rs = -minimoVel;
  }
  if (abs(M2rs) <= minimoVel) {
    if (M2rs >= 0) M2rs = minimoVel;
    if (M2rs < 0) M2rs = -minimoVel;
  }
  if (abs(M3rs) <= minimoVel) {
    if (M3rs >= 0) M3rs = minimoVel;
    if (M3rs < 0) M3rs = -minimoVel;
  }

}

void setMotor3(double M3rs) {
  
  // Converte rad/ para Hertz
  M3 = M3rs * 260.48 * rel ;

    
  //if(M3>1000) M3=1000; // Limite para não dar menor que 1 no timer abaixo. 
  
  // Generate micro period to step pulse
  M3 = (double)1000000 / M3;
  // Direction
  if (M3 >= 0) digitalWrite(dir3, HIGH); else digitalWrite(dir3, LOW);
  // Aciona os motores acionaMotores();

  if(abs(M3)<100) M3=100; // Valor pequeno para interrupção no timer trava o programa. 
  // LImitar no mínimo 100 us no Timer.
  //if(abs(M3)>100000000) M3=100000000;

  Timer5.initialize(abs(M3));
  
}

void setMotor2(double M2rs) {
  
   // Converte rad/ para Hertz
  M2 = M2rs * 260.48 * rel ;

  //if(M2>1000) M2=1000; // Limite para não dar menor que 1 no timer abaixo. 

  // Generate micro period to step pulse
  M2 = (double)1000000 / M2;
  // Direction
  if (M2 >= 0) digitalWrite(dir2, HIGH); else digitalWrite(dir2, LOW);
  // Aciona os motores acionaMotores();

  if(abs(M2)<100) M2=100; // Valor pequeno para interrupção no timer trava o programa. 
  // LImitar no mínimo 100 us no Timer.
  //if(abs(M2)>100000000) M2=100000000;

  Timer4.initialize(abs(M2));
  
}

void setMotor1(double M1rs) {
  
   // Converte rad/ para Hertz
  M1 = M1rs * 260.48 * rel ;

  //if(M1>1000) M1=1000; // Limite para não dar menor que 1 no timer abaixo. 
    
  // Generate micro period to step pulse
  M1 = (double)1000000 / M1;
  // Direction
  if (M1 >= 0) digitalWrite(dir1, HIGH); else digitalWrite(dir1, LOW);

  if(abs(M1)<100) M1=100; // Valor pequeno para interrupção no timer trava o programa. 
  // LImitar no mínimo 100 us no Timer.
  //if(abs(M1)>100000000) M1=100000000;

  // Aciona os motores acionaMotores();
  Timer3.initialize(abs(M1));
  
}

// Rotinas de interrupção (Ver na função init)
void callback1(){
  PORTE = PORTE | (1 << 4); delayMicroseconds(5);  PORTE = PORTE & ~(1 << 4); //delayMicroseconds(5);
}
void callback2(){
  PORTE = PORTE | (1 << 5); delayMicroseconds(5); PORTE = PORTE & ~(1 << 5); //delayMicroseconds(5);
}
void callback3(){
  PORTG = PORTG | (1 << 5); delayMicroseconds(5); PORTG = PORTG &  ~(1 << 5); //delayMicroseconds(5);
}
