from plyer import notification
import winsound


def reproducir_sonido():
    winsound.PlaySound("resources/owl_hooting_48028.wav", winsound.SND_FILENAME)


def getSondNotifyEndConcentration():
    reproducir_sonido()
    notification.notify(
        title="Fin del período",
        message="Es hora de tomar un descanso.",
        app_icon="resources/icono.ico",
        ticker="Pomodoro Buho",
        timeout=10,
    )
