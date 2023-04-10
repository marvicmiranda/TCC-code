import cv2
import numpy as np
import math
import sys


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

algorithm_types = ['GMG', 'MOG2', 'MOG', 'KNN', 'CNT']
algorithm_type = algorithm_types[2]

# Captura o vídeo
VIDEO = "C:/Users/mavic/TCC/TCC-code/videoteste.mp4"


def Kernel(KERNEL_TYPE):
    if KERNEL_TYPE == 'dilation':
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    if KERNEL_TYPE == 'opening':
        kernel = np.ones((3, 3), np.uint8)
    if KERNEL_TYPE == 'closing':
        kernel = np.ones((3, 3), np.uint8)
    return kernel


def Filter(img, filter):
    if filter == 'closing':
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, Kernel('closing'), iterations=2)
    if filter == 'opening':
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, Kernel('opening'), iterations=2)
    if filter == 'dilation':
        return cv2.dilate(img, Kernel('dilation'), iterations=2)
    if filter == 'combine':
        closing = cv2.morphologyEx(
            img, cv2.MORPH_CLOSE, Kernel('closing'), iterations=2)
        opening = cv2.morphologyEx(
            closing, cv2.MORPH_OPEN, Kernel('opening'), iterations=2)
        dilation = cv2.dilate(opening, Kernel('dilation'), iterations=2)
        return dilation


def Subtractor(algorithm_type):
    if algorithm_type == 'GMG':
        return cv2.bgsegm.createBackgroundSubtractorGMG()
    if algorithm_type == 'MOG':
        return cv2.bgsegm.createBackgroundSubtractorMOG()
    if algorithm_type == 'MOG2':
        return cv2.createBackgroundSubtractorMOG2()
    if algorithm_type == 'KNN':
        return cv2.createBackgroundSubtractorKNN()
    if algorithm_type == 'CNT':
        return cv2.bgsegm.createBackgroundSubtractorCNT()
    print('Detector inválido')
    sys.exit(1)


cap = cv2.VideoCapture(VIDEO)
background_subtractor = Subtractor(algorithm_type)

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
            # coordenada x do centro do blob
            x_center = int(keypoints[0].pt[0])
            # coordenada y do centro do blob
            y_center = int(keypoints[0].pt[1])
            cv2.line(blobs, (x_center, y_center),
                     (x_center, 267), (255, 0, 0), thickness=2)
            # Desenha o texto com a altura em centímetros no centro do blob
            cv2.putText(blobs, "{:.2f} cm".format(height_cm), (int(
                x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        mask = background_subtractor.apply(blobs)
        mask_Filter = Filter(mask, 'combine')
        walk_after_mask = cv2.bitwise_and(blobs, blobs, mask=mask_Filter)
        # Exibe o resultado em uma janela
        cv2.imshow('V.1.0', blobs)
        cv2.imshow('Mask', mask)
        cv2.imshow('Mask Filter', mask_Filter)
        cv2.imshow('Final', walk_after_mask)
        # Aguarda por uma tecla do usuário para sair
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    else:
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
