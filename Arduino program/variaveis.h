// Pinos de I/O (Driver)
#define dir1 5 // Saída do sentido de rotação do motor 1
#define dir2 6 // Saída do sentido de rotação do motor 2
#define dir3 7 // Saída do sentido de rotação do motor 3
#define enb 8 // Habilita o driver
#define stp1 2 // Pulso de step do motor 1
#define stp2 3 // Pulso de step do motor 2
#define stp3 4 // Pulso de step do motor 3
#define led 22 // LED indicador de funcionamento

// Coeficiente do filtro complementar
//#define alfa   0.98
//#define alfa_1 0.02
#define alfa   0.996 //  padrão q funciona bem 996
#define alfa_1 0.004

#define minimoVel    0.000001
// #define minimoVel 0.00001
int teste =0;

// Número de amostras para tirar a média do bias de PItch e Roll
int amostras = 3000;

// Período do loop de controle
#define STD_LOOP_TIME 6 // Período do loo de controle em ms  
unsigned long loopStartTime = 0;    // começo da contagem do tempo
unsigned long lastTime;             // tempo do último loop

// Variáveis da com. Serial
String inputString = "";         // string para guardar o dado recebido pela serial
boolean stringComplete = false;  // se a string esta completa (aguardar o \n)
boolean imprimeGanhos = false; // imprimirá na função de telemetria 

///////////////////////  Início das variáveis da Bússola //////////////
// Variáveis para a calibração da Bussola
double min_mx = 0; // Valor mínimo X
double max_mx = 0; // Valor máximo X
double min_my = 0; // Valor máximo Y
double max_my = 0; // Valor máximo Y
double mx_bias = 0; // Média do bias em X
double my_bias = 0; // Média do bias em Y
double mx_ganho = 0; // Ganho em X para correção do bias
double my_ganho = 0; // Ganho em Y para correção do bias

// Valor medido pela Bússola
double magx = 0; // Valor do magnetômetro X
double magy = 0; // Valor do magnetômetro Y
double orientacao = 0; // Orientação do robô em rad
double orientacaoF = 0; // Orientação do robô em rad
double orientacaoAnt = 0; // Orientação anterior para o filtro
double orientacaoGraus = 0; // Orientação do robô em graus
double erroYaw = 0; double erroYawAnt = 0; double integralErroYaw = 0;
double fz = 0; // saída do controlador PI
double fzAnt = 0; // Testar um passa baixa
double refz = 0; // setpoint do PI de Yaw

// Bússola
int Xaxis = 0; // Valor da leitura da bússola eixo X
int Yaxis = 0; // Valor da leitura da bússola eixo Y
int Zaxis = 0; // Valor da leitura da bússola eixo Z
uint8_t MSBnum = 0; // Parte mais significativa
uint8_t LSBnum = 0; // Parte menos significativa
#define addr 0x0D  // Endereço do dispositivo I2C

///////////////////////  Fim das variáveis e define da Bússola ////////////////////////////////////////

// Variáveis dos controladores e atuadores
double freqMax = 1; // Valor de saturação dos motores em rad/s
double acelMax = 30; // Valor de saturação da saída dos controlodores Pitch e Roll (antes estava 15)
double angleMax = 0.01; // Ângulo máximo de inclinação permitido para o controlador funcionar.
double Dir = 0; double Res = 0;

// Valor de referência passado via bluetooth para o controlador
double refX = 0; double refY = 0;
int tipoEntrada=0; // 0=degrau  1=rampa

// Variáveis velocidade e posição
double velX = 0; double velY = 0; double velXAnt = 0; double velYAnt = 0;
double posX = 0; double posY = 0; double posXAnt = 0; double posYAnt = 0;

// Variáveis de erro de ângulo em X (Pitch) e erro em Y (Roll)
double erroX = 0; double erroY = 0;
double erro0X = 0; double erro0Y = 0; double erroWX = 0; double erroWY = 0;
double erroXAnt = 0; double erroYAnt = 0; double erro0XAnt = 0; double erro0YAnt = 0;
double erroPosX = 0; double erroPosY = 0;
// Velocidades dos motores M1, M2 e M3
double M1 = 0; double M2 = 0; double M3 = 0; // Valor em periodo us para o pulso no motor
double M1rs = 0; double M2rs = 0; double M3rs = 0; // Velocidade em rad/s

