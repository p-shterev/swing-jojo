import pygame as p

WIDTH = 480
HEIGHT = 700
MAX_FPS = 120
OFFSET = 50
GAME_SPEED = 2
ARMATURE_SPACE = 200
JOJO_FAN_OFFSET = 2

GROUND_RATIO = .29
GRASS_RATIO = .02
BUILDINGS_RATIO = .42
CLOUDS_RATIO = .7
BUTTON_RATIO = .85

HAMMER_X_OFFSET = 56
HAMMER_Y_OFFSET = 25
HAMMER_SPEED = .15

IMAGES = {
    'HAMMER': p.image.load("resources/assets/Hammer.png").convert_alpha(),
    'ARMATURE': p.image.load("resources/assets/armature.png").convert_alpha(),
    'BUILDINGS': p.image.load("resources/assets/buildings.png").convert_alpha(),
    'GROUND': p.image.load("resources/assets/ground.png").convert_alpha(),
    'BUTTON': {
        "CHANGE": p.image.load("resources/assets/buttons/button_change.png").convert_alpha(),
        "START": p.image.load("resources/assets/buttons/button_start.png").convert_alpha(),
        "AI_START": p.image.load("resources/assets/buttons/button_start_AI.png").convert_alpha(),
        "BACK": p.image.load("resources/assets/buttons/button_back.png").convert_alpha()
    },
    'BACKGROUND': [
        p.image.load("resources/assets/background/blue.png").convert_alpha(),
        p.image.load("resources/assets/background/orange.png").convert_alpha(),
        p.image.load("resources/assets/background/purple.png").convert_alpha()
    ],
    'CLOUDS': [
        p.image.load("resources/assets/cloud/blue.png").convert_alpha(),
        p.image.load("resources/assets/cloud/orange.png").convert_alpha(),
        p.image.load("resources/assets/cloud/purple.png").convert_alpha()
    ],
    'FAN': [
        p.image.load("resources/assets/fan/fan_1.png").convert_alpha(),
        p.image.load("resources/assets/fan/fan_2.png").convert_alpha(),
        p.image.load("resources/assets/fan/fan_3.png").convert_alpha(),
        p.image.load("resources/assets/fan/fan_4.png").convert_alpha()
    ],
    'TITLE': [
        p.image.load("resources/assets/title/title_1.png").convert_alpha(),
        p.image.load("resources/assets/title/title_2.png").convert_alpha(),
        p.image.load("resources/assets/title/title_3.png").convert_alpha(),
        p.image.load("resources/assets/title/title_4.png").convert_alpha()
    ],
    'JOJO': [
        [
            p.image.load("resources/assets/jojo/white/white_jojo_1.png").convert_alpha(),
            p.image.load("resources/assets/jojo/white/white_jojo_2.png").convert_alpha(),
            p.image.load("resources/assets/jojo/white/white_jojo_3.png").convert_alpha()
        ], [
            p.image.load("resources/assets/jojo/red/red_jojo_1.png").convert_alpha(),
            p.image.load("resources/assets/jojo/red/red_jojo_2.png").convert_alpha(),
            p.image.load("resources/assets/jojo/red/red_jojo_3.png").convert_alpha()
        ], [
            p.image.load("resources/assets/jojo/pink/pink_1.png").convert_alpha(),
            p.image.load("resources/assets/jojo/pink/pink_2.png").convert_alpha(),
            p.image.load("resources/assets/jojo/pink/pink_3.png").convert_alpha()
        ], [
            p.image.load("resources/assets/jojo/yellow/yellow_jojo_1.png").convert_alpha(),
            p.image.load("resources/assets/jojo/yellow/yellow_jojo_2.png").convert_alpha(),
            p.image.load("resources/assets/jojo/yellow/yellow_jojo_3.png").convert_alpha()
        ], [
            p.image.load("resources/assets/jojo/helmet/helmet_jojo_1.png").convert_alpha(),
            p.image.load("resources/assets/jojo/helmet/helmet_jojo_2.png").convert_alpha(),
            p.image.load("resources/assets/jojo/helmet/helmet_jojo_3.png").convert_alpha()
        ]
    ],
    'GAME_OVER': {
        "TEXT": p.image.load("resources/assets/game_over/text_gameover.png").convert_alpha(),
        "PANEL": p.image.load("resources/assets/game_over/score_panel.png").convert_alpha()
    },
    'U_NUMBERS': [
        p.image.load("resources/assets/upper_numbers/0.png").convert_alpha(),
        p.image.load("resources/assets/upper_numbers/1.png").convert_alpha(),
        p.image.load("resources/assets/upper_numbers/2.png").convert_alpha(),
        p.image.load("resources/assets/upper_numbers/3.png").convert_alpha(),
        p.image.load("resources/assets/upper_numbers/4.png").convert_alpha(),
        p.image.load("resources/assets/upper_numbers/5.png").convert_alpha(),
        p.image.load("resources/assets/upper_numbers/6.png").convert_alpha(),
        p.image.load("resources/assets/upper_numbers/7.png").convert_alpha(),
        p.image.load("resources/assets/upper_numbers/8.png").convert_alpha(),
        p.image.load("resources/assets/upper_numbers/9.png").convert_alpha()
    ],
    'L_NUMBERS': [
        p.image.load("resources/assets/lower_numbers/0.png").convert_alpha(),
        p.image.load("resources/assets/lower_numbers/1.png").convert_alpha(),
        p.image.load("resources/assets/lower_numbers/2.png").convert_alpha(),
        p.image.load("resources/assets/lower_numbers/3.png").convert_alpha(),
        p.image.load("resources/assets/lower_numbers/4.png").convert_alpha(),
        p.image.load("resources/assets/lower_numbers/5.png").convert_alpha(),
        p.image.load("resources/assets/lower_numbers/6.png").convert_alpha(),
        p.image.load("resources/assets/lower_numbers/7.png").convert_alpha(),
        p.image.load("resources/assets/lower_numbers/8.png").convert_alpha(),
        p.image.load("resources/assets/lower_numbers/9.png").convert_alpha()
    ],
    'MEDAL': {
        'BRONZE': p.image.load("resources/assets/medals/medal_0.png").convert_alpha(),
        'SILVER': p.image.load("resources/assets/medals/medal_1.png").convert_alpha(),
        'GOLD': p.image.load("resources/assets/medals/medal_2.png").convert_alpha(),
        'PLATINUM': p.image.load("resources/assets/medals/medal_3.png").convert_alpha()
    }
}
