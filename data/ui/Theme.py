WHITE = "#FFFFFF"
LIGHT_WHITE = "#F2F3F5"
DARK_WHITE = "#B9BBBE"

DARK_GRAY = "#46494D"
LIGHT_GRAY = "#757779"
BLACK = "#000000"


class Theme:
    
    def __init__(self, fontColor, mainBackgroundColor, altBackgroundColor, name):
        self.fontColor = fontColor
        self.mainBackgroundColor = mainBackgroundColor
        self.altBackgroundColor = altBackgroundColor
        self.name = name

    @staticmethod
    def get_theme(theme):
        return Theme(*{"dark": [WHITE, DARK_GRAY, LIGHT_GRAY],
                       "light": [BLACK, WHITE, LIGHT_WHITE]}[theme], theme)
