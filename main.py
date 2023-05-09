from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.popup import Popup
import cv2 
import os
import shutil
import tempfile
import datetime
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import numpy as np
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window


class MyLabel(Label):
    def __init__(self, **kwargs):
        super(MyLabel, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(source='alpla.png', size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class MainApp(App):
    title = "Simple Video"
    
    def build(self):                
        # Criando o layout inicial
            self.intro_layout = BoxLayout(orientation='vertical')
            self.intro_label = MyLabel(text='', 
                         size_hint=(1, 0.5),
                         font_size=24,
                         bold=True,
                         halign='center',
                         color= ( 95, 158, 160, 1 ))

            self.intro_layout.add_widget(self.intro_label)
            self.start_button = Button(text='Começar', size_hint=(1, 0.1), background_normal='ini.png')
            self.start_button.bind(on_press=self.show_main_layout)
            self.intro_layout.add_widget(self.start_button)
        
        
            self.layout = BoxLayout(orientation='vertical')
            self.capture = None
            self.playing = True
            self.file_created = False  # variável de controle para verificar se um arquivo já foi criado


            self.clock_event = None

            # Adicionando o player de vídeo à layout
            self.img1 = Image(source='manual.png')
            self.img1.size_hint = (1, 1)  # Definindo o size_hint para 70% de altura
            with self.img1.canvas.before:
                Window.clearcolor = (0.660, 0.650, 0.660, 0.01)
                # Color(1, 0, 0, 1) # vermelho
                self.rect = Rectangle(size=self.img1.size, pos=self.img1.pos)
                
            self.layout.add_widget(self.img1)
            # Criando um BoxLayout horizontal para agrupar os botões de Play e Selecionar arquivo
            self.button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
            

            # Adicionando um botão para abrir o filechooser
            select_button = Button(text='Selecionar arquivo', background_normal='bgf.png',
                        background_down='bgpa.png')
            select_button.bind(on_press=self.show_filechooser)
            select_button.size_hint = (0.5, 0.7)  # Definindo o size_hint do botão Selecionar arquivo para ocupar metade da largura
            self.button_layout.add_widget(select_button)
            # Adicionando o BoxLayout com os botões à layout principal
            self.layout.add_widget(self.button_layout)
            
            self.y_input = TextInput(text='', multiline=False, hint_text='O valor padrão da altura da linha é 267, caso deseje alterar digite um novo valor neste espaço e aperte "Enter"')
            self.y_input.bind(on_text_validate=self.update_y)
            self.y_input.size_hint = (1, 0.1)  # Definindo o size_hint para 10% de altura
            self.layout.add_widget(self.y_input)
            
            self.play_button = Button(text='Play', on_press=self.toggle_play_pause,
                            background_normal='ini.png',
                            background_down='bgpa.png')
            self.play_button.size_hint = (0.5, 0.7)  # Definindo o size_hint do botão Play para ocupar metade da largura
            self.button_layout.add_widget(self.play_button)
         
            self.stop_clock()

            return self.intro_layout

    def show_main_layout(self, instance):
        # Trocando o layout atual pelo layout principal
        self.root.clear_widgets()
        self.root.add_widget(self.layout)
            

    def update_y(self, instance):
        try:
            self.yl = int(instance.text)
        except ValueError:
            pass
        
    def create_temporary_copy(self, path):
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, 'temp_file_name')
        shutil.copy2(path, temp_path)
        return temp_path
            
    def show_filechooser(self, *args):
        
        # Criando o filechooser e definindo a ação a ser tomada quando o arquivo é selecionado
        filechooser = FileChooserListView(filters= [lambda folder, filename: not filename.endswith('.sys')])
        filechooser.path = "C://Users"
        filechooser.bind(on_submit=self.play_video)
        # Exibindo o filechooser em uma janela popup
        self.popup = Popup(title='Selecione o arquivo de vídeo', content=filechooser, size_hint=(0.9, 0.9))
        self.popup.open()
    
    
    def start_clock(self):
        self.clock_event = Clock.schedule_interval(self.update, 1.0 / 30.0)

    def stop_clock(self):
        if self.clock_event:
            self.clock_event.cancel()

    def toggle_play_pause(self, instance):
        self.playing = not self.playing
        
        if self.playing:
            self.play_button.text = 'Pause'
            self.play_button.background_normal='bgpa.png'
            self.start_clock()
        else:
            self.play_button.text = 'Play'
            self.play_button.background_normal='ini.png'
            self.stop_clock()
    

    def play_video(self, filechooser,submit, teste):
        self.popup.dismiss()
        
        capture = cv2.VideoCapture(filechooser.selection[0])
        self.capture=capture
        now = datetime.datetime.now()
        self.file_created = "alturas_{}.txt".format(now.strftime("%Y-%m-%d_%H-%M-%S"))

            
    def update(self,dt):
        
            if self.capture is None:
                return 
            
            now = datetime.datetime.now()
            filename = self.file_created
     
            if self.file_created:
                # arquivo já foi criado, não precisa criar um novo arquivo
                pass
            elif os.path.exists(filename):
                # arquivo já existe, mas ainda não foi criado para esta sessão do programa
                self.file_created = True
            else:
                # arquivo ainda não existe, cria um novo arquivo e define a variável de controle como True
                with open(filename, "w") as arquivo:
                   filename = "alturas_{}.txt".format(now.strftime("%Y-%m-%d_%H-%M"))
                self.file_created = True
                    
            
            # Cria o objeto "params" e configura os parâmetros de detecção de blobs
            params = cv2.SimpleBlobDetector_Params()
            params.filterByArea = True
            params.minArea = 80
            params.filterByCircularity = True
            params.minCircularity = 0.8
            params.filterByConvexity = True
            params.minConvexity = 0.2
            params.filterByInertia = True
            params.minInertiaRatio = 0.01
            detector = cv2.SimpleBlobDetector_create(params)

            # Cria uma matriz vazia para desenhar os blobs
            blank = np.zeros((1, 1))
            # Loop para ler cada quadro do vídeo, detectar os blobs e exibir o resultado
            ret, frame = self.capture.read()
            if hasattr(self, 'yl'):
                yl = self.yl
            else:
                yl = 267
            if ret:
                # y = 267
                x1 = 0
                x2 = frame.shape[1]

                cv2.line(frame, (x1, yl), (x2, yl), (0, 0, 255), thickness=2)
                # Converte o quadro para escala de cinza
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detecta os blobs na imagem
                keypoints = detector.detect(gray)

            # Desenha os blobs na imagem
                blobs = cv2.drawKeypoints(frame, keypoints, blank, (0, 0, 255),
                                    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                escala_pixels_por_cm = 10  # supondo que a escala do vídeo é de 10 pixels por centímetro
                
                for keyPoint in keypoints:
                    x, y = keyPoint.pt
                    # Calcula a altura do centro do blob em relação à linha traçada na horizontal do vídeo em pixels
                    height_pixels = abs(y - yl)
                    # Calcula a altura do centro do blob em relação à linha traçada na horizontal do vídeo em centímetros
                    height_cm = height_pixels / escala_pixels_por_cm
                    # Imprime a altura em centímetros no console
                    print("Altura em x=", x, ":", height_cm, "cm")
                    # Imprime a altura em centímetros no console
                    altura_texto = "{:.2f} cm".format(height_cm)
                    # Atualiza o texto do Label
                    # self.label.text = altura_texto
                    
                    line_length = int(height_pixels)
                    x_center = int(keypoints[0].pt[0]) # coordenada x do centro do blob
                    y_center = int(keypoints[0].pt[1]) # coordenada y do centro do blob
                    cv2.line(blobs, (x_center, y_center), (x_center, yl), (255, 0, 0), thickness=2)
                    # Desenha o texto com a altura em centímetros no centro do blob
                    cv2.putText(blobs, "{:.2f} cm".format(height_cm), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    print("{:.2f} cm".format(height_cm))
                    altura_cm = "{:.2f} cm".format(height_cm)
                    print("blobs ------------- ",blobs[0])
                    
                    with open(filename, "a") as arquivo:
                            arquivo.write(altura_texto + "\n")
                    
                # convert it to texture
                buf1 = cv2.flip(blobs, 0)
                buf = buf1.tostring()
                texture1 = Texture.create(size=(blobs.shape[1], blobs.shape[0]), colorfmt='bgr') 
                #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
                texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                # display image from the texture
                self.img1.texture = texture1
            
MainApp().run()

cv2.destroyAllWindows()

