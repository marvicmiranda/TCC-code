import cv2
if 'bgsegm' in dir(cv2):
    print("O módulo bgsegm está disponível.")
else:
    print("O módulo bgsegm não está disponível.")