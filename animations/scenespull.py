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

C1_BODY = """# version 1
class Foo:
    pass"""

C2_BODY = """# version 2
class Foo:
    def __init__(self):
        pass"""

C3_BODY = """# version 3
class Foo:
    def __init__(self, x):
        self.x = x"""

C4_BODY = """# version 4
class Foo:
    def __init__(self, x, id):
        self.x = x
        self.id = id"""

class CloneAndPull(Scene):
    CONFIG = dict(
        icon_height=0.8,
    )
    def construct(self):
        display = Display(self)


        display.display("you notice a repo on github")
        #self.add(ScreenGrid())

        github_anchor = (github_icon(height=self.icon_height)
                         .to_corner(UR).shift(LEFT))
        class GithubRepo(Repo):
            CONFIG = dict(
                hash_size=0.25,
                y_stretch=1.8,
                arrow_color=GREEN,
                arrow_width=1.5,

            )
            def nail(self, other):
                (other
                 .next_to(github_anchor, DOWN, buff=0.5)
                 .to_edge(RIGHT, buff=0.5))


        class MyCommit(Commit):
            CONFIG = dict(
                hash_size=0.2,
                hash_buff=0.3,
                refs_size=0.15,
                refs_buff=0.15,
                regular_stroke_width=3,
                current_stroke_width=6,
            )

        repo1 = GithubRepo()
        c1 = MyCommit("h1", text=C1_BODY)
        c2 = MyCommit("h2", text=C2_BODY)
        c3 = MyCommit("h3", text=C3_BODY)
        c3.set_refs("main")

        repo1.add_commit(c1)
        repo1.add_commit(c2, c1)
        repo1.add_commit(c3, c2)

        self.add(github_anchor)
        self.add(repo1.add_target())

        self.wait()


        display.display("git clone https://github.com/...", console=True)

        git_repo_anchor = (git_repo_icon(height=self.icon_height)
                           .shift(5*LEFT))

        repo2 = repo1.deepcopy()
        repo2.generate_target()
        #repo2.target.shift(4*LEFT)
        def local_repo_nail(other):
            other.next_to(git_repo_anchor, DOWN, buff=0.5)
        repo2.nail = local_repo_nail
        repo2.nail(repo2.target)

        start = github_anchor.get_center()+LEFT*self.icon_height
        stop  = git_repo_anchor.get_center()+RIGHT*self.icon_height
        arrow = CurvedArrow(start, stop, angle=PI/2)
        internet = internet_icon(height=0.5).next_to(arrow, DOWN, buff=-0.3)
        sep = vertical_separator(repo1, repo2.target)


        self.play(ShowCreation(git_repo_anchor), MoveToTarget(repo2),
                  FadeIn(arrow), FadeIn(internet))
        self.wait()


        display.display("this will duplicate the commits\n"
                        "on your computer")

        self.play(FadeOut(arrow), FadeOut(internet), ShowCreation(sep))
        #self.wait()

        # shrink down the github area
        NORMAL_github_anchor = github_anchor.deepcopy()
        NORMAL_repo1 =  repo1.deepcopy()
        NORMAL_sep = sep.deepcopy()
        github_anchor.generate_target()
        github_anchor.target.shift(RIGHT).scale(0.5)
        repo1.generate_target()
        repo1.target.scale(0.5).next_to(github_anchor.target, DOWN, buff=0.5)
        d = RIGHT*2
        git_repo_anchor.generate_target()
        git_repo_anchor.target.shift(d)
        repo2.generate_target()
        repo2.target.shift(d)
        new_sep = vertical_separator(repo1.target, repo2.target)
        self.play(*(MoveToTarget(x)
                    for x in (github_anchor, repo1, repo2, git_repo_anchor)),
                  Transform(sep, new_sep))
        self.wait()

        index_anchor = index_icon(height=self.icon_height).shift(0.5*LEFT)
        class MyIndex(Index):
            CONFIG = dict(
                index_width=3,
            )
            def nail(self, other):
                super().nail(other)
                other.next_to(index_anchor, DOWN, buff=0.5)
                return other


        display.display("and then populate the index")

        index = MyIndex("------", color=RED)
        self.play(ShowCreation(index_anchor),
                  *index.create_animations(self))
        self.play(*index.morph_animations(self, repo2.current_commit))
        index.clean_morph(self)

        display.display(".. and files")

        file_system_anchor = (file_system_icon(height=self.icon_height)
                              .shift(1.5*RIGHT))
        class MyEditable(Editable):
            CONFIG = dict(
                filesystem_width=3,
            )
            def nail(self, other):
                super().nail(other)
                other.next_to(file_system_anchor, DOWN, buff=0.5)

        editable = MyEditable("")
        self.play(ShowCreation(editable), ShowCreation(file_system_anchor))
        self.play(*editable.morph_animations(self, index))
        editable.clean_morph(self)


        display.display("and you're all set")
        self.wait()

        display.hide()
        self.wait()

        # focus on github : move local stuff left
        # and resize back github repo to normal size
        SMALL_github_anchor = github_anchor.deepcopy()
        SMALL_sep = sep.deepcopy()

        display.display("after some time\nsomebody else publishes upstream")

        LEFT_MOVE = 2*LEFT
        local_group = Group(file_system_anchor, editable,
                  index_anchor, index,
                  git_repo_anchor, repo2)
        self.play(local_group.shift, LEFT_MOVE,
                  Transform(github_anchor, NORMAL_github_anchor),
                  Transform(sep, NORMAL_sep),
                  Transform(repo1, NORMAL_repo1))
        self.wait()

        # add h4 from the outside
        #repo1.add_target()
        repo1.add_commit(MyCommit("h4", text=C4_BODY), "h3")
        repo1.find_commit("h3").set_refs()
        repo1.find_commit("h4").set_refs("main")
        repo1.flush(self)
        self.wait()

        display.hide()
        # refocus on the local repo
        repo1.generate_target()
                # somehow repo1 is now very large in the Y direction on the left hand side
        # so we need to tweak this
        repo1.target.scale(0.5)
        repo1.nail(repo1.target)
        self.play(local_group.shift, -LEFT_MOVE,
                  Transform(github_anchor, SMALL_github_anchor),
                  Transform(sep, SMALL_sep),
                  MoveToTarget(repo1))
        self.wait()

        display.display("how can we cope with that ?")
        self.wait()

        display.display("git fetch", console=True)

        repo2.add_commit(MyCommit("h4", text=C4_BODY), "h3")
        repo2.set_current_commit("h3")
        repo2.find_commit("h4").set_refs("origin/main")

        repo2.flush(self)
        self.wait()


        display.display("fetch ONLY duplicates the missing\n"
                        "commits in the local repo\n"
                        "but it DOES NOT alter\n"
                        "current commit nor index nor files")
        self.wait()


        display.display("it does keep track\n"
                        "of the remote branches though,\n"
                        "by adding references like this one")

        repo2.find_commit("h4").outline_ref("origin/main", scale=3, color=RED)
        repo2.flush(self)
        self.wait()

        display.display("now that we have this new commit\n"
                        "locally, in order to catch up\n"
                        "we just need to merge it !\n"
                        "(and here it's a fast-forward merge)")
        self.wait()

        display.display("git merge origin/main", console=True)
        repo2.set_current_commit("h4")
        repo2.flush(self)
        self.wait(0.5)
        repo2.find_commit("h3").set_refs()
        repo2.find_commit("h4").set_refs("main", "origin/main")
        repo2.flush(self)
        self.wait(0.5)
        self.play(*index.morph_animations(self, repo2.current_commit))
        index.clean_morph(self)
        self.play(*editable.morph_animations(self, index))
        editable.clean_morph(self)
        self.wait()

        display.display("as it happens, the sequence\n"
                        "git fetch + git merge\n"
                        "is exactly the purpose of\n"
                        "git pull")

        self.wait(2)

