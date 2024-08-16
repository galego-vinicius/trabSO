# 🧙‍♂️ RPG Treasure Hunt - Jogo de RPG Multithread em Python 

## 🚀 Introdução

Este é um jogo de RPG simples desenvolvido em Python, onde vários personagens (representados por threads) se aventuram para coletar tesouros em um cenário compartilhado. O jogo mostra conceitos de sincronização de threads usando mutexes, semáforos, barreiras e troca de mensagens para coordenar as ações dos personagens e evitar condições de corrida.

## 📜 Regras do Jogo
- **Personagens:** Cada personagem é representado por uma thread que realiza ações de preparação, coleta de tesouros e término de aventura;
- **Preparação:** Os personagens devem se preparar para a aventura. Essa etapa é sincronizada usando uma barreira, garantindo que todos os personagens estejam prontos antes de avançar;
- **Coleta de Tesouros:** Os personagens competem para coletar tesouros. Como o recurso é limitado, utilizamos um semáforo para controlar quantos personagens podem acessar o tesouro simultaneamente;
- **Condição de Corrida:** Para evitar condições de corrida durante a coleta de tesouros, é utilizado um mutex, que garante que apenas um personagem possa acessar o recurso compartilhado (tesouro) por vez;
- **Troca de Mensagens:** Após coletar um tesouro, o personagem envia uma mensagem usando uma fila de mensagens, que pode ser lida posteriormente para verificar quais personagens conseguiram tesouros;
- **Fim da Aventura:** Após cada ciclo de coleta, o personagem aguarda um tempo aleatório antes de começar uma nova aventura.

## 🛡️ Soluções para as condições de Corrida

O código implementa várias técnicas para gerenciar a sincronização entre as threads e resolver condições de corrida:

- **Mutex (Mutual Exclusion):** Um mutex é utilizado para garantir que somente um personagem (thread) possa acessar a seção crítica (coleta de tesouros) por vez. Isso previne que múltiplas threads modifiquem o recurso compartilhado simultaneamente, evitando inconsistências;
  
- **Semáforo:** Um semáforo é utilizado para controlar o número de threads que podem acessar simultaneamente um recurso limitado (neste caso, o tesouro). Com o semáforo, garantimos que apenas um número limitado de personagens possa tentar coletar tesouros ao mesmo tempo;

- **Barreira:** A barreira sincroniza a preparação dos personagens, garantindo que todos estejam prontos antes de iniciar a coleta de tesouros. Isso evita que qualquer thread avance para a próxima etapa sem que todas estejam sincronizadas;

- **Troca de Mensagens:** O sistema de troca de mensagens permite que os personagens comuniquem as suas ações, como a coleta de tesouros. Isso ajuda no monitoramento e verificação das ações executadas pelas threads;

## 🎮 Execução do Jogo

Para executar o jogo, siga os passo abaixo. O jogo iniciará automaticamente, criando e gerenciando múltiplas threads de personagens, cada uma realizando suas tarefas até que uma interrupção seja recebida (por exemplo, um Ctrl+C no terminal).

1. Clone o repositório:
   ```bash
   git clone https://github.com/galego-vinicius/trabSO.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd trabSO
   ```
3. Execute o jogo:
   ```bash
   python trabSO.py
   ```
