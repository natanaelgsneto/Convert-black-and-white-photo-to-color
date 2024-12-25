#Colorir uma imagem preto e branco para colorido pode ser um processo complexo, pois requer a reconstrução das cores que não estão presentes na imagem original. Esse processo normalmente é feito usando redes neurais treinadas em grandes conjuntos de dados. No entanto, é possível criar uma implementação básica usando bibliotecas de Python como OpenCV e modelos pré-treinados.

#Aqui está um exemplo simples de como colorir uma imagem em preto e branco usando o OpenCV e um modelo pré-treinado para colorização:


import cv2
import numpy as np

# Baixe os arquivos do modelo pré-treinado:
# 1. Model: https://github.com/richzhang/colorization/raw/master/models/colorization_deploy_v2.prototxt
# 2. Weights: https://github.com/richzhang/colorization/raw/master/models/colorization_release_v2.caffemodel
# 3. Cluster centers: https://github.com/richzhang/colorization/raw/master/resources/pts_in_hull.npy

# Carregando os arquivos do modelo
prototxt = "colorization_deploy_v2.prototxt"
caffemodel = "colorization_release_v2.caffemodel"
pts_in_hull = "pts_in_hull.npy"

# Carrega o modelo
net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
pts = np.load(pts_in_hull)

# Adiciona os pontos do cluster ao modelo
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype(np.float32)]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

# Carregando a imagem em escala de cinza
input_image = cv2.imread("imagem_preto_branco.jpg")
input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
input_image = cv2.cvtColor(input_image, cv2.COLOR_GRAY2RGB)

# Prepara a imagem para o modelo
scaled = input_image.astype("float32") / 255.0
lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2LAB)
resized = cv2.resize(lab, (224, 224))  # Dimensão necessária pelo modelo
L = resized[:, :, 0]
L -= 50

# Passa a imagem pelo modelo
net.setInput(cv2.dnn.blobFromImage(L))
ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

# Redimensiona para as dimensões originais
ab = cv2.resize(ab, (input_image.shape[1], input_image.shape[0]))
L = lab[:, :, 0]
colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

# Converte para RGB
colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2RGB)
colorized = np.clip(colorized, 0, 1)

# Converte para 8 bits
colorized = (255 * colorized).astype("uint8")

# Salva e exibe o resultado
cv2.imwrite("imagem_colorida.jpg", colorized)
cv2.imshow("Colorized Image", colorized)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Requisitos
#Bibliotecas Necessárias:
#opencv-python
#numpy
#Arquivos do Modelo:
#Faça o download dos arquivos indicados no início do código.
#Explicação
#O modelo usado é um modelo Caffe pré-treinado para colorização de imagens.
#Ele utiliza o espaço de cores LAB, onde L representa a luminosidade e os canais A e B representam as informações de cor.
#Observação
#Para resultados melhores, considere usar uma rede neural moderna como uma U-Net ou um modelo treinado em frameworks como TensorFlow ou PyTorch.
