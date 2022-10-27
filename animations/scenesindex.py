# import from . won't work out of the box
from manimlib.imports import *

import sys
sys.path.append('.')

from bricks import (
    file_system_icon, index_icon, git_repo_icon,
    github_icon, internet_icon, vertical_separator, manim_pprint,
    Display, Legend, Editable, Index,
)

from repo import (
    Commit, ObsoleteRepo, Repo,
)

from grids import ScreenGrid



BODY1 = """class Foo:
    \"\"\"
    empty for now
    \"\"\"
    pass"""

BODY2_HALF = """class Foo:
    \"\"\"
    empty for now
    \"\"\"
    def __init__(self, text):
        self.text = text"""

BODY2 = """class Foo:
    \"\"\"
    a little better
    \"\"\"
    def __init__(self, text):
        self.text = text"""

BODY2_TEXTCOLORS = [([2, 4, 5], RED)]

BODY3 = """# one cosmetic change
class Foo:
    \"\"\"
    a little better
    \"\"\"
    def __init__(self, text, id):
        self.text = text
        self.id = id"""

BODY4 = """# one cosmetic change
class Foo:
    \"\"\"
    another change
    \"\"\"
    def __init__(self, text, id):
        self.text = text
        self.id = id
    """

# like python slices (beg included and end excluded)
BODY3_TEXTCOLORS = [(0, YELLOW), ([5, 7], RED)]
BODY3_BLOCKS = [(0, YELLOW), ((5, 8), RED)]


FAST = False
#FAST = True

class NoIndex(Scene):
    CONFIG = {
            'wait_duration': 0.2 if FAST else 1,
            'transition_duration': 0.5 if FAST else 2,
            'remove_duration': 0.5,
        }

    def wait(self, duration=None):
        duration = duration or self.wait_duration
        super().wait(duration)

    def construct(self):

        display = Display(self)

        display.display("let's imagine a model\nwithout an index")
        self.wait()

        # display filesystem icon
        top_left_anchor = file_system_icon()
        self.add(top_left_anchor)

        class MyEditable(Editable):
            def nail(self, other):
                super().nail(other)
                other.next_to(top_left_anchor, DOWN, buff=1)
                other.to_edge(LEFT)
                return self


        display.display("you create a file")
        # display initial file contents
        editable = MyEditable(BODY1)
        editable.nail(editable)
        self.play(*editable.create_animations(self),
                  run_time=self.transition_duration)
        self.wait()


        # git init
        display.display("git init", console=True)

        top_right_anchor = git_repo_icon()
        self.play(ShowCreation(top_right_anchor))

        class MyRepo(ObsoleteRepo):
            def nail(self, other):
                super().nail(other)
                other.next_to(top_right_anchor, DOWN, buff=0.5)
                return self

        repo = MyRepo(down_scaling=0.9)
        repo.nail(repo)
        self.add(repo)
        self.wait()


        # commit h1
        display.display("git commit", console=True)

        repo.adopt_initial(c1 := Commit("h1"))
        self.play(*c1.create_morph_animations(self, editable))
        c1.clean_morph(self)
        self.wait()


        # edit h2
        display.display("using your editor")

        self.play(*editable.replace_animations(self,BODY2))
        editable.apply_textcolors(BODY2_TEXTCOLORS)
        self.wait()


        # commit h2
        display.display("git commit", console=True)

        repo.adopt_further(c := Commit("h2"))
        self.play(*c.create_morph_animations(self, editable))
        c.clean_morph(self)
        self.wait()

        c.reset_textcolors()
        self.wait()


        # edit h3
        display.display("etc...")

        self.play(*editable.replace_animations(self, BODY3))
        editable.apply_textcolors(BODY3_TEXTCOLORS)
        self.wait()

        # commit h3
        display.display("git commit", console=True)

        repo.adopt_further(c := Commit("h3"))
        self.play(*c.create_morph_animations(self, editable))
        c.clean_morph(self)
        c.reset_textcolors()
        self.wait()

        display.display("now imagine you have\n"
                        "SEVERAL distinct CHANGES")

        rects = editable.get_blocks(BODY3_BLOCKS)
        self.play(*(FadeIn(rect) for rect in rects))
        self.wait()


        display.display("with this model, one MUST put ALL\n"
                        "the pending changes in the new commit")
        self.wait()

        display.display("not good enough !!!")

        h2, w2 = 3, 5
        dl = h2*DOWN + w2*LEFT
        dr = h2*DOWN + w2*RIGHT
        ul = h2*UP + w2*LEFT
        ur = h2*UP + w2*RIGHT

        cross1 = Line(dl, ur).set_width(12).set_color(RED)
        cross2 = Line(dr, ul).set_width(12).set_color(RED)
        self.play(ShowCreation(cross1), ShowCreation(cross2))
        self.wait()

        self.wait()


