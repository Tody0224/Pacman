import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandController:
    """
    Responsável pela captura da câmera e detecção da direção das mãos
    utilizando o MediaPipe Hand Landmarker.

    O sistema divide a imagem em dois lados:

        - Esquerda  -> Jogador 1
        - Direita   -> Jogador 2

    Para cada jogador é detectada apenas uma mão por quadro.

    A direção é calculada através do vetor médio entre o centro da palma
    e as pontas dos dedos, retornando:

        - CIMA
        - BAIXO
        - ESQUERDA
        - DIREITA
    """

    def __init__(self):
        """
        Inicializa a câmera e o detector de mãos.
        """

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            print("Não foi possível abrir a câmera.")

        base_options = python.BaseOptions(
            model_asset_path="hand_landmarker.task"
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2
        )

        self.detector = vision.HandLandmarker.create_from_options(options)

        self.dead_zone = 0.12

    def get_direction(self):
        """
        Captura um frame da câmera, detecta as mãos presentes e calcula
        a direção apontada por cada jogador.

        Returns
        -------
        list[dict]

        Lista contendo dicionários no formato:

        [
            {
                "jogador": 1,
                "direcao": "CIMA"
            },
            {
                "jogador": 2,
                "direcao": "DIREITA"
            }
        ]

        Caso nenhuma direção seja detectada, retorna uma lista vazia.
        """

        ret, frame = self.camera.read()

        if not ret:
            print("Erro ao capturar imagem da câmera.")
            return None

        frame = cv2.flip(frame, 1)

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )

        result = self.detector.detect(mp_image)

        direcoes = []

        h, w, _ = frame.shape

        cv2.line(
            frame,
            (w // 2, 0),
            (w // 2, h),
            (0, 0, 255),
            2
        )

        jogador_esquerda = False
        jogador_direita = False

        if result.hand_landmarks:

            for hand in result.hand_landmarks:

                direcao = None

                palma = [0, 5, 9, 13, 17]

                px = sum(hand[i].x for i in palma) / len(palma)
                py = sum(hand[i].y for i in palma) / len(palma)

                if px < 0.5:

                    if jogador_esquerda:
                        continue

                    id_jogador = 1
                    jogador_esquerda = True

                else:

                    if jogador_direita:
                        continue

                    id_jogador = 2
                    jogador_direita = True

                dedos = [
                    (4, 0.5),
                    (8, 1.0),
                    (12, 1.5),
                    (16, 1.0),
                    (20, 0.5)
                ]

                dx = 0.0
                dy = 0.0
                peso_total = 0.0

                for idx, peso in dedos:

                    dx += (hand[idx].x - px) * peso
                    dy += (hand[idx].y - py) * peso

                    peso_total += peso

                dx /= peso_total
                dy /= peso_total

                tamanho = (dx * dx + dy * dy) ** 0.5

                if tamanho > 0:

                    dx /= tamanho
                    dy /= tamanho

                LIMIAR = 0.35

                if abs(dx) > abs(dy):

                    if dx > LIMIAR:
                        direcao = "DIREITA"

                    elif dx < -LIMIAR:
                        direcao = "ESQUERDA"

                else:

                    if dy > LIMIAR:
                        direcao = "BAIXO"

                    elif dy < -LIMIAR:
                        direcao = "CIMA"

                if direcao:

                    direcoes.append(
                        {
                            "jogador": id_jogador,
                            "direcao": direcao
                        }
                    )

                cx = int(px * w)
                cy = int(py * h)

                fx = int((px + dx * 0.20) * w)
                fy = int((py + dy * 0.20) * h)

                cv2.circle(
                    frame,
                    (cx, cy),
                    10,
                    (0, 255, 0),
                    -1
                )

                for idx, _ in dedos:

                    x = int(hand[idx].x * w)
                    y = int(hand[idx].y * h)

                    cv2.circle(
                        frame,
                        (x, y),
                        6,
                        (255, 255, 0),
                        -1
                    )

                    cv2.line(
                        frame,
                        (cx, cy),
                        (x, y),
                        (80, 80, 80),
                        1
                    )

                cv2.arrowedLine(
                    frame,
                    (cx, cy),
                    (fx, fy),
                    (255, 0, 255),
                    4
                )

                texto = f"Jogador {id_jogador}: {direcao}"

                cv2.putText(
                    frame,
                    texto,
                    (20, 40 + id_jogador * 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

        cv2.imshow(
            "Hand Controller",
            frame
        )

        cv2.waitKey(1)

        return direcoes

    def release(self):
        """
        Libera todos os recursos utilizados pela classe.

        Fecha:
            - câmera;
            - janelas do OpenCV.
        """

        self.camera.release()
        cv2.destroyAllWindows()


controle = HandController()

try:

    while True:

        direcao = controle.get_direction()

        if direcao:
            print(f"Direção detectada: {direcao}")

except KeyboardInterrupt:

    print("\nEncerrando programa...")

finally:

    controle.release()