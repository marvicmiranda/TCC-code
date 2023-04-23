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
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import numpy as np

class MainApp(App):
    title = "Simple Video"

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.capture = None
       # Adicionando o player de vídeo à layout
        self.img1= Image()
        self.layout.add_widget(self.img1)
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        # Adicionando um botão para abrir o filechooser
        button = Button(text='Selecione o vídeo')
        button.bind(on_press=self.show_filechooser)
        self.layout.add_widget(button)
         
        return self.layout

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
        

    def play_video(self, filechooser,submit, teste):
        self.popup.dismiss()
 
        capture = cv2.VideoCapture(filechooser.selection[0])
        self.capture=capture
        
    def update(self,dt):
        
        if self.capture is None:
            return 
        # cap = self.capture 
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
        if ret:
            y = 267
            x1 = 0
            x2 = frame.shape[1]

            cv2.line(frame, (x1, y), (x2, y), (0, 0, 255), thickness=2)
            # Converte o quadro para escala de cinza
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detecta os blobs na imagem
            keypoints = detector.detect(gray)

        # Desenha os blobs na imagem
            blobs = cv2.drawKeypoints(frame, keypoints, blank, (0, 0, 255),
                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            escala_pixels_por_cm = 10  # supondo que a escala do vídeo é de 50 pixels por centímetro

            for keyPoint in keypoints:
                x, y = keyPoint.pt
                # Calcula a altura do centro do blob em relação à linha traçada na horizontal do vídeo em pixels
                height_pixels = abs(y - 267)
                # Calcula a altura do centro do blob em relação à linha traçada na horizontal do vídeo em centímetros
                height_cm = height_pixels / escala_pixels_por_cm
                # Imprime a altura em centímetros no console
                print("Altura em x=", x, ":", height_cm, "cm")

                # height_cm = height_pixels * 0.03 # altura em cm
                line_length = int(height_pixels)
                x_center = int(keypoints[0].pt[0]) # coordenada x do centro do blob
                y_center = int(keypoints[0].pt[1]) # coordenada y do centro do blob
                cv2.line(blobs, (x_center, y_center), (x_center, 267), (255, 0, 0), thickness=2)
                # Desenha o texto com a altura em centímetros no centro do blob
                cv2.putText(blobs, "{:.2f} cm".format(height_cm), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Exibe o resultado em uma janela
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