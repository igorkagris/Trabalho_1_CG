from tkinter import *
from tkinter import colorchooser
import math
t_width = 750
t_height = 600

class vertice:
    def __init__(self, x = int, y = int, cor = "black"):
        self.x = x
        self.y = y
        self.cor = cor
    
    def altera_cor(self, cor):
        self.cor = cor

class triangulos:
    def __init__(self, Vert_A = '', Vert_B = '', Vert_C = '', nome = ''):
        self.A = Vert_A
        self.B = Vert_B
        self.C = Vert_C
        self.nome = nome

    def arestas(self):
        x_aux = self.B.x - self.A.x
        y_aux = self.B.y - self.A.y
        self.AB = math.sqrt(math.pow(x_aux, 2) + math.pow(y_aux, 2))

        x_aux = self.C.x - self.A.x
        y_aux = self.C.y - self.A.y
        self.AC = math.sqrt(math.pow(x_aux, 2) + math.pow(y_aux, 2))
        
        x_aux = self.C.x - self.B.x
        y_aux = self.C.y - self.B.y
        self.BC = math.sqrt(math.pow(x_aux, 2) + math.pow(y_aux, 2))


def fill_poly():                #algoritmo de coloração fill_poly
    global triangulo
    obj = triangulo[0]

    #   Transforma as strings hexadecimais em vetores cor[[r], [g], [b]],
    # ignorando o #, separando e convertendo as 3 duplas de hexadecimais(00-FF) para inteiros[0-255]
    if '#' not in obj.A.cor:
        print("Erro na linha 43, cor está em string")
    cor_A_rgb = obj.A.cor[1:]
    cor_A_rgb = [int(cor_A_rgb[0:2], 16), int(cor_A_rgb[2:4], 16), int(cor_A_rgb[4:6], 16)] 
    cor_B_rgb = obj.B.cor[1:]
    cor_B_rgb = [int(cor_B_rgb[0:2], 16), int(cor_B_rgb[2:4], 16), int(cor_B_rgb[4:6], 16)]
    cor_C_rgb = obj.C.cor[1:]
    cor_C_rgb = [int(cor_C_rgb[0:2], 16), int(cor_C_rgb[2:4], 16), int(cor_C_rgb[4:6], 16)]

    '''     *******  PSEUDOCÓDIGO  *******
    obj ou triangulo[x] tem seus vertices A, B e C organizados de forma crescente em y por outra função
    para cada valor (linha de pixel) entre o menor valor em y e o maior
        define x1 e x2, limites min e max entre os quais serão pintados #x_intersecao = x1 + ((x2 - x1) * (y_scanline - y1)) / (y2 - y1)
            #ifs definem se x1 faz parte do vertice AB ou BC; x2 = vertice AC

        degrade = valor entre 0 e 1 equivalente ao percentual percorrido na aresta (AB ou BC) e AC
        cor_x1 = cor atual do degrade entre A e B, ou B e C
        cor_x2 = cor atual do degrade entre os vertices A e C

        condicao if garante que x1 esteja antes que x2

        para cada elelento entre x1 e x2
            degrade = valor entre 0 e 1 equivalente ao percentual percorrido entre x1 e x2
            cor_pixel = cor atual do degrade entre cor_x1 e cor_x2, convertido para hexadecimal novamente
            pinta o pixel atual com o valor de cor_pixel '''
    
    for y in range(obj.A.y, obj.C.y):

        if (y < obj.B.y):
            #x1 = obj.A.x + ((obj.B.x - obj.A.x) * (y - obj.A.y)) / (obj.B.y - obj.A.y)
            x1 = obj.A.x + (y - obj.A.y) * (obj.B.x - obj.A.x) / (obj.B.y - obj.A.y)
            degrade = (y - obj.A.y)/(obj.B.y - obj.A.y)
            cor_x1 = (int((1-degrade)*cor_A_rgb[0] + degrade*cor_B_rgb[0]), int((1-degrade)*cor_A_rgb[1] + degrade*cor_B_rgb[1]), int((1-degrade)*cor_A_rgb[2] + degrade*cor_B_rgb[2]))
        elif (y == obj.B.y):
            x1 = obj.B.x
            cor_x1 = cor_B_rgb
        else:
            x1 = obj.B.x + ((obj.C.x - obj.B.x) * (y - obj.B.y)) / (obj.C.y - obj.B.y)
            degrade = (y-obj.B.y) / (obj.C.y-obj.B.y)
            cor_x1 = (int((1-degrade)*cor_B_rgb[0] + degrade*cor_C_rgb[0]), int((1-degrade)*cor_B_rgb[1] + degrade*cor_C_rgb[1]), int((1-degrade)*cor_B_rgb[2] + degrade*cor_C_rgb[2]))

        degrade = (y-obj.A.y)/(obj.C.y-obj.A.y)
        x2 = obj.A.x + ((obj.C.x - obj.A.x) * (y - obj.A.y)) / (obj.C.y - obj.A.y)
        cor_x2 = (int((1 - degrade)*cor_A_rgb[0] + degrade*cor_C_rgb[0]), int((1-degrade)*cor_A_rgb[1] + degrade*cor_C_rgb[1]), int((1-degrade)*cor_A_rgb[2] + degrade*cor_C_rgb[2]))
        
        if(x2<x1):
            x1, x2 = x2, x1
            cor_x1, cor_x2 = cor_x2, cor_x1

        for i in range(round(x1), round(x2)):
            degrade = (i-round(x1))/(round(x2) - round(x1))
            cor_pixel = (int((1-degrade) * cor_x1[0] + degrade*cor_x2[0]), int((1-degrade)*cor_x1[1] + degrade*cor_x2[1]), int((1-degrade)*cor_x1[2] + degrade*cor_x2[2]))
            cor_pixel = "#{:02X}{:02X}{:02X}".format(*cor_pixel)

            janela_desenho.create_oval(i, y, i+1, y+1, fill=cor_pixel, outline=cor_pixel)
         
            