class PullDiverge(Scene):
    CONFIG = dict(
        icon_height=0.8,
    )
    def construct(self):

        #self.add(ScreenGrid())

        def legend_position(legend):
            legend.to_edge(DOWN).shift(UP)
        display = Display(self, position_lambda=legend_position)

        display.display("sometimes\ngit pull\n"
                        "needs to create\n a local commit")
        self.wait()


        display.display("from 2 repos\nin sync")
        github_anchor = (github_icon(height=self.icon_height)
                         .to_corner(UR).shift(3*LEFT))
        git_repo_anchor = (git_repo_icon(height=self.icon_height)
                           .to_corner(UR).shift(9.5*LEFT))
        class GithubRepo(Repo):
            CONFIG = dict(
                hash_size=0.25,
                arrow_color=RED,
                y_stretch=1.5,
            )
            def nail(self, other):
                other.next_to(github_anchor, DOWN, buff=0.5)

        class MyRepo(Repo):
            CONFIG = dict(
                hash_size=0.25,
                arrow_color=GREEN,
                y_stretch=1.5,
            )
            def nail(self, other):
                other.next_to(git_repo_anchor, DOWN, buff=0.5)

        class MyCommit(Commit):
            CONFIG = dict(
                hash_size=0.3,
                hash_buff=0.3,
                refs_size=0.15,
                refs_buff=0.15,
#                regular_stroke_width=3,
#                current_stroke_width=6,
            )
            def __init__(self, commit, *args, **kwds):
                super().__init__(commit, text=" ", *args, **kwds)

        repo1 = GithubRepo()
        repo1.add_commit(MyCommit("h1")).hash_location = RIGHT
        repo1.add_commit(MyCommit("h2"), "h1").hash_location = RIGHT

        self.add(github_anchor)
        self.add(repo1.add_target())


        repo2 = MyRepo()
        repo2.add_commit(MyCommit("h1"))
        repo2.add_commit(MyCommit("h2"), "h1")

        self.add(git_repo_anchor)
        self.add(repo2.add_target())
        self.wait()


        display.display("something new\non github")
        repo1.add_commit(MyCommit("theirs"), "h2").hash_location = RIGHT
        repo1.find_commit("theirs").set_refs("main")
        repo1.flush(self)
        self.wait()

        display.display("AND a local\ncommit")
        repo2.add_commit(MyCommit("ours"), "h2")
        repo2.find_commit("ours").set_refs("main")
        repo2.flush(self)
        self.wait()

        display.display("git pull\nstarts with a\ngit fetch")
        repo2.add_commit(MyCommit("theirs"), "h2", current=False).hash_location = RIGHT
        repo2.find_commit("ours").set_refs("main")
        repo2.find_commit("ours").outline_ref("main")
        repo2.find_commit("theirs").set_refs("origin/main")
        repo2.find_commit("theirs").outline_ref("origin/main")
        repo2.flush(self)
        self.wait()

        display.display("now git merge\nhas no other\nchoice")
        self.wait()

        display.display("than to create\na new commit")
        repo2.add_commit(MyCommit("h4"), "ours", "theirs")
        repo2.find_commit("h4").set_refs("main")
        repo2.find_commit("theirs").set_refs("origin/main")
        repo2.find_commit("ours").set_refs()
        repo2.flush(self)
        self.wait()
