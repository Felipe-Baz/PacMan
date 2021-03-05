from app_class import *

if __name__ == '__main__':
    # Inicializa o mixer de audio
    pygame.mixer.init()
    # Carrega a musica
    pygame.mixer.music.load("data/Dirty_Ninoff_Fantastic.mp3")
    # Configura o som
    pygame.mixer.music.set_volume(0.3)
    # Começa a tocar a musica
    pygame.mixer.music.play(loops=-1)
    app = App()
    app.run()
