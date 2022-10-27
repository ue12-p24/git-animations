from manimlib.imports import *

from coloredfile import ColoredFile

# NOTE on updaters and staticmethods
# we NEED to refer to the updater functions as Class._method
# and NOT self._method, because in the latter case the bound method
# receives 2 arguments (the bound instance + itself again)
# (one could have used staticmethods as well)

def _load_icon(filename, built_in_scale, scale, height=None):
    loaded = SVGMobject(filename)
    if height is not None:
        return loaded.set_height(height)
    else:
        return loaded.scale(built_in_scale*scale)

def file_system_icon(scale=1, height=None):
    return (_load_icon("folder-svgrepo-com.svg", 0.7, scale, height)
            .to_corner(UL))

def index_icon(scale=1, height=None):
    return (_load_icon("stage-svgrepo-com.svg", 0.7, scale, height)
            .to_edge(UP))

def git_repo_icon(scale=1, height=None):
    return (_load_icon("database-svgrepo-com.svg", 0.7, scale, height)
            .to_corner(UR))

def github_icon(scale=1, height=None):
    return (_load_icon("github-cat2.svg", 0.4, scale, height)
            .to_corner(UR))

def internet_icon(scale=1, height=None):
    return (_load_icon("internet-svgrepo-com.svg", 0.4, scale, height))


def manim_pprint(obj, *, indent='  ', depth=0):
    print(depth*indent, end='')
    print(obj.__class__.__name__)
    if isinstance(obj, Container):
        for sub in obj.submobjects:
            manim_pprint(sub, indent=indent, depth=depth+1)


def vertical_separator(obj1, obj2):
    """
    returns a vertical line that splits the space between both objects
    """
    # obj1 is on the left of obj2
    sep_x, *_ = (obj1.get_left()+obj2.get_right())/2
    sep_bot = sep_x * RIGHT + 4*DOWN
    sep_top = sep_x * RIGHT + 4*UP
    return Line(sep_bot, sep_top)


class Legend:
    font = "helveltica"
    """
    a message that explains what we're doing
    """
    def __init__(self, scene, legend: str, **config):
        self.scene = scene
        self.legend = VGroup(*(TextMobject(line, font=self.font, **config)
                               for line in legend.split("\n"))).arrange(DOWN)

    def show(self, position_lambda):
        if position_lambda:
            position_lambda(self.legend)
        self.scene.play(Write(self.legend), run_time=0.5)
        self.scene.wait(0.5)
        return self

    def hide(self):
        self.scene.play(self.hide_animation(), run_time=0.5)
        self.scene.wait(0.5)
        return self

    def hide_animation(self):
        return FadeOut(self.legend)

class Console(Legend):
    font = "courier"
    alignment = "left"

    def __init__(self, scene, legend:str):
        self.scene = scene
        self.legend = Paragraph(*(f"$ {x}" for x in legend.split("\n")),
                                alignment=self.alignment,
                                font=self.font)


class Display:

    # the default position is in the bottom left corner
    # upped by one so the video player UI has space
    def default_position(self, obj):
        obj.to_corner(DL).shift(UP)

    def __init__(self, scene, position_lambda=None):
        self.scene = scene
        self.legend = None
        self.position_lambda = position_lambda or self.default_position

    def hide(self):
        if self.legend is not None:
            self.legend.hide()
        self.legend = None

    def display(self, text, console=False, position_lambda=None):
        self.hide()
        if isinstance(text, Legend):
            self.legend = text
        else:
            cls = Console if console else Legend
            self.legend = cls(self.scene, text)
        self.legend.show(position_lambda or self.position_lambda)


class Editable(ColoredFile):
    """
    the materialization of a file on the disk
    """
    CONFIG = dict(
        filesystem_width=4,
        color=BLUE,
        opacity=0.25,
    )
    def __init__(self, text, *args, **kwds):
        super().__init__(text, *args, **kwds)
        self.frame = SurroundingRectangle(
            self, color=self.color, fill_color=self.color, fill_opacity=self.opacity)
    def nail(self, other):
        if self.filesystem_width:
            other.scale(self.filesystem_width / other.get_width())
        return self
    def create_animations(self, scene):
        if self.filesystem_width:
            self.set_width(self.filesystem_width)
        self.nail(self)
        def update_decorations(x):
            r = SurroundingRectangle(self)
            self.frame.set_width(r.get_width(), stretch=True)
            self.frame.set_height(r.get_height(), stretch=True)
            self.frame.move_to(r.get_center())
        self.add_updater(update_decorations)
        return [FadeIn(self),
                ShowCreation(self.frame)]



class Index(ColoredFile):
    CONFIG = dict(
        index_width=4,
        color=GREEN,
        opacity=0.25,
    )
    def __init__(self, text, *args, **kwds):
        super().__init__(text, *args, **kwds)
        #
        self.frame = SurroundingRectangle(
            self, color=self.color, fill_color=self.color, fill_opacity=self.opacity)

    def nail(self, other):
        if self.index_width:
            other.scale(self.index_width / other.get_width())
        return self

    def create_animations(self, scene):
        if self.index_width:
            self.set_width(self.index_width)
        self.nail(self)
        def update_decorations(x):
            r = SurroundingRectangle(self)
            self.frame.set_width(r.get_width(), stretch=True)
            self.frame.set_height(r.get_height(), stretch=True)
            self.frame.move_to(r.get_center())
        self.add_updater(update_decorations)
        return [FadeIn(self),
                ShowCreation(self.frame)]


