import random
import numpy as np
from chrome_trex import DinoGame


# Sinta-se livre para brincar com os valores abaixo

CHANCE_MUT = .3      # Chance de mutação de um peso qualquer
CHANCE_CO = .4      # Chance de crossing over de um peso qualquer
NUM_INDIVIDUOS = 200  # Tamanho da população
NUM_MELHORES = 80     # Número de indivíduos que são mantidos de uma geração para a próxima


def ordenar_lista(lista, ordenacao, decrescente=True):
    """
    Argumentos da Função:
        lista: lista de números a ser ordenada.
        ordenacao: lista auxiliar de números que define a prioridade da
        ordenação.
        decrescente: variável booleana para definir se a lista `ordenacao`
        deve ser ordenada em ordem crescente ou decrescente.
    Saída:
        Uma lista com o conteúdo de `lista` ordenada com base em `ordenacao`.
    Por exemplo,
        ordenar_lista([2, 4, 5, 6], [7, 2, 5, 4])
        # retorna [2, 5, 6, 4]
        ordenar_lista([1, 5, 4, 3], [3, 8, 2, 1])
        # retorna [5, 1, 4, 3]
    """
    return [x for _, x in sorted(zip(ordenacao, lista), key=lambda p: p[0], reverse=decrescente)]


def populacao_aleatoria(n):
    """
    Argumentos da Função:
        n: Número de indivíduos
    Saída:
        Uma população aleatória. População é uma lista de indivíduos,
        e cada indivíduo é uma matriz 3x10 de pesos (números).
        Os indivíduos podem tomar 3 ações (0, 1, 2) e cada linha da matriz
        contém os pesos associados a uma das ações.
    """
    # Referência: np.random.uniform()
    #             list.append()
    #             for loop (for x in lista:)
    minVal = -10.0
    maxVal = 10.0
    pop = [np.random.uniform(minVal, maxVal, (3, 10)) for i in range(n)]
    return pop


def valor_das_acoes(individuo, estado):
    """
    Argumentos da Função:
        individuo: matriz 3x10 com os pesos do indivíduo.
        estado: lista com 10 números que representam o estado do jogo.
    Saída:
        Uma lista com os valores das ações no estado `estado`. Calcula os valores
        das jogadas como combinações lineares dos valores do estado, ou seja,
        multiplica a matriz de pesos pelo estado.
    """
    # Referência: multiplicação de matrizes (A @ B)
    return individuo @ estado


def melhor_jogada(individuo, estado):
    """
    Argumentos da Função:
        individuo: matriz 3x10 com os pesos do indivíduo.
        estado: lista com 10 números que representam o estado do jogo.
    Saída:
        A ação de maior valor (0, 1 ou 2) calculada pela função valor_das_acoes.
    """
    # Referência: np.argmax()
    v = valor_das_acoes(individuo, estado)
    return np.argmax(v)


def mutacao(individuo):
    """
    Argumentos da Função:
        individuo: matriz 3x10 com os pesos do indivíduo.
    Saída:
        Essa função não tem saída. Ela apenas modifica os pesos do indivíduo,
        de acordo com chance CHANCE_MUT para cada peso.
    """
    # Referência: for loop (for x in lista)
    #             np.random.uniform()

    # A modificação dos pesos pode ser feita de diversas formas (vide slides)

    minVal = -1.5
    maxVal = 1.5
    for i in range(len(individuo)):
        for j in range(len(individuo[0])):
            if np.random.uniform(0, 1) < CHANCE_MUT: 
                individuo[i, j] *= np.random.uniform(minVal, maxVal)

def crossover(individuo1, individuo2):
    """
    Argumentos da Função:
        individuoX: matriz 3x10 com os pesos do individuoX.
    Saída:
        Um novo indivíduo com pesos que podem vir do `individuo1`
        (com chance 1-CHANCE_CO) ou do `individuo2` (com chance CHANCE_CO),
        ou seja, é um cruzamento entre os dois indivíduos. Você também pode pensar
        que essa função cria uma cópia do `individuo1`, mas com chance CHANCE_CO,
        copia os respectivos pesos do `individuo2`.
    """
    # Referência: for loop (for x in lista)
    #             np.random.uniform()
    individuo = individuo1.copy()
    for i in range(len(individuo)):
        for j in range(len(individuo[0])):
            if np.random.uniform(0, 1) < CHANCE_CO: 
                individuo[i, j] = individuo2[i, j] 
    return individuo


