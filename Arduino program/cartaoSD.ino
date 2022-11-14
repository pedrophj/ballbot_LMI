void iniciarSDCard(){

// Testar a inicialização do cartão SD
if (!SD.begin(53)) {
      Serial.println("Erro no SD Card");
      Serial2.println("Erro no SD Card");
      //while (1);
}
Serial.println("Sucesso SD Card");
Serial2.println("Sucesso SD Card");
SD.remove("test.txt");
myFile = SD.open("test.txt", FILE_WRITE);
}
