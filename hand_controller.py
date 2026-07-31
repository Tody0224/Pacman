import math

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandController:
    """Controla a captura e interpretação de gestos das mãos utilizando MediaPipe."""

    def __init__(self) -> None:
        """Inicializa a câmera, o detector de mãos e os parâmetros do controlador."""
        cv2.namedWindow("Hand Controller")
        self.camera = cv2.VideoCapture(0, cv2.CAP_MSMF)

        if not self.camera.isOpened():
            print("Não foi possível abrir a câmera.")

        base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=4,
        )

        self.detector = vision.HandLandmarker.create_from_options(options)
        self.dead_zone = 0.25

    def get_direction(self) -> list[dict[str, int | str]] | str | None:
        """
        Captura um frame da câmera e identifica ações realizadas pelas mãos.

        Returns:
            list[dict[str, int | str]]:
                Lista de ações detectadas. Cada item possui:
                - jogador: ID do jogador (1 ou 2)
                - mao: Número da mão detectada (1 ou 2)
                - acao: Direção ou gesto identificado.
            str:
                Retorna `"SAIR"` caso o usuário feche a janela ou pressione
                `ESC` ou `Q`.
            None:
                Retorna `None` caso ocorra erro na captura do frame.
        """
        ret, frame = self.camera.read()

        if not ret:
            print("Erro ao capturar imagem da câmera.")
            return None

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb,
        )

        result = self.detector.detect(mp_image)

        acoes: list[dict[str, int | str]] = []

        cv2.line(frame, (w // 2, 0), (w // 2, h), (0, 0, 255), 2)

        maos_esquerda = 0
        maos_direita = 0

        if result.hand_landmarks:
            for hand in result.hand_landmarks:
                acao_atual: str | None = None

                palma = [0, 5, 9, 13, 17]
                pulso = hand[0]

                px = (sum(hand[i].x for i in palma) / len(palma)) * w
                py = (sum(hand[i].y for i in palma) / len(palma)) * h

                if px < (w / 2):
                    if maos_esquerda >= 2:
                        continue

                    id_jogador = 1
                    maos_esquerda += 1
                    id_mao = maos_esquerda
                else:
                    if maos_direita >= 2:
                        continue

                    id_jogador = 2
                    maos_direita += 1
                    id_mao = maos_direita

                dedos_info = [
                    (8, 6),
                    (12, 10),
                    (16, 14),
                    (20, 18),
                ]

                dedos_levantados: list[bool] = []

                for ponta, meio in dedos_info:
                    dist_ponta = math.hypot(
                        (hand[ponta].x - pulso.x) * w,
                        (hand[ponta].y - pulso.y) * h,
                    )

                    dist_meio = math.hypot(
                        (hand[meio].x - pulso.x) * w,
                        (hand[meio].y - pulso.y) * h,
                    )

                    dedos_levantados.append(dist_ponta > dist_meio)

                total_levantados = sum(dedos_levantados)

                if total_levantados == 0:
                    acao_atual = "BOMBA"

                elif dedos_levantados == [True, True, False, False]:
                    acao_atual = "PAUSA"

                else:
                    dedos = [8, 12, 16, 20]

                    dx = 0.0
                    dy = 0.0

                    for idx in dedos:
                        dx += (hand[idx].x * w) - px
                        dy += (hand[idx].y * h) - py

                    dx /= len(dedos)
                    dy /= len(dedos)

                    magnitude = math.hypot(dx, dy)

                    if magnitude > 10:
                        nx = dx / magnitude
                        ny = dy / magnitude

                        if abs(nx) > abs(ny) + self.dead_zone:
                            acao_atual = (
                                "DIREITA"
                                if nx > 0
                                else "ESQUERDA"
                            )

                        elif abs(ny) > abs(nx) + self.dead_zone:
                            acao_atual = (
                                "BAIXO"
                                if ny > 0
                                else "CIMA"
                            )

                if acao_atual:
                    acoes.append(
                        {
                            "jogador": id_jogador,
                            "mao": id_mao,
                            "acao": acao_atual,
                        }
                    )

                cx, cy = int(px), int(py)

                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

                for idx in [8, 12, 16, 20]:
                    x = int(hand[idx].x * w)
                    y = int(hand[idx].y * h)

                    cv2.circle(frame, (x, y), 6, (255, 255, 0), -1)
                    cv2.line(frame, (cx, cy), (x, y), (80, 80, 80), 1)

                if acao_atual not in {"BOMBA", "PAUSA"}:
                    fx = int(px + dx * 1.5)
                    fy = int(py + dy * 1.5)

                    cv2.arrowedLine(
                        frame,
                        (cx, cy),
                        (fx, fy),
                        (255, 0, 255),
                        4,
                    )

                cor_texto = (
                    (0, 255, 255)
                    if acao_atual in {"BOMBA", "PAUSA"}
                    else (0, 255, 0)
                )

                pos_x = 20 if id_jogador == 1 else (w // 2) + 20
                pos_y = 40 + (id_mao * 40)

                texto = (
                    f"J{id_jogador} M{id_mao}: "
                    f"{acao_atual if acao_atual else '---'}"
                )

                cv2.putText(
                    frame,
                    texto,
                    (pos_x, pos_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    cor_texto,
                    2,
                )

        cv2.imshow("Hand Controller", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27 or key == ord("q"):
            return "SAIR"

        try:
            if (
                cv2.getWindowProperty(
                    "Hand Controller",
                    cv2.WND_PROP_VISIBLE,
                )
                < 1
            ):
                return "SAIR"

        except cv2.error:
            return "SAIR"

        return acoes

    def release(self) -> None:
        """Libera os recursos utilizados pela câmera e fecha as janelas do OpenCV."""
        self.camera.release()
        cv2.destroyAllWindows()


controle = HandController()

try:
    print("Iniciando controle...")
    print(
        "SÍMBOLOS:\n"
        " - Mão Aberta: Move (Cima, Baixo, Esq, Dir)\n"
        " - Mão Fechada (Punho): BOMBA\n"
        " - Símbolo de Paz (V): PAUSA"
    )
    print("Aperte 'Q' ou 'ESC' na janela da câmera para sair.\n")

    while True:
        resultado = controle.get_direction()

        if resultado == "SAIR":
            break

        if isinstance(resultado, list):
            for evento in resultado:
                print(
                    f"Jogador {evento['jogador']} "
                    f"(Mão {evento['mao']}) "
                    f"executou: {evento['acao']}"
                )

except KeyboardInterrupt:
    print("\nEncerrando...")

finally:
    controle.release()