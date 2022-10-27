#
# VOLATILE and TEMPORARY
#
# just a collection of microscopic scripts used to try out small ideas
#


from manimlib.imports import *

import sys; sys.path.append('.')
from grids import ScreenGrid

BODY1 = """# empty for now
class Foo:
    pass"""

BODY2 = """# a little better
class Foo:
    def __init__(self, text):
        self.text = text"""

GLOBAL_CONFIG = {
    'body1': BODY1,
    'body2': BODY2,
    'font': 'courier',
}

class ArcCreation(Scene):
    def construct(self):

        self.add(ScreenGrid())

        def game(a1, a2, sign):
            for angle in 0, .4*PI, PI/3, PI/4, PI/5:
                self.play(
                    ShowCreation(
                        CurvedArrow(
                            a1, a2, angle=angle*sign
                        )
                    ),
                    run_time=0.1
                )
                self.wait(0.2)

        a1 = 2*UP + 4 * LEFT
        a2 = 2*UP + 4 * RIGHT
        game(a1, a2, 1)

        b1 = 2*DOWN + 4 * LEFT
        b2 = 2*DOWN + 4 * RIGHT
        game(b1, b2, -1)

        self.wait()

class FramedText(Scene):
    def construct(self):

        text = Paragraph("one", "two", "three",
                         font="courier", alignment="left")

        r = SurroundingRectangle(text, color=RED)
        self.add(text, r)
        self.wait()


        def update_frame(x):
            print("updating frame")
            # NOT WORKING if we use x here, but text is fine
            r2 = SurroundingRectangle(text)
            r.set_width(r2.get_width(), stretch=True)
            r.set_height(r2.get_height(), stretch=True)
            r.move_to(r2.get_center())
        text.add_updater(update_frame)

        self.play(text.shift, 4*RIGHT,
                  text.scale, 2,
                  runtime=5)
        self.wait()

        transformed_text = (Paragraph("one", "three",
                                      font="courier", alignment="left")
                            .to_corner(DR))
        self.play(Transform(text, transformed_text))


        self.wait()

class TextTransform(Scene):
    CONFIG = GLOBAL_CONFIG

    def construct(self):
        r = Rectangle(width=10, height=3)
        v1 = Text(self.body1, font=self.font)
        v2 = Text(self.body2, font=self.font)
        self.add(r, v1)
        self.wait()
        self.play(ReplacementTransform(v1, v2))
        self.wait()
        v2.generate_target()
        v2.target.shift(2*RIGHT+2*DOWN)
        r.generate_target()
        r.target.shift(2*RIGHT+2*DOWN)
        self.play(MoveToTarget(v2), MoveToTarget(r))
        self.wait()

class SetTextSize(Scene):
    CONFIG = GLOBAL_CONFIG
    def construct(self):
        v1 = Text(self.body1, font=self.font)
        v1.set_width(5)
        def updater(text, dt):
            print(f"{text.width=}, {dt=}")
        self.add(v1)
        self.play( v1.set_width, 2, )
        v1.add_updater(updater)
        self.wait()
        v1.clear_updaters()
        self.wait()


WIDTH = 1
class IndexManual(Scene):

    def construct(self):

        c1 = Circle().to_edge(UP)

        r1 = Rectangle(width=WIDTH, height=2).next_to(c1, DOWN)
        p1 = Paragraph("one line", "two lines").to_edge(LEFT)
        self.add(c1, r1, p1)
        self.wait()

        p1.generate_target()
        p1.target.move_to(r1.get_center())
        p1.target.set_width(WIDTH)
        next_height = SurroundingRectangle(p1.target).get_height()
        r1.generate_target()
        r1.target.set_height(next_height, stretch=True)
        r1.target.next_to(c1, DOWN)
        p1.target.move_to(r1.target.get_center())
        self.play(MoveToTarget(p1), MoveToTarget(r1))

        self.wait()

class InsertInParagraph(Scene):
    def construct(self):
        p = Paragraph("line1", "line2", font='courier', alignment='left')
        self.add(p)
        self.wait()
        p2 = Paragraph("line1", "line1bis", "line1ter", "line2",
                       font='courier', alignment='left')
        r = SurroundingRectangle(p2[1:3])
        p2[1:3].set_color(YELLOW)
        self.play(Transform(p, p2), FadeIn(r))
        self.wait()
        p2[1:3].set_color(WHITE)
        self.play(Transform(p, p2), FadeOut(r))
        self.wait()


