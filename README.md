# Projeto de Redes (Socket)

Nesse projeto desenvolvemos uma socket de rede e uma aplicação, para exercitar nosso conhecimento em Redes de computadores, onde até 3 pessoas conseguem usar a aplicação e se comunicar através dela.

## Rodando a aplicação

1. É preciso ter as seguintecas bibliotecas do Python instaladas no sistema: pygame, socket e pickle.
2. No terminal que será responsável por rodar o servidor, execute o arquivo *servidor.py*
3. No(s) terminal(is) que irá(ão) rodar o jogo, execute o arquivo *game.py*
4. No jogo que se abrir, aparecerá instruções na parte de baixo da janela com a tecla que o usuário deverá apertar caso queira jogar ou enviar seu score ao servidor
5. Caso perca, aparecerá instruções na parte de baixo da janela com a tecla que o usuário deverá caso queira enviar para o servidor seu score ou não.

# Funcionalidades da Aplicação

O jogo consiste no clássico "jogo da cobrinha", na qual consiste em uma cobra que se movimenta na tela de acordo com a vontade do jogador e come frutinhas que fazem crescer o seu tamanho. Quanto mais frutinhas ela cobre, maior ela fica e maiores são as chances de ou se morder ou atingir as bordas da tela. Em ambos os casos, o jogador perde.
Quando termina a partida, o jogador pode escolher enviar seu score para um servidor, que é multi-thread, aceitando até três conexões com clientes, rodando localmente na máquina. Ele armazena os scores dos jogadores e envia o scoreboard quando algum cliente pedir. Foram utilizados três bibliotecas do Python para a construção do servidor: Socket e Pickle e Thread. A socket, como o nome sugere, é a responsável por fazer a comunicação entre o cliente e o servidor, já a pickle é responsável em encapsular a lista contendo as pontuações dos jogadores, dividindo-os em bits.

# O que poderia ter sido implementado a mais

O servidor poderia hospedar os jogadores em tempo real, como em jogos de batalha real, na qual um jogador ataca outro indiretamente e tenta derrotar todos os restantes até se tornar o único sobrevivente e então vencedor. Nesse caso, os 4 jogadores iriam batalhar entre si, onde um jogador iria forçar as cobrinhas dos adversários acertarem as bordas da tela ou se morder, a partir de maçãs especiais que a cobrinha do jogador iria comer, mas enviaria um boost de velocidade para as cobrinhas adversárias. É fácil notar que quanto maior a cobrinha, mais dificil ela é de controlar, logo as chances do jogador que a possui perder aumentariam também.

# Dificuldades encontradas

### Na aplicação

A lógica da colisão com objetos que não tem o mesmo tamanho de um pouco de trabalho, mas conseguimos concluir. Ainda na parte da aplicação, a lógica da rotação da imagem da cauda da cobra não foi concluída por má gestão de tempo, pois, por causa de alguns atrasos acabamos deixando de segundo plano, assim como partidas com multiplas cobras na mesma tela.


