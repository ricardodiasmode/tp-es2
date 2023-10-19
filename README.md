## tp-es2
This is a simples ML project using Reinforcement Learning with Neural Network to train some Software Engineering concepts. 

# 1.
Ricardo Dias Avelar - 2019054960
# 2.
A ideia do projeto é um jogo onde temos dois bonecos (controlados por uma rede neural) inimigos e eles precisam se destruir. Aquele que mata o outro primeiro, ou chega mais perto disso, é o que prevalece na próxima geração. Para tanto, há o artifício de ter que criar uma arma (faca). A criação da arma se dá pelo processo de pegar e transformar um recurso (madeira). Note, portanto, que os passos para o sucesso são: Andar até o recurso -> Transformar o recurso em arma -> Matar o inimigo. É importante notar que, dado a complexidade do sistema e o tempo dado para o trabalho, já temos uma boa quantidade de código escrita mas apenas o segundo passo está implementado. Ainda, é importante notar também que a rede neural implementada *ainda* não converge. Pretendo completar o terceiro passo e fazer a rede neural convergir na segunda etapa.

A rede neural é treinada pela estratégia de aprendizado por reforço, e todas as funções relacionadas estão na classe neuralNetwork.py. O loop do jogo ocorre em main.py, onde podemos ver que as gerações e a verificação se o jogo ainda ocorre ou não é rodada por um "while". O jogo se resume a um primeiro passo que é a rede neural pensar (chamadas GameMode.BlueCharacters[i].Brain.Think e GameMode.RedCharacters[i].Brain.Think), que é o processo em que ela é alimentada por uma entrada e retorna uma saída, e um segundo passo que é a rede neural reagir (chamadas GameMode.BlueCharacters[i].React e GameMode.RedCharacters[i].React), que é de fato a ação dela no mundo, dado o output feito pelo "pensamento".

Todo o loop do jogo se resume aos passos:
1. Chamada do GameMode para iniciar ou reiniciar o jogo;
2. Aos personagens pensarem e reagirem;
3. Verificação do GameMode de como foi o turno;
    3.1. Se no turno todos os personagens de um time morreram, então a geração é reiniciada;
    3.2. Caso contrário, volta para etapa 2.

Note que o ato de reiniciar a geração significa realizar todos os rituais de uma rede neural que trabalha com aprendizado por reforço, que vou omitir aqui pois me extenderia demais.

# 3. 

