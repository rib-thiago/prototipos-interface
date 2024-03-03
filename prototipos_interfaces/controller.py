# controller.py

import cv2
import pytesseract
import threading

class ShowContentController:
    def __init__(self):
        pass

    def extract_text(self, filename, language='rus'):
        img = cv2.imread(filename)
        resultado = pytesseract.image_to_string(img, lang=language)
        return resultado

#     def show_image(self, image_path):
#         img = cv2.imread(image_path)
#         cv2.imshow('Imagem', img)
#         cv2.waitKey(5000)  # Aguarda 2 segundos antes de continuar
#         cv2.destroyAllWindows()


    def show_image(self, image_path):
        # Define uma função para exibir a imagem
        def display_image(image_path):
            img = cv2.imread(image_path)
            cv2.namedWindow('Imagem', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Imagem', 1000, 600)
            cv2.imshow('Imagem', img)

            while True:
                key = cv2.waitKey(0)
                if key == ord('q'):
                    break

            cv2.destroyAllWindows()

        # Cria e inicia uma thread para exibir a imagem
        image_thread = threading.Thread(target=display_image, args=(image_path,))
        image_thread.start()