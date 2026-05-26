class PacManConfig:
    radious = 16
    frame_interval = 0.2
    color = (0, 240, 255)
    angle = 50
    speed = 3
    position = [8, 8]

class Config:
    pacman_config = PacManConfig()
    window_name = "pac_man"
    fps = 60
    map_size = (16, 16)
    tile_size = 40

config = Config()