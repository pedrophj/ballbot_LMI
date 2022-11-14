// Último teste feito por aqui
#include <Wire.h>
//#include "TimerOne.h"
#include "TimerThree.h"
#include "TimerFour.h"
#include "TimerFive.h"
#include "variaveis.h"
#include <SPI.h>
#include <SD.h>
File myFile;

long periodoLoop=0;
String dados="";
int contDebug=0;

void setup() {
  iniciar(); // configura pinos I/O, configura IMU, bussola, etc
  //iniciarLidar();
  periodoLoop=millis();
}



void loop() {
   
  // Feedback com ângulo e vel. angular (Theta ThetaP)
  ler_IMU(); // ler os angulos e vel. angulares

   
  // Testar em Seno na referência de ângulo do PD (fica muio legal ele fica dançando)
  //SetpointX=sin(millis()*0.004)*refX;
  //SetpointY=sin(millis()*0.01)*refY;
 // SetpointX+=(double)refX;

   // Enviar na Serial b1 (mudar entrada para rampa) ou b0 (para degrau). Padrão é degrau.
   // Ver na aba atuadores, o limite para a rampa parar.
   
   if(tipoEntrada) entradaRampa();
   else entradaDegrau();

   // Enviar na Serial n1 (controle de posição) ou n0 para (controle de velocidade)
   if(modoVelPos==0)  controladorLQRVel(); // Calcula erros e a saída do controlador Velocidade
   if(modoVelPos==1)  controladorLQRPos(); // Calcula erros e a saída do controlador Posição
   
   //controladorPID();  
  // Controle de Guinada
  leituraBussola();  // Obter os valores do magnetômetro
  //imprimeRespostaNatural();
  
  // Modo de ref. do controlador de Guinada 
  //if(contGui>10){
    if(modoGuinada==0)  controladorYawPos(); // Modo de controle de Posição da Guinada (Proporcional)
    if(modoGuinada==1)  controladorYawVel(); // Modo de controle de Velocidade da Guinada (PI)
  //  contGui=0;
  //}
  //contGui++;
  
  // Atuadores 
  converVel(); // Converter velX e velY para M1,M2 e M3 obs rs = radiano/segundo

  setMotor1(M1rs); // ajusta da velocidade do motor 1
  setMotor2(M2rs); // ajusta da velocidade do motor 2
  setMotor3(M3rs); // ajusta da velocidade do motor 3
  
  // Debugguer e telemetria

 debugar(debug);  // Parâmetro debug seleciona quais dados serão impressos na serial


  telemetria();   // Enviar os ângulos para o robô via serial 
  
  // Manter o Loop de controle c/ período constante
  timekeeper();   // Manter o período do loop constante

  Teste_serialEvent3();
}
