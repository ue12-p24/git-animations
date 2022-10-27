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
class PushAndNeedPull(Scene):
    CONFIG = dict(
        icon_height=0.8,
    )
    def construct(self):

        #self.add(ScreenGrid())

        def nail_legend(legend):
            legend.to_edge(DOWN).shift(UP)
        display = Display(self, position_lambda=nail_legend)

        display.display("to export your stuff\nuse, wait for it...\ngit push")
        self.wait()


        display.display("from 2 repos\nin sync")

        github_anchor = (github_icon(height=self.icon_height)
                         .to_corner(UR).shift(2.5*LEFT))
        git_repo_anchor = (git_repo_icon(height=self.icon_height)
                           .to_corner(UR).shift(10*LEFT))

        class GithubRepo(Repo):
            CONFIG = dict(
                hash_size=0.25,
                arrow_color=GREEN,
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
        repo1.find_commit("h2").set_refs("main")

        self.add(github_anchor)
        self.add(repo1.add_target())


        repo2 = MyRepo()
        repo2.add_commit(MyCommit("h1"))
        repo2.add_commit(MyCommit("h2"), "h1")
        repo2.find_commit("h2").set_refs("main")
        repo2.generate_target()
        #repo2.target.shift(4*LEFT)
#        repo2.nail(repo2.target)

        self.add(git_repo_anchor)
        self.add(repo2.add_target())
        self.wait()

        display.display("you create\nlocal commits")
        repo2.add_commit(MyCommit("h3"), "h2")
        repo2.add_commit(MyCommit("h4"), "h3")
        repo2.find_commit("h2").set_refs()
        repo2.find_commit("h4").set_refs("main")
        repo2.flush(self)
        self.wait()

        display.display("to an extent\ngit push\nworks a bit\nlike git pull")
        self.wait()

        display.display("it will first\nduplicate\n"
                        "your commits\non the remote side")
        repo1.add_commit(MyCommit("h3"), "h2", current=False).hash_location = RIGHT
        repo1.add_commit(MyCommit("h4"), "h3", current=False).hash_location = RIGHT
        repo1.find_commit("h4").set_refs("pushing/main")
        repo1.flush(self)
        self.wait()

        display.display("and then merge\non the remote side")
        repo1.set_current_commit("h4")
        repo1.find_commit("h2").set_refs()
        repo1.find_commit("h2").set_refs()
        repo1.find_commit("h4").set_refs("main")
        repo1.flush(self)
        self.wait()

        display.display("BUT!!\ngit push will\n"
                        "cowardly REFUSE\n"
                        "to CREATE\na merge commit\n")
        self.wait()

        display.display("assume you\ncreate a local\ncommit")
        repo2.add_commit(MyCommit("ours"), "h4")
        repo2.find_commit("h4").set_refs()
        repo2.find_commit("ours").set_refs("main")
        repo2.flush(self)
        self.wait()

        display.display("also assume\n"
                        "somebody else\nhas been\n"
                        "working on the\n"
                        "same commit\n")
        self.wait()

        display.display("AND they manage\n"
                        "to push\n"
                        "theirs first\n")
        repo1.add_commit(MyCommit("theirs"), "h4").hash_location = RIGHT
        repo1.find_commit("h4").set_refs()
        repo1.find_commit("theirs").set_refs("main")
        repo1.flush(self)
        self.wait()

        display.display("then at\nthat point you\nCANNOT PUSH !!!")
        self.wait()

        display.display("because\nthat would mean..")
        repo1.add_commit(MyCommit("ours"), "h4",
                         current=False).set_refs("pushing/main")
        # preserve apparent order
        repo1.swap_commits("ours", "theirs")
        repo1.flush(self)
        self.wait()

        display.display("that push\nwould need to\ncreate a commit\nremotely")
        c = repo1.add_commit(MyCommit("merged"), "ours", "theirs", current=False)
        repo1.flush(self)
        cross = VGroup()
        cross.add(Line(UP+RIGHT, -(UP+RIGHT)).set_color(RED).set_stroke(width=10, color=RED))
        cross.add(Line(UP+LEFT, -(UP+LEFT)).set_color(RED).set_stroke(width=10, color=RED))
        cross.scale(0.6*c.commit_width)
        cross.move_to(c.get_center())
        self.play(ShowCreation(cross))
        self.wait()
        display.display("and that is\nNOT ALLOWED")
        self.wait()
        display.display("as it might\ninvolve conflicts")
        footnote = Paragraph(r"if you try, git push",
                             "will complain about",
                             "the remote merge",
                             "not being",
                             "a fast-foward",
                             font="Times",
                             color=RED)
        footnote.to_edge(UP)
        self.add(footnote)
        self.wait()
        self.wait()

        self.remove(footnote)
        display.display("so here instead")
        repo1.delete_commit("ours")
        repo1.delete_commit("merged")
        repo1.clear_layout()
        self.remove(cross)
        repo1.flush(self)
        self.wait()

        display.display("FIRST you\n"
                        "need to do a\ngit pull")
        repo2.add_commit(MyCommit("theirs"), "h4", current=False)\
            .set_refs("origin/main")\
            .hash_location = RIGHT
        repo2.flush(self)
        self.wait()

        display.display("so the merge\nis done locally")
        repo2.add_commit(MyCommit("merged"), "ours", "theirs").set_refs("main")
        repo2.find_commit("ours").set_refs()
        repo2.flush(self)
        self.wait()
        display.display("and you can\ndeal with conflicts\nif any")
        self.wait()

        display.display("and NOW\nyou can push")
        repo1.add_commit(MyCommit("ours"), "h4")
        repo1.swap_commits("ours", "theirs")
        repo1.add_commit(MyCommit("merged"), "ours", "theirs").set_refs("main")
        repo1.find_commit("theirs").set_refs()
        repo2.find_commit("theirs").set_refs()
        repo2.find_commit("merged").set_refs("main", "origin/main")
        repo1.flush(self)
        repo2.flush(self)
        self.wait()

        display.display("since now the\nremote merge\nis a fast-forward")
        self.wait()
