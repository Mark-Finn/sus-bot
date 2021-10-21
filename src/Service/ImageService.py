from datetime import datetime
from random import shuffle
from typing import Tuple, List

from PIL import Image, ImageDraw, ImageFont

class ImageService:

    def __init__(self, base_directory: str, color_palette: dict) -> None:
        self.base_directory: str = base_directory
        self.color_palette: dict = color_palette
        self.CREWMATE_SIZE = (150, 192)
        self.SIDE_MARGIN = 50
        self.PADDING = 60
        self.TOP_SIZE = 400
        self.NAME_SIZE = 62
        self.TITLE_SIZE = 150
        self.TITLE_Y_POSITION = 70
        self.CREWMATE_COLOR = (0, 0, 255)
        self.IMPOSTOR_COLOR = (255, 0, 0)
        self.MIN_WIDTH = 1280
        self.CREWMATES_PER_ROW_OPTIONS = [ 6, 5, 4 ]
        self.__background_height = 0
        self.__total_rows = 0
        self.__offset = 0

    def create_victory_screen(self, is_impostor_win: bool, winner_color_pairs: List[Tuple], no_save=False) -> str:
        if is_impostor_win:
            title = 'Impostors Win!'
            title_color = self.IMPOSTOR_COLOR
        else:
            title = 'Crewmates Win!'
            title_color = self.CREWMATE_COLOR

        winners = map(lambda pairs: pairs[0], winner_color_pairs)
        filename = self.__create_victory_filename(is_impostor_win, winners)
        file = f'{self.base_directory}/img/victory/{filename}.png'

        image = self.__create_image(title, title_color, file, winner_color_pairs)

        if no_save:
            image.show()
        else:
            image.save(file)

        return file

    def create_team_screens(self, crewmate_color_pairs: List[Tuple], impostor_color_pairs: List[Tuple], no_save=False) -> Tuple:
        all_pairs = crewmate_color_pairs + impostor_color_pairs
        shuffle(all_pairs)

        crewmate_filename = 'crewmates'
        crewmate_file = f'{self.base_directory}/img/temp/{crewmate_filename}.png'

        impostor_filename = 'impostors'
        impostor_file = f'{self.base_directory}/img/temp/{impostor_filename}.png'

        sub = f'{len(impostor_color_pairs)}    Impostor' + ('s' if len(impostor_color_pairs) > 1 else '')
        crewmate_image = self.__create_image('Crewmate', self.CREWMATE_COLOR, crewmate_file, all_pairs, sub, self.IMPOSTOR_COLOR)
        impostor_image = self.__create_image('Impostor', self.IMPOSTOR_COLOR, impostor_file, impostor_color_pairs)

        if no_save:
            crewmate_image.show()
            impostor_image.show()
        else:
            crewmate_image.save(crewmate_file)
            impostor_image.save(impostor_file)

        return crewmate_file, impostor_file

    def __create_image(self, title, title_color, file, player_color_pairs: List[Tuple], subtitle=None, subtitle_color=None):
        total_players = len(player_color_pairs)
        split = self.__best_split(self.CREWMATES_PER_ROW_OPTIONS, total_players)
        player_color_pair_chunks = [player_color_pairs[i:i + split] for i in range(0, total_players, split)]

        width = len(player_color_pair_chunks[0]) * self.__crewmate_space()[0] + 2 * self.SIDE_MARGIN
        self.__offset = max(self.MIN_WIDTH - width, 0)
        width += self.__offset

        self.__background_height = len(player_color_pair_chunks) * self.__crewmate_space()[1] + self.TOP_SIZE

        background = Image.open(f'{self.base_directory}/img/space_background.jpg')
        image = background.resize((width, self.__background_height))

        self.__add_title(image, title, title_color, subtitle, subtitle_color)

        players = []
        self.__total_rows = len(player_color_pair_chunks)
        for y_position in range(0, self.__total_rows):
            player_colors = player_color_pair_chunks[y_position]
            for x_position in range(0, len(player_colors)):
                player, color = player_colors[x_position]
                if split != len(player_colors) and self.__total_rows != 1:
                    x_position += (split - len(player_colors) + 1) / len(player_colors)
                image = self.__add_player(image, player, color, (x_position, y_position))
                players.append(player)

        return image

    def __add_title(self, base, title, color, subtitle=None, subtitle_color=None):
        font_file = f'{self.base_directory}/font/ConnectionIii-Rj3W/ConnectionIii-Rj3W.otf'
        font = ImageFont.truetype(font_file, size=self.TITLE_SIZE)

        draw = ImageDraw.Draw(base)

        base_width, _ = base.size
        w_title, h_title = draw.textsize(title, font=font)

        x = int(base_width / 2 - w_title / 2)
        y = self.TITLE_Y_POSITION - 30 if subtitle else self.TITLE_Y_POSITION
        draw.text((x, y), title, fill=color, font=font)

        if not subtitle:
            return

        sub_font = ImageFont.truetype(font_file, size=70)

        sub_base_width, _ = base.size
        sub_w_title, _ = draw.textsize(subtitle, font=sub_font)

        sub_x = int(sub_base_width / 2 - sub_w_title / 2)
        sub_y = self.TITLE_Y_POSITION + h_title
        draw.text((sub_x, sub_y), subtitle, fill=subtitle_color, font=sub_font)

    def __add_player(self, base, player_name, color_name, position: Tuple):
        position_x, position_y = position

        player_image = Image.open(f'{self.base_directory}/img/{color_name.capitalize()}.png').resize(self.CREWMATE_SIZE)

        x = int(self.__crewmate_space()[0] * position_x + self.SIDE_MARGIN + self.__center_padding() + self.__offset / 2)
        y = self.__background_height + (self.__crewmate_space()[1] + self.__center_padding()) * (position_y - self.__total_rows) + self.__center_padding()

        base.paste(player_image, (x, y), player_image.convert('RGBA'))

        font = ImageFont.truetype(f'{self.base_directory}/font/In your face, joffrey!/In your face, joffrey!.ttf', size=self.NAME_SIZE)

        draw = ImageDraw.Draw(base)

        w_name, h_name = draw.textsize(player_name, font=font)

        if w_name > self.__crewmate_space()[0]:
            ellipsis = '...'
            while True:
                player_name = player_name[:len(player_name) - 1]
                w_name, h_name = draw.textsize(player_name + ellipsis, font=font)
                if w_name <= self.__crewmate_space()[0]:
                    break
            player_name += ellipsis

        x_name = int(x + self.CREWMATE_SIZE[0] / 2 - w_name/2)
        y_name = y - h_name - 10
        color_fill = self.color_palette.get(color_name.lower(), (0, 0, 0))
        draw.text((x_name, y_name), player_name, fill=color_fill, font=font)

        return base

    def __create_victory_filename(self, is_impostor_win, winners):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        winning_team = 'impostors' if is_impostor_win else 'crewmates'
        return f'{timestamp}_{winning_team}_{"_".join(winners)}'[:250]

    def __crewmate_space(self):
        return self.CREWMATE_SIZE[0] + self.PADDING, self.CREWMATE_SIZE[1] + self.PADDING

    def __center_padding(self):
        return int(self.PADDING / 2)

    def __best_split(self, split_options, total):
        best_split = 0
        least_empty = split_options[0]
        for split in split_options:
            value = total % split
            if not value:
                return split
            empty = split - value
            if empty < least_empty:
                least_empty = empty
                best_split = split
        return best_split

