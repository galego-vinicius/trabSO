
'''
O jogo simula um cenário onde vários personagens (threads) estão se aventurando e coletando tesouros. As threads representam diferentes personagens que realizam ações de preparação, coleta e término de aventura em um loop contínuo. Durante essas ações, elas precisam coordenar o acesso a recursos compartilhados usando técnicas de sincronização.'''

import threading
import random
import time
import signal
import sys

# Implementação do Mutex
class Mutex:
    def __init__(self):
        self.lock = threading.Lock()
    
    def acquire(self):
        self.lock.acquire()
    
    def release(self):
        self.lock.release()

# Implementação do Semáforo
class Semaphore:
    def __init__(self, value):
        self.value = value
        self.mutex = Mutex()
        self.waiting = []

    def acquire(self):
        self.mutex.acquire()
        while self.value <= 0:
            cond = threading.Condition(self.mutex.lock)
            self.waiting.append(cond)
            cond.wait()
        self.value -= 1
        self.mutex.release()

    def release(self):
        self.mutex.acquire()
        self.value += 1
        if self.waiting:
            cond = self.waiting.pop(0)
            cond.notify()
        self.mutex.release()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

# Implementação da Barreira
class Barrier:
    def __init__(self, count):
        self.count = count
        self.mutex = Mutex()
        self.condition = threading.Condition(self.mutex.lock)
        self.current = 0

    def wait(self):
        self.mutex.acquire()
        self.current += 1
        if self.current >= self.count:
            self.current = 0
            self.condition.notify_all()
            print("Barreira liberada. Todas as threads estão prontas!")
        else:
            print(f"Thread {threading.current_thread().name} aguardando na barreira...")
            self.condition.wait()
        self.mutex.release()

# Implementação da Troca de Mensagens
class MessageQueue:
    def __init__(self):
        self.queue = []
        self.mutex = Mutex()
        self.not_empty = threading.Condition(self.mutex.lock)

    def send(self, message):
        self.mutex.acquire()
        self.queue.append(message)
        print(f"Mensagem enviada: {message}")
        self.not_empty.notify()
        self.mutex.release()

    def receive(self):
        self.mutex.acquire()
        while not self.queue:
            self.not_empty.wait()
        message = self.queue.pop(0)
        self.mutex.release()
        return message

# Definições do jogo
class Character(threading.Thread):
    def __init__(self, name, barrier, semaphore, mutex, messages, stop_event):
        super().__init__(name=name)
        self.barrier = barrier
        self.semaphore = semaphore
        self.mutex = mutex
        self.messages = messages
        self.stop_event = stop_event

    def run(self):
        while not self.stop_event.is_set():
            self.prepare_for_adventure()
            self.collect_treasure()
            self.end_adventure()
            print(f"{self.name} esperando para começar uma nova aventura...")
            time.sleep(random.uniform(5, 10))

    def prepare_for_adventure(self):
        print(f"{self.name} está se preparando para a aventura...")
        time.sleep(random.uniform(1, 2))
        self.barrier.wait()
        print(f"{self.name} está pronto para começar.")

    def collect_treasure(self):
        print(f"{self.name} tentando adquirir o semáforo...")
        with self.semaphore:
            print(f"{self.name} adquiriu o semáforo.")
            self.mutex.acquire()
            try:
                print(f"{self.name} está coletando tesouros.")
                time.sleep(random.uniform(3, 6))  # Aumentado o tempo de coleta de tesouros
                self.messages.send(f"{self.name} coletou um tesouro!")
            finally:
                self.mutex.release()
                print(f"{self.name} liberou o mutex.")

    def end_adventure(self):
        print(f"{self.name} terminou a aventura.")

def signal_handler(sig, frame):
    print("\nInterrupção recebida, finalizando...")
    stop_event.set()
    for char in characters:
        char.join()  # Aguarda todas as threads terminarem
    sys.exit(0)

def main():
    global characters
    stop_event = threading.Event()  # Evento para sinalizar a parada das threads
    num_characters = 4
    barrier = Barrier(num_characters)
    semaphore = Semaphore(2)
    mutex = Mutex()
    messages = MessageQueue()

    characters = [Character(f"Personagem {i+1}", barrier, semaphore, mutex, messages, stop_event) for i in range(num_characters)]

    # Configurar o tratamento do sinal SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    print("Iniciando a execução das threads...")
    for char in characters:
        char.start()

    try:
        while not stop_event.is_set():
            time.sleep(60)  # Espera por 1 minuto a cada iteração
    except KeyboardInterrupt:
        pass

    print("Todas as aventuras foram concluídas.")
    print("Mensagens recebidas:")
    while not messages.queue:
        time.sleep(0.1)
    while messages.queue:
        print(messages.receive())

if __name__ == "__main__":
    main()
