import cv2 # Importa o pacote OpenCV
import numpy as np # Importa o pacote numpy e o renomeia como np

# Carrega a imagem "imagemteste.jpg" em escala de cinza
image = cv2.imread('C:/Users/mavic/TCC/imagemteste.jpg', 0) 

# Cria um objeto "params" da classe "SimpleBlobDetector_Params()"
params = cv2.SimpleBlobDetector_Params()

# Define os parâmetros de detecção de blobs
params.filterByArea = True # Filtra os blobs por área
params.minArea = 80 # Define a área mínima do blob em pixels
params.filterByCircularity = True # Filtra os blobs por circularidade
params.minCircularity = 0.8 # Define a circularidade mínima do blob
params.filterByConvexity = True # Filtra os blobs por convexidade
params.minConvexity = 0.5 # Define a convexidade mínima do blob
params.filterByInertia = True # Filtra os blobs por inércia
params.minInertiaRatio = 0.01 # Define a inércia mínima do blob

# Cria um objeto "detector" da classe "SimpleBlobDetector_create()"
# com base nos parâmetros definidos anteriormente
detector = cv2.SimpleBlobDetector_create(params)

# Detecta os blobs circulares na imagem usando o objeto "detector"
keypoints = detector.detect(image)

# Cria uma matriz vazia (blank) com a função "np.zeros()"
blank = np.zeros((1, 1))

# Desenha os blobs circulares na imagem
blobs = cv2.drawKeypoints(image, keypoints, blank, (0, 0, 255),
                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Conta o número de blobs circulares detectados e cria uma string de texto
number_of_blobs = len(keypoints)
text = "Number of Circular Blobs: " + str(len(keypoints))

# Adiciona o texto à imagem desenhada
cv2.putText(blobs, text, (20, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)

# Exibe a imagem com os blobs circulares destacados
cv2.imshow("Filtering Circular Blobs Only", blobs)

# Aguarda por uma tecla do usuário para fechar a janela exibida
cv2.waitKey(0)

# Fecha todas as janelas abertas
cv2.destroyAllWindows()