from coloredfile import ColoredFile
from bricks import Index, Editable
from repo import Commit, ObsoleteRepo, Repo

class BricksIndexCreation(Scene):
    def construct(self):

        p1 = ColoredFile(["line1", "line2"],
                         alignment="left", font='courier')
        p1.to_edge(LEFT)
        self.add(p1)

        anchor = Dot().to_edge(UP)
        self.add(anchor)
        class MyIndex(Index):
            def nail(self, other):
                super().nail(other)
                other.next_to(anchor, DOWN, buff=0.5)
                return self

        index = MyIndex("---", color=RED)
        self.play(*index.create_animations(self))
        self.wait(.5)

        p2 = ColoredFile(["line1", "line1bis", "line2"],
                         alignment="left", font='courier')
        p2.to_edge(LEFT)
        r = SurroundingRectangle(p2[0:2])
        self.play(Transform(p1, p2),
                  FadeIn(r))
        self.wait()

        self.play(*index.morph_animations(self, p1),
                  FadeOut(r))
        index.clean_morph(self)

        self.wait()


class CommitCreation(Scene):
    def construct(self):
        self.add(ScreenGrid())
        p = Paragraph("one line", "two", "three",
                      font="courier", alignment="left")
        p.to_corner(UL)
        self.add(p)

        d = Dot().to_corner(UR).shift(2*LEFT)
        class MyRepo(ObsoleteRepo):
            def nail(self, other):
                other.next_to(d, DOWN, buff=1)
                return self

        repo = MyRepo(DOWN_SCALING=0.8)
        self.add(d, repo)


        # commit h1
        repo.adopt_initial(c1 := Commit("h1"))
        self.play(*c1.create_morph_animations(self, p))
        c1.clean_morph(self)
        self.wait()

        # return

        # replace file
        self.remove(p)
        p = Paragraph("one line", "two", "three", "four",
                      font="courier", alignment="left")
        p.to_corner(UL)
        self.add(p)
        self.wait()


        # commit h2
        repo.adopt_further(c := Commit("h2", hash_location=RIGHT))
        self.play(*c.create_morph_animations(self, p))
        c.clean_morph(self)
        self.wait()


        # replace file
        self.remove(p)
        p = Paragraph("something longer\n    class Foo:\n"
                      "    def __init__(self):\n        pass",
                      font="courier", alignment="left")
        p.to_corner(UL)
        self.add(p)
        self.wait()


        # commit h3
        repo.adopt_further(c := Commit("h3"))
        self.play(*c.create_morph_animations(self, p))
        c.clean_morph(self)
        self.wait()

        # commit h4
        repo.adopt_further(c := Commit("h4"))
        self.play(*c.create_morph_animations(self, p))
        c.clean_morph(self)
        self.wait()

class IndexFromCommit(Scene):
    def construct(self):

        class MyCommit(Commit):
            def nail(self, other):
                c1.to_edge(RIGHT)
        c1 = MyCommit(hash="a21", text=["a much longer", "contents"])
        c1.make_it_fit()
        c1.add_updater(Commit.update_decorations)
        c1.nail(c1)
        self.add(c1, c1.hash, c1.circle)
        self.wait()

        anchor = Dot().to_edge(UP)
        self.add(anchor)
        class MyIndex(Index):
            def nail(self, other):
                super().nail(other)
                other.next_to(anchor, DOWN, buff=0.5)
                return self

        index = MyIndex("---", color=RED)
        self.play(*index.create_animations(self))
        self.wait()

        self.play(*index.morph_animations(self, c1))
        index.clean_morph(self)

        self.wait()

class IndexPartialManual(Scene):
    def construct(self):
        plain = ColoredFile("one\ntwo\nthree\nfour")
        plain.to_edge(LEFT)
        self.add(plain)
        block_spec = ((1, 3), BLUE)
        r = plain.get_block(block_spec)
        self.add(r)

        index_file = ColoredFile("one\nmiddle\nfour")

        class MyIndex(Index):
            def nail(self, other):
                super().nail(other)
                other.to_edge(UP)
                return self

        index = MyIndex(index_file)
        self.play(*index.create_animations(self))

        new_text = index.lines_list.copy()
        new_text[1:2] = plain.lines_list[1:3]
        new_index = Index(text="\n".join(new_text))
        new_index.nail(new_index)

        floating = plain[1:3].copy()
        floating.generate_target()
        floating.target.move_to(
            new_index[1:3].get_center()
        )

        self.play(MoveToTarget(floating), Transform(index, new_index))
        self.wait()

