import ptext


class Text:
    def __init__(self, state, text, style, **kwargs):
        self.state = state
        self.text = text
        self.style = style
        self.kwargs = kwargs

        self.font = "assets/fonts/recharge/recharge.ttf"
        self.font_mono = "assets/fonts/unispace/unispace bd.ttf"

        self.styles = {
            "regular": {
                "color": self.state.colors['text'],
                "fontname": self.font,
                "fontsize": 14
            },
            "regular_mono": {
                "color": self.state.colors['text'],
                "fontname": self.font_mono,
                "fontsize": 14
            },
            "button": {
                "color": self.state.colors['button_text_top'],
                "gcolor": self.state.colors['button_text_bottom'],
                "fontname": self.font,
                "fontsize": 26
            },
            "heading": {
                "color": "white",
                "gcolor": "purple",
                # "color": "red",
                # "gcolor": "purple",
                "shadow": (1, 1),
                "scolor": "#666666",
                "fontname": self.font,
                "fontsize": 40
            },
            "label": {
                "color": self.state.colors['label_text_top'],
                "gcolor": self.state.colors['label_text_bottom'],
                "shadow": (1, 1),
                "scolor": "#666666",
                "fontname": self.font,
                "fontsize": 26
            },
            "progress_label": {
                "color": self.state.colors['label_text_top'],
                "gcolor": self.state.colors['label_text_bottom'],
                "shadow": (1, 1),
                "scolor": "#666666",
                "fontname": self.font_mono,
                "fontsize": 22
            }
        }
        pass

    def process_event(self, event):
        pass

    def update(self):
        pass

    def render(self, surface):
        draw_options = self.styles[self.style]
        draw_options['surf'] = surface
        draw_options.update(self.kwargs)

        ptext.draw(self.text, **draw_options)
