# %%
import pygame
import math
import random
import matplotlib.pyplot as plt


"""
ATENCAO!
as cores na simulacao referense a:
verde:      saudavel
azul:       imune
vermelho:   doente
cinza:      morto
"""

#tamanho da tela
tamanho = {
    "x": 820,
    "y": 600 
        }

pygame.init()

#tela
display = pygame.display.set_mode([tamanho["x"]+20,tamanho["y"]+20])

pygame.display.set_caption("Tela de contagio")

#Grupo de desenho pygame
drawGroup = pygame.sprite.Group()

#fps da simulação, recomendado deixar baixo para melhor perfirmance
ticks= 10
#mantem uma relação entre o fps com a variação de velocidade das pessoas
max_speed = int(80/ticks) 

#frames ao redor da pessoa para que ocorra o contagio
cont_range = 8

#numero de pessoas na simulação
Npessoas = 200

#inicialmente contaminadas
iniContaminadas = 10

#parametro de tempo para duração do viros
dia = 6

#agressividade do virus (0 <= a <= 1)
agreVirus = 0.7

#classe das pessoas
#implica na logica de todas elas, tratando cada uma especificamente
class life(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        #gera o bloco
        self.image = pygame.image.load("data/verde.png")
        self.image = pygame.transform.scale(self.image, [5,5]) 
        self.rect = pygame.Rect(50,50,5,5)
    
        #gera o bloco em uma posição aleatoria
        self.rect.x = random.randint(11,tamanho["x"]-10)
        self.rect.y = random.randint(11,tamanho["y"]-10)

        #gera o bloco com uma variação de velocidade aleatoria
        self.speedx = random.randrange(-max_speed,max_speed+1)
        self.speedy = random.randrange(-max_speed,max_speed+1)


        # chance do bloco mudar de direcao, serve pras pessoas mudarem de diracao de forma mais real    
        # vai ser utilizado no update  
        self.chance = None

        #parametro do bloco
        self.contaminado = False

        self.imune = None

        self.morte = None
        
        #tempo de vida do bloco serve para monitorar o tempo individual de contaminação e imunidade
        self.tempo = None
        #auxilia o controle de tempo interno no bloco para funcao
        self.tt = None

    def update(self, *args):

        #se ele morrer, nao se movimenta nem atualiza
        if self.morte != True:
            #movimentação
            self.chance = random.randint(0,100)
            if self.chance < 5:
                self.speedx = random.randrange(-max_speed,max_speed+1)
                self.speedy = random.randrange(-max_speed,max_speed+1)

            #implementando o limite da tela
            if self.rect.y < 10:
                self.speedy = -1*abs(self.speedy)

            if self.rect.y > tamanho["y"]-10:
                self.speedy = abs(self.speedy)

            if self.rect.x < 10:
                self.speedx = abs(self.speedx)

            if self.rect.x > tamanho["x"]-10:
                self.speedx = -1 * abs(self.speedx)

            #atualização da movimentação 
            self.rect.x += self.speedx 
            self.rect.y -= self.speedy 

            #logica para quando a pessoa é contaminada
            if self.tempo != None and self.contaminado == True:
                if int(self.tt) == int(self.tempo) +dia:
                    #chance de morte
                    if random.random() <= self.morte:
                        self.morte = True
                        #cor da pessoa morta
                        self.image = pygame.image.load("data/cinza.png")
                        self.image = pygame.transform.scale(self.image, [5,5]) 
                        
                    #imunidade caso nao morra
                    else:
                        self.image = pygame.image.load("data/blue.png")
                        self.image = pygame.transform.scale(self.image, [5,5]) 
                        self.imune = True
                        self.contaminado = False

            #aqui acaba a imunidade
            if self.imune == True and int(self.tt) == int(self.tempo) + dia + dia*2:
                self.imune = False
                self.tempo = None
                self.image = pygame.image.load("data/verde.png")
                self.image = pygame.transform.scale(self.image, [5,5]) 
            
        
        
#todas as informações sobre CADA pessoa
#essa tabela foi muito util e extremamente importante para o controle do programa
#foi a primeira coisa feita, facilitou bastante o desenvolvimento por conta da organizacao
TabelaGeral = {"idade": [],
            "vezes contaminado": [], 
            "contaminou x pessoas": [], 
            "morreu?":[],
            "tempo de vida":[],
            "contaminado":[],
            "imune":[],} 

#"turtle" da pessoa.
# no caso refere a uma lista que guarda o bloco de todas as pessoas
pessoas = []


#gerador de pessoas
"""
gera todas as pessoas com idades aleatorias,
junto com o preenchimento dos dados de cada um
e tambem cria o "turtle"de cada pessoa.

algo interessante, é que por conta dessa geração de pessoas com o comando "for"
o nome de cada pessoa seria um NUMERO, ou seja é facil de manejar os dados de todo mundo
após o "dataframe" criado
"""
for x in range(Npessoas):
    TabelaGeral["idade"].append(random.randint(20,50))
    TabelaGeral["vezes contaminado"].append(0)
    TabelaGeral["contaminou x pessoas"].append(0)
    TabelaGeral["morreu?"].append(0)
    TabelaGeral["tempo de vida"].append(0)
    TabelaGeral["contaminado"].append(False)
    TabelaGeral["imune"].append(False) 
    pessoas.append(life(drawGroup))
    #posicao.append(pessoas[x].rect)

#Pessoas Inicialmente contaminados
"""
como as pessoas ja sao criadas de forma aleatoria
basta deixar as primeiras delas contaminadas
"""
for x in range(iniContaminadas):
    TabelaGeral["contaminado"][x] = True


#mortalidade
#chance de morte dependente da idade da pessoa
for x in range(Npessoas):
    if TabelaGeral["idade"][x] <= 25:
        pessoas[x].morte = 0.1

    elif TabelaGeral["idade"][x] < 30: 
        pessoas[x].morte = 0.15

    elif TabelaGeral["idade"][x] < 35:
        pessoas[x].morte = 0.20

    elif TabelaGeral["idade"][x] < 40:
        pessoas[x].morte = 0.30

    elif TabelaGeral["idade"][x] <= 45:
        pessoas[x].morte = 0.35

    elif TabelaGeral["idade"][x] >45:
        pessoas[x].morte = 0.50


#tempo do primeito pronto do grafico
foto = 1

#dados utilizados para plotar o grafico
DadosPlot ={
    "tempo":[],
    "doente":[],
    "imune":[],
    "vivos":[],
    "mortes":[],
}





clock = pygame.time.Clock()

#aqui inicia a simulação
while pygame.event.poll().type != pygame.QUIT:
    clock.tick(ticks)

    #tempo ta iguala 1 segundo
    tempo = pygame.time.get_ticks() * 0.001

    display.fill([0,0,0]) 

    drawGroup.update()
    drawGroup.draw(display)

    #pra deixar o programa mais rapido a cada instante  aporcentagem vai ser a mesma pra todoas as n pessoas
    porcent = random.random()
    
    #valida imunidade,morte
    for x in range(Npessoas): 
        if pessoas[x].imune == True:
            TabelaGeral["contaminado"][x] = False
            TabelaGeral["imune"][x] = True
        else:
            TabelaGeral["imune"][x] = False

        if pessoas[x].morte == True:
            TabelaGeral["morreu?"][x] = True
            TabelaGeral["contaminado"][x] = False



    for x in range(Npessoas):                   
        """
        condição que confirma o estado de contaminado da pessoa
        a classe serve pra validar que a pessoa nao seja contaminada ja estando contaminada"""
        if TabelaGeral["contaminado"][x] == True and pessoas[x].contaminado == False:
            pessoas[x].image = pygame.image.load("data/red.png")
            pessoas[x].image = pygame.transform.scale(pessoas[x].image, [5,5]) 
            pessoas[x].tempo = tempo
            pessoas[x].contaminado = True

            TabelaGeral["vezes contaminado"][x] += 1
            

    #contaminacao de pessoas
    for x in range(Npessoas):

        if TabelaGeral["contaminado"][x] == True:
            for y in range(Npessoas):
                if porcent <= agreVirus: #chance de contagiar
                    #cada pessoa tem uma chance de pegar
                    if pessoas[y].imune != True and TabelaGeral["morreu?"][y] != True: #verifica imunidade
                        if x != y :
                            #aqui entra em pratica a area de contagio declarada inicialmente
                            if pessoas[x].rect.x in range(pessoas[y].rect.x-cont_range,
                            pessoas[y].rect.x+cont_range+1):

                                if pessoas[x].rect.y in range(pessoas[y].rect.y-cont_range,
                            pessoas[y].rect.y+cont_range+1):
                                    TabelaGeral["contaminado"][y] = True
                                    #atualizacao para possivel monitoramento
                                    TabelaGeral["contaminou x pessoas"][x] += 1


    #atualiza o tempo de vida no mundo em cada pessoa/bloco
    for x in range(Npessoas):
        if TabelaGeral["morreu?"][x] != True:
            pessoas[x].tt = tempo
    
    #pontos que sao coletados a cada x segundos
    if int(tempo) == foto:
        #o "foto" determina a cada quanto tempo que é pego os pontos
        foto +=1
        DadosPlot["tempo"].append(int(tempo))
        DadosPlot["doente"].append(TabelaGeral["contaminado"].count(True))
        DadosPlot["vivos"].append(TabelaGeral["morreu?"].count(False))
        DadosPlot["imune"].append(TabelaGeral["imune"].count(True))
        DadosPlot["mortes"].append(TabelaGeral["morreu?"].count(True))

    pygame.display.update()
    pygame.display.flip()
pygame.quit()



#criação do grafico

ax = plt.subplot()

ax.plot(DadosPlot["tempo"], DadosPlot["doente"], label='doentes')  
ax.plot(DadosPlot["tempo"], DadosPlot["imune"], label='imunes')  
ax.plot(DadosPlot["tempo"], DadosPlot["vivos"], label='vivos') 
ax.plot(DadosPlot["tempo"], DadosPlot["mortes"], label='mortes') 
ax.legend()

# %%