class MyEditable(Editable):
    def nail(self, other):
        super().nail(other)
        other.to_edge(LEFT)
        return self

class MyIndex(Index):
    def nail(self, other):
        super().nail(other)
        other.to_edge(UP)
        return self

class IndexPartial(Scene):
    def construct(self):

        self.add(Text("just one partial morph",
                      font="times").to_corner(DL))

        editable = MyEditable(
            "one\ntwo\nthree\nfour\nfive\n"
            "six\nseven\neight\nnine\nten\n"
            ).to_edge(LEFT)
        self.add(editable)

        index = MyIndex(
            "one index\nto-replace 11\nto-replace 12\nfive index\n"
            "six index\nto-replace 21\nto-replace 22\nten index",
            color=YELLOW)
        self.play(*index.create_animations(self))

        changes = []
        changes.append((1, 4, 1, 3))
        changes.append((6, 9, 5, 7))

        self.play(*index.morph_partial_animations(self, editable, changes))
        index.clean_morph(self)
        self.wait()


class IndexPartial2(Scene):
    def construct(self):

        self.add(Text("morph + partial morphs",
                      font="times").to_corner(DR))

        editable = MyEditable(
            "one\ntwo\nthree\nfour\nfive\n"
            "six\nseven\neight\nnine\nten",
            filesystem_width=1.5).to_edge(LEFT)
        self.add(editable)

        # this one won't show up
        initial = ColoredFile(
            "one index\nto-replace 11\nto-replace 12\nfive index\n"
            "six index\nto-replace 21\nto-replace 22\nten index",
        )

        index = MyIndex("start", color=GREEN)
        index.nail(index)
        self.play(*index.create_animations(self))
        self.wait()

        self.play(*index.morph_animations(self, initial))
        index.clean_morph(self)
        self.wait()

        changes = []
        changes.append((1, 4, 1, 3))
        changes.append((6, 9, 5, 7))

        self.play(*index.morph_partial_animations(self, editable, changes))
        index.clean_morph(self)
        self.wait()

        changes = []
        changes.append((0, 0, 5, 10))
        self.play(*index.morph_partial_animations(self, editable, changes))
        index.clean_morph(self)
        self.wait()

        self.play(index.to_edge, RIGHT)
        self.wait()

class TextGallery(Scene):
    def construct(self):

        self.add(x := Dot().to_edge(UP))
        self.add(x := Text("Text plain $a^2$ \textbf{bold}").next_to(x, DOWN))
        self.add(x := TextMobject("TextMobject plain $a^2$ \textbf{bold}").next_to(x, DOWN))
        self.add(x := TexMobject("TexMobject plain a^2\textbf{bold}").next_to(x, DOWN))
        self.add(x := Text("Text plain $a^2$ but some bold",
                           t2w={'some bold': BOLD},
                           font="helvetica").next_to(x, DOWN))
        self.add(x := Paragraph("a paragraph spans",
                                "several lines and bold",
                                t2w={'some bold': BOLD},
                                font="helvetica").next_to(x, DOWN))
        self.add()
        self.wait()

class Fills(Scene):
    def construct(self):

        script = '''Hello
World'''

        t = Text(script, font="helvetica") #, t2w={'World': BOLD})
        t.to_edge(RIGHT)
        r = SurroundingRectangle(t, fill_opacity=0.25, fill_color=GREEN, color=GREEN)
        r.move_to(t.get_center())
        g = VGroup(t, r)
        self.play(Write(g))

        #t2.generate_target()

        self.play(Rotate(g, about_point=4*DOWN, angle=2*PI/3), run_time=4)
        self.wait(0.2)

        self.wait()


script = '''Hello
l'été
ça va coûter des €'''

class FilledVGroup(Scene):
    def construct(self):
        g = VGroup()
        r = SurroundingRectangle(g, fill_color=GREY, fill_opacity=0.25, color=GREY)
        for i in range(4):
            g.add(Dot().shift(i*RIGHT))
        self.play(ShowIncreasingSubsets(g), FadeIn(r))
        self.wait()

class CircleLabels(Scene):
    def construct(self):

        g = VGroup()

        def one(label, point):
            c = Circle(radius=0.4).move_to(point)
            l = Text("h1")
            c.add_updater(lambda c: l.move_to(c.get_center()))
            # c.update()
            g.add(c, l)

        one("h1", 0*DOWN)
        one("h2", UP)

        self.add(g)
        self.wait()