def alterar_cor():              #(buttom) altera a cor do vertice a ser posto
    global cor_vertice
    cor_vertice = colorchooser.askcolor(color=cor_vertice)[1]

def local_ponteiro(event):      #retorna o local do ponteiro dentro do quadro de desenho para exibir no rodape
    ponteiro_x = event.x
    ponteiro_y = event.y
    ponteiro_txt["text"] = f'''x: {ponteiro_x};  y: {ponteiro_y}'''

def verifica_triangulo():       #retorna true se o triangulo criado for válido (A != B+C)
    lado = []
    for i in range(3):
        x_aux = vetor_X[(i+1)%3] - vetor_X[i]
        y_aux = vetor_Y[(i+1)%3] - vetor_Y[i]
        lado.append(math.sqrt(math.pow(x_aux, 2) + math.pow(y_aux, 2)))
    
    if lado[0] == (lado[1] + lado[2]) or lado[1] == (lado[0] + lado[2]) or lado[2] == (lado[1] + lado[0]):
        return False

def limpa_tela():               #remove todos os dados da area de desenho
    janela_desenho.delete(ALL)

def msg_erro(mensagem = str):   #nova janela com mensagem de erro
    msg_erro = Tk()
    msg_erro.title("Erro")
    mensagem = Label(msg_erro, text=mensagem)
    mensagem.grid(column=0, row=0, padx= 30, pady=20)
    OK_buttom = Button(msg_erro, text="OK", padx=35, pady=10, command= msg_erro.destroy)
    OK_buttom.grid(column=0, row=1, padx= 30, pady=20)
    msg_erro.mainloop()


def novo_triangulo():           #coloca os dados de vetor_X e vetor_Y na estrutura triangulo[]
    pares = list(zip(vetor_X, vetor_Y, vetor_cor))
    pares = sorted(pares, key=lambda par: par[1])#ordena os pares com y como referencia


    triangulo.append(triangulos(nome="Triangulo"))
    vertice_aux = ''
    vertice_aux = vertice(x=pares[0][0], y=pares[0][1], cor=pares[0][2])
    triangulo[0].A = vertice_aux
    
    vertice_aux = vertice(x=pares[1][0], y=pares[1][1], cor=pares[1][2])
    triangulo[0].B = vertice_aux
    
    vertice_aux = vertice(x=pares[2][0], y=pares[2][1], cor=pares[2][2])
    triangulo[0].C = vertice_aux

    triangulo[0].arestas()


def retorna_ponto(event):       #cria um vetor no espaço de trabalho, e após o terceiro chama fill
    coord_x = event.x
    coord_y = event.y
    janela_desenho.create_oval(coord_x-3, coord_y-3, coord_x+3, coord_y+3, fill=cor_vertice)
    janela_desenho.create_text(coord_x+42, coord_y-5, text=f'''(x: {coord_x}; y: {coord_y})''')
    vetor_X.append(coord_x)
    vetor_Y.append(coord_y)
    vetor_cor.append(cor_vertice)

    if len(vetor_X) >= 3:
        if verifica_triangulo() == False:
            limpa_tela()
            vetor_X.clear()
            vetor_Y.clear()
            vetor_cor.clear()
            msg_erro("Os pontos não formam um triângulo\n Tente novamente")
        else:
            novo_triangulo()
            objeto_txt["text"] = f'''Coordenadas do triangulo:\nA = [{vetor_X[0]}, {vetor_Y[0]}]\nB = [{vetor_X[1]}, {vetor_Y[1]}]\nC = [{vetor_X[2]}, {vetor_Y[2]}]'''
            vetor_X.clear()
            vetor_Y.clear()
            vetor_cor.clear()
           
            fill_poly()

triangulo = []
vetor_X = []
vetor_Y = []
vetor_cor = []
cor_vertice = "#888888"

tela = Tk()
tela.title("Trabalho CG")

janela_desenho = Canvas(tela, width=t_width, height=t_height, relief = "solid", bd=1) #define a tela, seu tipo e a borda de desenho
janela_desenho.pack(padx=3, pady=3) #borda de visualização
janela_desenho.grid(column=0, row=0)

janela_desenho.bind("<Motion>", local_ponteiro) 
bindID = janela_desenho.bind("<Button-1>", retorna_ponto)


objeto_txt = Label(tela, text="Coordenadas do triangulo:")
objeto_txt.grid(column=1, row=0)
botao = Button(tela, text="Alterar a cor do vértice", command=alterar_cor)
botao.grid(column=1, row=1)
botao = Button(tela, text="Limpar a tela", command=limpa_tela)
botao.grid(column=1, row=2)

ponteiro_txt = Label(tela, text="")
ponteiro_txt.grid(column=0, row=1)

tela.mainloop()