// Ângulo de Pitch eixo X
double ThetaX = 0;    double ThetaY = 0; // Valores de ângulo de Pitch e Roll
double ThetaXAnt = 0;    double ThetaYAnt = 0; // (Ant = Anterior) usado no filtro passa baixa

// Ângulo de Roll eixo Y
double ThetaXp = 0;    double ThetaYp = 0; // Valores da velocidade ângular de Pitch e Roll
double ThetaXpAnt = 0;    double ThetaYpAnt = 0; // (Ant = Anterior) Anterior usado no filtro passa baixa

double distLidar=0; double distLidarAnt=0; // Anterior
int habGuinadaLidar=0; // Se habilitar ele começa a ler 90 graus ao redor dele.
double refAngLidar=0;  // Variavel para incremetnar o rastreamento pelo lidar
double refAngLidarInicio=0; // Angulo inicial da varredura do Lidar
double refAngLidarFim=0;   // Angulo final da varredura do Lidar

// Saída do controlador
double acelX;     double acelY; // Saída do controlador em aceleração
double acelXAnt;     double acelYAnt; // Saída do controlador em aceleração

// Ganhos e Setpoint do controlador LQR
//double K1 = 60, K2 = 45, K3 = 3, K4 = 0; // Ganhos dos controladores e Pitch e Roll estavam 60, 45, 3 
//double rel = 4; // Relação da roda/bola

double K1 = 50, K2 = 25, K3 = 2.5, K4 = 0;
double rel = 7; // Relação da roda/bola


double SetpointX = 0; double SetpointY = 0; // Valores de velocidade desejados

// Controlador PI + PD
double integralErroVelX = 0; double integralErroVelY = 0; //intgral do erro de velocidade do PI
double refThetaX = 0; double refThetaY = 0; // Saída dos controladores PI de velocidade

long tempoM1, tempoM2, tempoM3;

boolean habGuinada = false; // Para permitir a habilitação do controlador

//Gyro Variaveis
double elapsedTime, time, timePrev;        //Variables for time control
int gyro_error = 0;                       //We use this variable to only calculate once the gyro data error
float Gyr_rawX, Gyr_rawY, Gyr_rawZ;     //Here we store the raw data read
float Gyro_angle_x, Gyro_angle_y;         // Usado apenas no filtro complementar, veja que não é feito += para integrar
float GyroAngleX, GyroAngleY;         // ângulo obtido pela integração númerica
float Gyro_raw_error_x, Gyro_raw_error_y; //Here we store the initial gyro data error

//Acc Variaveis
int acc_error = 0;                       //We use this variable to only calculate once the Acc data error
float rad_to_deg = 180 / 3.141592654;    //This value is for pasing from radians to degrees values
float Acc_rawX, Acc_rawY, Acc_rawZ;    //Here we store the raw data read
float Acc_angle_x, Acc_angle_y;          //Here we store the angle value obtained with Acc data
float Acc_angle_error_x, Acc_angle_error_y; //Here we store the initial Acc data error

// Bias
float Acc_rawXBias = 0; float Acc_rawYBias = 0; float Acc_rawZBias = 0;
float Gyr_rawXBias = 0; float Gyr_rawYBias = 0; float Gyr_rawZBias = 0;

float Total_angle_x, Total_angle_y; // Valor em graus
float GyroZ=0; float GyroZAnt=0;

// Variáveis para medir o tempo e auxiliar em multiplas tarefas
long tempoPulso = millis(); // Medir o tempo dp pulso
long tempoPisca = millis(); // Para fazer o piscaLED de atividade
long tempoRampaVel = millis(); // Para fazer o piscaLED de atividade
long tempoTelemetria = millis(); //
int habTelemetria = 0; // Variável para habilitar a telemetria (0 desabilita e 1 habilita)
int modoGuinada=0;
int contGui=0; // Contador teste para deixar a guinada sempre no loop
int modoVelPos=0; // 0=velocidade 1=posição
int modoRastreamento=0;


int debug = 0; // Para debuggar e ver os dados na Serial

int inicioMov = 0; // Somente se o robô estiver em 0 ele começa o movimento
