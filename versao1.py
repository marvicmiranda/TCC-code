import cv2
import numpy as np
import math


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

# Captura o vídeo
VIDEO = "C:/Users/mavic/TCC/TCC-code/videoteste.mp4"
cap = cv2.VideoCapture(VIDEO)


# Loop para ler cada quadro do vídeo, detectar os blobs e exibir o resultado
while cap.isOpened():
    ret, frame = cap.read()
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
        escala_pixels_por_cm = 50  # supondo que a escala do vídeo é de 50 pixels por centímetro

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
        cv2.imshow('V.1.0', blobs)

        # Aguarda por uma tecla do usuário para sair
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    else:
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
