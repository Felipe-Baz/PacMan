from app_class import *
from moviepy.editor import *

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("PacMan - By FelipeBazCode")

    while True:
        print("[1] Musica 1: Dirty Ninoff Fantastic: ")
        print("[2] Musica 2: PacMan Theme remix")
        music_choose = 0
        print("qual sera a musica de hj? 1 ou 2:")
        music_choose = int(input(" "))
        if music_choose == 1 or music_choose == 2:
            if int(input("tamo de testezada? [0 ou 1]")):
                atual_score = {"HighScore": 0}
                # salva as informações do dicionario de informações relevantes em um arquivo .json para analise
                with open(f'data/HighScore.json', 'w') as json_file:
                    json.dump(atual_score, json_file, indent=3, ensure_ascii=False)
                json_file.close()
            break

    video = VideoFileClip('data/IntroFinalVersion.mp4')
    video.preview()

    # Inicializa o mixer de audio
    pygame.mixer.init()
    # Carrega a musica
    if music_choose == 1:
        pygame.mixer.music.load("data/music/Dirty_Ninoff_Fantastic.mp3")
        pygame.mixer.music.set_volume(0.3)
    else:
        pygame.mixer.music.load("data/music/Pac_man_theme_remix.mp3")
        # Configura o som
        pygame.mixer.music.set_volume(0.1)
    # Começa a tocar a musica
    pygame.mixer.music.play(loops=-1)
    app = App()
    app.run()