class WithIndex(Scene):
    CONFIG = {
            'wait_duration': 0.2 if FAST else 1,
            'transition_duration': 0.5 if FAST else 2,
            'remove_duration': 0.5,
        }

    def construct(self):

        display = Display(self)

        display.display("same warm up,\nbut with an index")
        self.wait()
        # display filesystem icon
        top_left_anchor = file_system_icon()
        self.add(top_left_anchor)

        class MyEditable(Editable):
            def nail(self, other):
                super().nail(other)
                other.next_to(top_left_anchor, DOWN, buff=1)
                other.to_edge(LEFT)
                return self

        # display initial file contents
        editable = MyEditable(BODY1)
        editable.nail(editable)
        self.play(*editable.create_animations(self),
                  run_time=self.transition_duration)
        self.wait()


        # git init
        display.display("git init", console=True)
        middle_anchor = index_icon().shift(.5*RIGHT)
        class MyIndex(Index):
            def nail(self, other):
                super().nail(other)
                other.next_to(middle_anchor, DOWN, buff=1)
                return self
        index = MyIndex("     ")
        index.nail(index)

        top_right_anchor = git_repo_icon()
        class MyRepo(ObsoleteRepo):
            def nail(self, other):
                super().nail(other)
                other.next_to(top_right_anchor, DOWN, buff=0.5)
                return self

        repo = MyRepo(down_scaling=0.9)
        repo.nail(repo)
        self.add(repo)

        self.play(ShowCreation(top_right_anchor),
                  ShowCreation(middle_anchor),
                  *index.create_animations(self))
        self.wait()


        # show the 2 arrows that outline add and commit
        display.display("we need 2 commands")
        X1r = top_left_anchor.get_center()+RIGHT
        X2l = middle_anchor.get_center()+LEFT
        X2r = middle_anchor.get_center()+RIGHT
        X3l = top_right_anchor.get_center()+LEFT

        a1 = CurvedArrow(X1r, X2l, angle=-PI/4, color=MAROON)
        a2 = CurvedArrow(X2r, X3l, angle=-PI/4, color=MAROON)
        l1 = Text("add", font=Legend.font, color=MAROON).next_to(a1, DOWN)
        l2 = Text("commit", font=Legend.font, color=MAROON).next_to(a2, DOWN)
        self.play(*(ShowCreation(x) for x in (a1, a2, l1 ,l2)))
        #self.wait(2)
        #self.play(*(FadeOut(x) for x in (a1, a2, l1 ,l2)))
        self.wait()


        # add for h1
        display.display("git add foo.py", console=True)
        self.play(*index.morph_animations(self, editable))
        index.clean_morph(self)


        # commit h1
        display.display("git commit", console=True)
        repo.adopt_initial(c1 := Commit("h1"))
        self.play(*c1.create_morph_animations(self, index))
        c1.clean_morph(self)
        self.wait()


        # edit h2
        display.display("with your editor")
        self.play(*editable.replace_animations(self, BODY2_HALF))

        # add h2
        display.display("git add foo.py", console=True)
        self.play(*index.morph_animations(self, editable))
        index.clean_morph(self)

        # edit h2
        display.display("we can add as many times as needed")
        self.play(*editable.replace_animations(self, BODY2))

        # re add h2
        display.display("git add foo.py", console=True)
        self.play(*index.morph_animations(self, editable))
        index.clean_morph(self)


        # commit h2
        display.display("git commit", console=True)
        repo.adopt_further(c := Commit("h2"))
        self.play(*c.create_morph_animations(self, index))
        c.clean_morph(self)


        # edit h3
        display.display("keep on hacking")
        self.play(*editable.replace_animations(self, BODY3))
        left_blocks = editable.get_blocks(BODY3_BLOCKS)
        self.play(*(ShowCreation(r) for r in left_blocks))


        # add for h3
        display.display("now we can add selectively")
        changes = [(0, 1, 0, 0)]
        textcolor_spec = BODY3_TEXTCOLORS.pop(0)
        block_spec = BODY3_BLOCKS.pop(0)
        old_block = left_blocks.pop(0)

        self.play(*index.morph_partial_animations(self, editable, changes),
                  Uncreate(old_block))
        index.clean_morph(self)
        new_block = index.get_block(block_spec)
        self.play(ShowCreation(new_block))
        self.wait()


        # commit h3
        display.display("git commit", console=True)
        repo.adopt_further(c := Commit("h3"))
        self.play(*c.create_morph_animations(self, index),
                  Uncreate(new_block))
        c.clean_morph(self)
        self.wait()


        # add for h4
        display.display("and add the rest later")
        changes = [(5, 8, 5, 7)]
        textcolor_spec = BODY3_TEXTCOLORS.pop(0)
        block_spec = BODY3_BLOCKS.pop(0)
        old_block = left_blocks.pop(0)

        self.play(*index.morph_partial_animations(self, editable, changes),
                  Uncreate(old_block))
        index.clean_morph(self)
        new_block = index.get_block(block_spec)
        self.play(ShowCreation(new_block))
        self.wait()


        # commit h4
        display.display("git commit", console=True)
        repo.adopt_further(c := Commit("h4"))
        self.play(*c.create_morph_animations(self, index),
                  Uncreate(new_block))
        c.clean_morph(self)
        self.wait()

