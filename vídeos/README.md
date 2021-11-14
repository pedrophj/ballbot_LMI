
## Vídeos do Simulador CoppeliaSim

Os vídeos abaixo mostram a navegação autônoma com 4 *waypoints*, operando em dois modos. O modo 1 a referência de guinada é alterada com o objetivo do robô orientar em direção ao *waypoint* atual. O modo 2 o robô executa a missão com uma orientação fixa. 
As coordenadas dos pontos (em centímetros) foram: [ [0,100] , [-50,100] , [-50,0] [0,0] ]

- navegacao_coppeliaSim_4pontos_modo1.mp4
- navegacao_coppeliaSim_4pontos_modo2.mp4

A navegação de uma trajetória complexa em formato de "8" no modo 1 é apresentado no vídeo abaixo. As coordenadas dos pontos (em centímetros) foram: [ [0,0], [19.9, 7.7], [28.5,25.12],[20.9,42.7],[7.1 ,50.2],[-9.8,57.9],[-26,69.2],[-26.6,88.46],[-9.89,99.19],[10.3,98.3],[24.2,87.4],[24.4,71.9],[15.6,59.3],[0,55],[-22,43.3],[-30.6,36.6],[-31.7,22.7],[-23.4,8],[0,0] ].

- navegacao_coppeliaSim_19pontos.mp4


## Vídeos de rastreamento de objetos

No primeiro vídeo o robô deve seguir o objeto colorido, ou seja, o objeto deve estar sempre no centro da imagem captada pela câmera embarcada no robô. Nesse experimento o robô está a 1 metro de distância do objeto. A posição do objeto colorido é alterada em 3 etapas com distância total de 30 cm. O objetivo de analisar apenas a guinada do robô. No segundo vídeo é testado tanto a guinada como a translação.

- experimento_rastreamento_guinada.mp4
- experimento_rastreamento_translacao.mp4

## Vídeos de navegação por waypoints

Os vídeos mostram os resultados de navegação com 2, 3 e 4 *waypoints*. Essa lista é carregada em um arquivo .txt no software de controle e então é enviada via *bluetooth* para o robô. O *ballbot* deve seguir ponto a ponto até completar todos os pontos da lista. 

As coordenadas dos pontos(em centímetros) foram: 2 pontos = [[75,150],[75,50]]; 3 pontos = [[100,150],[50,150],[50,50]]; 4 pontos = [[100,150], [50,150], [50,50],[100,50]].

- experimento_navegacao_2.mp4
- experimento_navegacao_3.mp4
- experimento_navegacao_4.mp4
- experimento_navegacao_reta.mp4

## Vídeos de controle via aplicativo

Os dois vídeos abaixo mostram o controle manual via *bluetooth*. No modo de guinada são incrementados as velocidades dos 3 motores. No arquivo experimento_controle_app a translação foi executada enviando a referência (10 cm/s) de velocidade via *bluetooth*.

- experimento_controle_guinada_app.mp4 
- experimento_controle_app.mp4