def main():
    crewmates_colors_map = [
        ('GabeAvacado', 'Brown'),
        ('hnstokes', 'Purple'),
        ('Guo', 'White'),
        ('Quesotilla', 'Green'),
        ('Beccles', 'Blue'),
        ('okdawg', 'Tan'),
        ('poopboost', 'Gray'),
        ('Pinkytoe101', 'Pink'),
        ('Mark', 'Maroon'),
        ('jrod9739', 'Orange'),
    ]

    impostors_colors_map = [
        ('Jenna', 'Red'),
        ('Dink', 'Cyan'),
        ('Can', 'Black'),
    ]

    service = ImageService('D:/Documents/SusProject', {
        'red': (215, 30, 34),
        'blue': (29, 60, 233),
        'green': (27, 145, 62),
        'pink': (255, 99, 212),
        'orange': (255, 141, 28),
        'yellow': (255, 255, 103),
        'black': (74, 86, 94),
        'white': (233, 247, 255),
        'purple': (120, 61, 210),
        'brown': (128, 88, 45),
        'cyan': (68, 255, 247),
        'lime': (91, 254, 75),
        'maroon': (108, 43, 61),
        'rose': (255, 214, 236),
        'banana': (255, 255, 190),
        'gray': (131, 151, 167),
        'tan': (159, 153, 137),
        'coral': (236, 117, 120),
    })
    service.create_team_screens(crewmates_colors_map, impostors_colors_map, True)

if __name__ == '__main__': # used for testing
    main()