class RelativeMove(Scene):
    def construct(self):
        self.add(ScreenGrid())
        g = VGroup()
        c = Dot().move_to(UR)
        d = Dot().move_to(3*(UR))
        g.add(c, d)
        g.to_corner(DL)
        self.add(g)
        # how do I move c to  e.g. (2*UP+2*RIGHT)
        # but inside the group coordinates ?
        # so it ends up between its original position and d ?
        self.wait()

        g2 = VGroup()
        c.move_to(2*UR)
        d.move_to(3*UR)
        g2.add(c, d)
        g2.to_corner(DL)
        self.play(Transform(g, g2))
        self.wait()


class AAA(Scene):
    def construct(self):
        pass


from repo import Repo

class RepoTest(Scene):

    def construct(self):

        class RightRepo(Repo):
            CONFIG = dict(
                x_stretch=0.8, y_stretch=1.5,
            )
            def nail(self, other):
                other.to_corner(UR)

        repo = RightRepo()

        class MyCommit(Commit):
            CONFIG = dict(
                commit_width=0.5,
            )
            pass

        c1 = MyCommit("h1", text=' ')
        c21 = MyCommit("h21", text=' ')
        c22 = MyCommit("h22", text=' ', hash_location=RIGHT, refs_location=UP)
        c3 = MyCommit("h3", text=' ')
        c4 = MyCommit("h4", text=' ')

        repo.add_commit(c1)
        c1.set_refs("foo", "bar")
        c1.outline_ref("foo", color=RED, scale=3)
        repo.add_commit(c21, "h1")
        repo.add_commit(c22, c1)
        c22.set_refs("origin/devel")
        repo.add_commit(c3, c21, c22)
        c3.set_refs("HEAD")

        self.add(repo.add_target())
        self.wait()

        repo.add_commit(c4, c3)
        c3.set_refs()
        c4.set_refs("HEAD")
        target = repo.update_target()
        self.play(Transform(repo, target), run_time=0)
        self.wait()

        # xx about to make an animation instead of
        # this out of the blue business
        # repo_floating = repo.copy()

        repo2 = repo.copy()
        repo2.find_commit("h1").refs_buff = 1
        x_stretch = 1
        y_stretch = 2
        for commit in repo2.commits:
            commit.commit_width = 1
        def middle_repo_nail(other):
            other.to_corner(DL)
        repo2.nail = middle_repo_nail
        self.play(FadeIn(repo2.add_target()))
        self.wait()

from scenespull import C1_BODY, C2_BODY, C3_BODY
from bricks import *

class SampleRepos(Scene):
    CONFIG = dict(
        icon_height=0.5,
    )
    def construct(self):
        self.add(ScreenGrid())
        def one_repo(X, stretch, arrow_width,
                     commit_width, hash_size, hash_buff):
            github_anchor = (github_icon(height=self.icon_height)
                             .move_to(X*RIGHT).to_edge(UP))
            class GithubRepo(Repo):
                CONFIG = dict( y_stretch=stretch, arrow_width=arrow_width, arrow_color=GREEN, )
                def nail(self, other):
                    #other.set_width(self.repo_width)
                    other.next_to(github_anchor, DOWN, buff=0.5)
            class MyCommit(Commit):
                CONFIG = dict( commit_width=commit_width, hash_size=hash_size, hash_buff=hash_buff, )

            repo1 = GithubRepo()
            c1 = MyCommit("h1", text=C1_BODY)
            c2 = MyCommit("h2", text=C2_BODY)
            #c22 = MyCommit("h22", text=' ', hash_location=RIGHT)
            c3 = MyCommit("h3", text=C3_BODY)

            repo1.add_commit(c1)
            repo1.add_commit(c2, c1)
            #repo1.add_commit(c22, c1)
            repo1.add_commit(c3, c2)

            self.add(github_anchor)
            self.add(repo1.add_target())
            self.wait()
        #X, stretch, arrow_width, commit_width, hash_size, hash_buff
        one_repo(5, 1.5, None, 1, 0.2, 0.2)
        one_repo(2, 2, None, 1, 0.3, 0.3)
        one_repo(-1, 3, None, 1, 0.4, 0.4)
        one_repo(-4, 2, None, 1.2, 0.5, 0.5)