def calcular_fitness(jogo, individuo):
    """
    Argumentos da Função:
        jogo: objeto que representa o jogo.
        individuo: matriz 3x10 com os pesos do individuo.
    Saída:
        O fitness calculado de um indivíduo. Esse cálculo é feito simulando um
        jogo e calculando o fitness com base nessa simulação. O modo mais simples
        é usando fitness = score do jogo.
    """
    # Referência: while loop (while condition)
    #             np.random.uniform()

    # Você precisará da função melhor_jogada()

    # O jogo é simulado usando:
    #   jogo.reset()
    #   jogo.game_over
    #   jogo.step(acao)  # Toma a ação `acao` e vai para o próximo frame
    #   jogo.get_score()
    #   jogo.get_state()

    jogo.reset()
    while not jogo.game_over:
        acao = melhor_jogada(individuo, jogo.get_state())
        jogo.step(acao)
    return jogo.get_score()

def proxima_geracao(populacao, fitness):
    """
    Argumentos da Função:
        populacao: lista de indivíduos.
        fitness: lista de fitness, uma para cada indivíduo.
    Saída:
        A próxima geração com base na população atual.
        Para criar a próxima geração, segue-se o seguinte algoritmo:
          1. Colocar os melhores indivíduos da geração atual na próxima geração.
          2. Até que a população esteja completa:
             2.1. Escolher aleatoriamente dois indivíduos da geração atual.
             2.2. Criar um novo indivíduo a partir desses dois indivíduos usando
                  crossing over.
             2.3. Mutar esse indivíduo.
             2.4. Adicionar esse indivíduo na próxima geração
    """
    # Referência: random.choices()
    #             while loop (while condition)
    #             lista[a:b]

    # Dica: lembre-se da função `ordenar_lista(lista, ordenacao)`.

    popOrdenada = ordenar_lista(populacao, fitness)
    novaGeracao = popOrdenada[0:NUM_MELHORES]
    while len(novaGeracao) < NUM_INDIVIDUOS:
        individuo1, individuo2 = random.choices(populacao, k = 2)
        individuo = crossover(individuo1, individuo2)
        mutacao(individuo)
        novaGeracao.append(individuo)
    return novaGeracao


def mostrar_melhor_individuo(jogo, populacao, fitness):
    """
    Argumentos da Função:
        jogo: objeto que representa o jogo.
        populacao: lista de indivíduos.
        fitness: lista de fitness, uma para cada indivíduo.
    Saída:
        Não há saída. Simplesmente mostra o melhor indivíduo de uma população.
    """
    # VOCÊ NÃO PRECISA MEXER NESSA FUNÇÂO

    fps_antigo = jogo.fps
    jogo.fps = 100
    ind = populacao[max(range(len(populacao)), key=lambda i: fitness[i])]
    print('Melhor individuo:', ind)
    while True:
        if input('Pressione enter para rodar o melhor agente. Digite q para sair. ') == 'q':
            jogo.fps = fps_antigo
            return
        fit = calcular_fitness(jogo, ind)
        print('Fitness: {:4.1f}'.format(jogo.get_score()))


###############################
# CÓDIGO QUE RODA O ALGORITMO #
###############################

# Referência: for loop (for x in lista)
#             list.append()

# OBS: Todos os prints dentro dessa função são opcionais.
#      Eles estão aqui para facilitar a visualização do algoritmo.

num_geracoes = 100
jogo = DinoGame(fps=50_000)

populacao = populacao_aleatoria(NUM_INDIVIDUOS)

print('ger | fitness\n----+-' + '-'*5*NUM_INDIVIDUOS)

for ger in range(num_geracoes):
    fitness = [calcular_fitness(jogo, i) for i in populacao]
    populacao = proxima_geracao(populacao, fitness)

    print('{:3} |'.format(ger),
          ' '.join('{:4d}'.format(s) for s in sorted(fitness, reverse=True)))

    # Opcional: parar se o fitness estiver acima de algum valor (p.ex. 300)
    if np.amax(fitness) > 800:
        break

# Calcule a lista de fitness para a última geração
fitness = [calcular_fitness(jogo, i) for i in populacao]

mostrar_melhor_individuo(jogo, populacao, fitness)
