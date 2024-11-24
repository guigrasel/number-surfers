# Number Surfers

**Descrição**:  
"Number Surfers" é um jogo desenvolvido com a biblioteca Pygame, onde o jogador precisa desviar de obstáculos enquanto resolve questões matemáticas simples. O objetivo é escolher a lane correta que corresponde à resposta de uma soma, ganhando pontos ao acertar as questões e evitando colisões com obstáculos.

## Funcionalidades

- **Tela inicial**:  
  O jogo começa com uma tela inicial, onde o jogador pode iniciar a partida. Esta tela é exibida pela função `show_start_screen`.

- **Início do jogo**:  
  Após pressionar uma tecla para iniciar, o jogo entra no loop principal, onde as seguintes funcionalidades acontecem:
  - O fundo é carregado e exibido.
  - O jogador é representado por uma imagem que se move em três lanes (faixas).
  - Obstáculos caem das partes superiores da tela e o jogador deve desviar deles.
  - A cada 10 segundos, uma nova questão de soma é gerada, com três alternativas de resposta.

- **Movimentos do jogador**:  
  O jogador pode se mover para a esquerda ou para a direita usando as teclas de setas. O jogador é representado por uma imagem, inicialmente posicionada na lane do meio.

- **Obstáculos**:  
  Os obstáculos são gerados aleatoriamente e caem da parte superior da tela em uma das três lanes. O jogador perde o jogo se colidir com um obstáculo.

- **Questões matemáticas**:  
  A cada 10 segundos, o jogo gera uma questão matemática simples de soma. O jogador deve escolher a lane correta, onde a resposta correta aparece. As alternativas são exibidas nas lanes de forma aleatória.
  - Se o jogador escolhe a lane com a resposta correta, ele ganha 1000 pontos.
  - Se o jogador escolhe a lane errada ou se o tempo de exibição da questão expira sem resposta, o jogo termina.

- **Pontuação**:  
  A pontuação é incrementada a cada ciclo do jogo. Quando o jogador acerta uma questão, ele ganha 1000 pontos adicionais. O jogador perde o jogo se colidir com um obstáculo ou fizer a escolha errada.

- **Tela de Game Over**:  
  Quando o jogador perde o jogo, a tela de Game Over é exibida. A pontuação final é salva e apresentada na tela de Game Over. O jogador pode escolher reiniciar o jogo.

- **Reinício**:  
  Após a tela de Game Over, o jogador pode iniciar uma nova partida pressionando uma tecla.

## Estrutura do código

- **screens.py**  
  Responsabilidade: Gerenciar as telas do jogo, como a tela inicial e a de "Game Over".  
  Principais Funções:
  - `show_start_screen`: Exibe a tela inicial com o título do jogo, os "Top Scores" e um botão para iniciar.
  - `show_game_over_screen`: Mostra a tela de fim de jogo, com o placar final e opções para reiniciar ou sair.

- **score.py**  
  Responsabilidade: Gerenciar a pontuação do jogador e os rankings de "Top Scores".  
  Principais Componentes:
  - **Classe Score**: Incrementa e reseta a pontuação do jogador. Salva e carrega os "Top Scores" de um arquivo JSON. Ordena os scores para manter o ranking atualizado.

- **player.py**  
  Responsabilidade: Representar o jogador e gerenciar sua movimentação no jogo.  
  Principais Componentes:
  - **Classe Player**: Representa o jogador com imagem e posição inicial. Permite movimentação entre diferentes faixas (lanes) utilizando entradas do teclado.

- **obstacle.py**  
  Responsabilidade: Definir obstáculos no jogo e suas interações com o jogador.  
  Principais Componentes:
  - **Classe Obstacle**: Base para todos os tipos de obstáculos. Gerencia a posição, movimentação e colisão.
  - **Subclasses**: `ObstacleBox`, `ObstacleCar`, `ObstacleLixeira`: Especializações com imagens diferentes para os obstáculos.
  - **Função `create_random_obstacle`**: Gera um obstáculo aleatório a partir das subclasses.

- **game_logic.py**  
  Responsabilidade: Controlar o loop principal do jogo e sua lógica central.  
  Principais Funções e Componentes:
  - Inicializa os elementos do jogo (jogador, obstáculos e fundo).
  - Gerencia a lógica de gameplay:
    - Incremento de dificuldade.
    - Geração de obstáculos e perguntas matemáticas.
    - Verificação de colisões e condições de "Game Over".

## Orientação a Objetos

O projeto aplica os princípios da programação orientada a objetos de maneira consistente:

- **Encapsulamento**: As classes agrupam dados e comportamentos relacionados. A classe `Player` encapsula atributos como posição e velocidade, enquanto a classe `Score` organiza a lógica de pontuação e persistência de dados.

- **Herança**: A classe base `Obstacle` serve como modelo para outros tipos de obstáculos, como `ObstacleBox`, `ObstacleCar` e `ObstacleLixeira`, promovendo o reaproveitamento de código.

- **Polimorfismo**: Diferentes tipos de obstáculos podem ser tratados de maneira uniforme. A função `create_random_obstacle` retorna objetos de subclasses específicas, mas o código não precisa saber qual o tipo exato de obstáculo.

- **Abstração**: Conceitos de alto nível como "Jogador", "Obstáculo" e "Pontuação" são encapsulados em classes, escondendo os detalhes de implementação interna e tornando o código mais limpo e modular.

## Considerações finais

O projeto demonstra uma aplicação sólida dos princípios da programação orientada a objetos, com organização modular e boa separação de responsabilidades entre as classes. O uso de encapsulamento, herança, polimorfismo e abstração garante um código reutilizável, flexível e fácil de manter. Além disso, a lógica do jogo é clara e bem estruturada, permitindo futuras expansões ou melhorias, como a adição de novos tipos de obstáculos ou funcionalidades.
