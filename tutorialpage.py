from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp

class TutorialPage(Screen):
    pass

class TutorialPageModel(RelativeLayout):
    tutorial_text = """Seja bem-vindo ao CifraNote!!

Desenvolvi esse aplicativo para
servir como bloco de notas para
cifras, com a funcionalidade
especial de trocar o tom das
cifras.

-- Criando uma cifra
  Para criar uma nova cifra, clique
no botão de "+" na página inicial.
Você será redirecionado à tela de 
criação de cifras. 
  Para alterar o conteúdo da cifra, 
clique na caixa de texto que diz 
"Digite a cifra". Para escolher
o nome da cifra, selecione a frase 
"Nova cifra" e digite o título 
desejado.
  Caso deseje especificar o tom
da cifra, clique no botão de texto 
"Tom: Auto" e escolha o tom desejado.
Caso não escolha o tom da cifra, o 
aplicativo tentará reconhecer o tom
automaticamente. 
  Por fim, quando terminar de criar a 
cifra, basta apertar no botão de "v", 
no canto superior direito da tela, para
salvar a cifra criada. Caso queira deletar 
o que criou, clique no botão "x", no canto 
superior esquerdo da tela, e confirme para 
exclusão.

-- Excluindo uma cifra
  Para excluir uma cifra, basta
apertar e segurar em seu nome na 
página inicial, até aparecer a opção
"Excluir". Confirme.

-- Editando uma cifra
  Para editar uma cifra, clique em
seu nome na tela inicial.
  Para trocar o tom de uma cifra,
use os botões "-Semitom" e "+Semitom", 
localizados na barra superior, para 
diminuir ou aumentar em um semitom a
cifra, respectivamente. Caso queira saber
qual é o tom da cifra, use o visor "Tom" 
para se guiar.
  Caso queira trocar o tom de uma parte 
específica da cifra, selecione o texto desejado
e use os botões "-Semitom" e "+Semitom" para
alterar o tom do texto selecionado sem alterar
a cifra inteira.
  
-- Agradecimento
  Bom, obrigado por ler até aqui.
Espero que esse aplicativo possa 
ser útil e o ajudar na edição de
cifras. Caso veja algo de errado,
manda mensagem pelo email 
"controlfelipe86@gmail.com" 
reportando o erro (se possível com prints). É isso. Obrigado.

-- Crédito
Github: @Felifelps
App por Felifelps"""
 
    def back_to_mainpage(self):
        self.root.manager.current = "mainpage"
        