class Arrows(Scene):
    def construct(self):
        self.add(ScreenGrid())

        self.play(ShowCreation(Arrow(UP, .5*UP, buff=0)))
        self.wait()
        self.play(ShowCreation(Arrow(0*UP, 2*DOWN)))
        self.wait()

        self.play(ShowCreation(Arrow(RIGHT, 3*RIGHT+DOWN, buff=0.5)))
        self.wait()

        self.play(ShowCreation(CurvedArrow(RIGHT, 3*RIGHT+DOWN, angle=PI/3,
                                           buff=0.5)))
        self.wait()

class DirectMove(Scene):
    def construct(self):
        self.add(d1 := Dot())
        self.add(d2 := Dot().shift(RIGHT))
        self.play(d1.shift, UP, d2.shift, DOWN)
        self.wait()
        g = Group(d1, d2)
        self.play(g.shift, 3*(UP+RIGHT))
        self.wait()
        pprint(g)

class Buffs(Scene):
    def construct(self):
        buff = 1
        direction = DOWN
        d = Dot().to_edge(UP)
        g = VGroup()
        g.add(Text("foo", font="courrier"))
        g.add(Text("bar", font="courrier"))
        g.arrange(direction, buff=buff)
        g.next_to(d, direction=direction, buff=buff)
        self.add(d, g)
        self.add(SurroundingRectangle(g))
        self.wait()


class Ordering(Scene):
    def construct(self):

        class MyRepo(Repo):
            def nail(self, other):
                other.to_edge(DOWN).shift(UP)
        class MyCommit(Commit):
            CONFIG = dict(
                commit_width=0.5,
                hash_size=0.2,
            )

        repo = MyRepo(x_stretch=0.5, y_stretch=1)
        repo.add_commit(MyCommit("h1"))
        #repo.add_commit(MyCommit("h2"), "h1")
        #repo.add_commit(MyCommit("h3"), "h2")
        #repo.add_commit(MyCommit("h4"), "h3")
        fork = "h1"
        repo.add_commit(MyCommit("yours"), fork)
        #print("------up to yours")
        self.add(repo.add_target())
        self.wait()

        repo.debug_graph = True
        repo.add_commit(MyCommit("theirs"), fork).hash_location = RIGHT
        print("------added theirs")
        repo.flush(self)
        self.wait()

        print("------swapped")
        repo.swap_commits("yours", "theirs")
        repo.find_commit("yours").hash_location = RIGHT
        repo.find_commit("theirs").hash_location = LEFT
        repo.clear_layout()
        repo.flush(self)
        self.wait()

        repo.add_commit(MyCommit("merged"), "yours", "theirs")
        print("------merged")
        repo.flush(self)
        self.wait()

        print("------swapped again")
        repo.swap_commits("yours", "theirs")
        repo.find_commit("yours").hash_location = LEFT
        repo.find_commit("theirs").hash_location = RIGHT
        repo.clear_layout()
        repo.flush(self)

        repo.add_commit(MyCommit("b1"), "merged")
        repo.add_commit(MyCommit("b2"), "merged")
        repo.add_commit(MyCommit("b3"), "merged")
        repo.add_commit(MyCommit("c1"), "b1")
        repo.add_commit(MyCommit("c2"), "b2", "b3")
        repo.add_commit(MyCommit("d"), "c1", "c2")
        repo.flush(self)

        self.wait()

class Footnote(Scene):
    def construct(self):

        footnote = Paragraph(r"if you try, git push will complain",
                             r"about the remote merge being not a fast-foward",
                             color=RED)
        footnote.to_edge(UP).shift(DOWN)
        self.add(footnote)
        self.wait()

class Displays(Scene):
    def construct(self):

        display = Display(self)
        display.display("default is DOWN LEFT + 1")
        display.display("down left + 1", console=True)
        display.hide()

        def mydisplay(x):
            x.to_corner(UR)
        def overridedisplay(x):
            x.move_to(0*UP).shift(LEFT)
        display = Display(self, mydisplay)
        display.display("UP RIGHT")
        display.display("up right", console=True)
        display.display("MIDDLE-1", position_lambda=overridedisplay)
        display.display("back up right", console=True)


        note = Legend(self, "with this model, one can only put\n"
                            "all the changes in the new commit\n"
                            "at the same time ... not good enough !!!",
                            t2w={'all the changes': BOLD})
        display.display(note)
        self.wait()
        display.hide()
        self.wait()

