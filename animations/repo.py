from collections import defaultdict

import numpy as np

from grandalf.graphs import Vertex, Edge, Graph as GrandalfGraph
from grandalf.layouts import SugiyamaLayout, DigcoLayout

from manimlib.imports import *

from coloredfile import ColoredFile

# for grandalf
class DefaultView:
    w, h = 0, 0

# helpful when displaying objects and animations
class Hash(Text):
    pass

class CommitCircle(Circle):
    def __init__(self, commit, *a, **k):
        self.commit = commit
        super().__init__(*a, **k)

    def show_current(self):
        self.set_stroke(
            width=(
                self.commit.current_stroke_width if self.commit.is_current
                else self.commit.regular_stroke_width),
            color=(
                self.commit.current_stroke_color if self.commit.is_current
                else self.commit.regular_stroke_color))


    # used only in ObsoleteRepo
    def propagate_scale(self, *a, **k):
        self.commit.hash.scale(*a, **k)
        self.commit.make_it_fit()


class Commit(ColoredFile):
    CONFIG = dict(
        commit_width=1,
        hash_font='courier',
        hash_location=LEFT,
        hash_size=0.5,
        hash_buff=0.3,
        refs_font='courier',
        refs_location=DOWN,
        refs_size=0.35,
        refs_buff=0.3,
        is_current=False,
        regular_stroke_width=2,
        current_stroke_width=5,
        regular_stroke_color=GREY,
        current_stroke_color=BLUE,
    )
    def __init__(self, hash: str,
                 *a, font="courier", text=None, refs=None, **k):
        if text is None:
            text = hash
        if refs is None:
            refs = []
        super().__init__(text, font=font, *a, **k)
        self.hash = Hash(hash, font=self.hash_font)
        self.circle = CommitCircle(self)
        self.refs = refs
        self.grefs = VGroup()
        self.reset_decoration_sizes()
        self.make_it_fit()

    def update_decorations(self):
        self.circle.move_to(self.get_center())
        self.circle.show_current()
        self.hash.next_to(self.circle, self.hash_location, buff=self.hash_buff)
        self.grefs.next_to(self.hash, self.refs_location, buff=self.refs_buff)

    def reset_decoration_sizes(self):
        self.circle.set_width(self.commit_width)
        self.hash.scale(self.hash_size/self.hash.get_height())
#        for ref in self.grefs:
#            ref.scale(self.refs_size/ref.get_height())

    def make_it_fit(self, target=None):
        if target is None:
            target = self
        w, h = target.get_width(), target.get_height()
        alpha = math.atan2(h, w)
        cos = math.cos(alpha)
        if w == 0:
            scale = 1
        else:
            scale = (self.circle.get_width()*cos/w) * 0.95
        target.scale(scale)

    def add_in(self, container):
        self.make_it_fit()
        self.update_decorations()
        container.add(self)
        container.add(self.hash)
        container.add(self.circle)
        container.add(self.grefs)

    def create_morph_animations(self, scene, original: Paragraph):
        self.add_updater(Commit.update_decorations)
        # this creates an extra Paragraph
        floating = original.copy()
        floating.generate_target()
        floating.target.move_to(self.get_center())
        self.make_it_fit(floating.target)
        self._floatings.append(floating)

        return [
            ShowCreation(self.circle),
            ShowCreation(self.hash),
            MoveToTarget(floating),
            Transform(self, floating.target),
        ]

    # used only in ObsoleteRepo
    def move_in_circle(self):
        """
        when e.g. a VGroup is laying us out, it uses
        the circles and not the Paragraphs
        (that have inconsistent heights)
        """
        self.move_to(self.circle.get_center())

    def set_refs(self, *refs):
        self.refs = refs
        self.update_refs()
        return self

    def update_refs(self):
        group = self.grefs
        # clean up
        for former in group.submobjects:
            group.remove(former)
        # populate again
        def oneref(ref):
            label = Text(ref, font=self.refs_font)
            label.scale(self.refs_size/label.get_height())
            return label
        for ref in self.refs:
            group.add(oneref(ref))
        group.arrange(self.refs_location, buff=self.refs_buff)
        group.next_to(self.hash, self.refs_location, buff=self.refs_buff)


    def outline_ref(self, ref, scale=2, color=RED):
        group = self.grefs
        for label in group:
            if label.text == ref:
                (label
                 .scale(scale*self.refs_size/label.get_height())
                 .set_color(color))
                group.arrange(self.refs_location, buff=self.refs_buff)
                group.next_to(self.hash, self.refs_location, buff=self.refs_buff)
                return
        print(f"ERROR, no such ref to outline {ref}")


class Repo(VGroup):

    # hard-wired constants that bring
    # grandalf units into a 1x1 grid
    GR_X_RATIO = 10
    GR_Y_RATIO = 20

    CONFIG = dict(
        font="times",
        circle_color=GREY,
        # apply transform on grandalf coord system
        x_stretch=1,
        y_stretch=2,
        arrow_width=3,
        arrow_color=BLUE,
#        arrow_tip_length=1,
    )
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.commits = []
        self.neighbours = defaultdict(list)
        self.current_commit = None
        self.debug_graph = False

    def nail(self, other):
        return self

    def describe(self, debug=False):
        print(f"repo of class {type(self).__name__} "
              f"with {len(self.commits)} commits "
              f"and {sum(len(n) for n in self.neighbours.values())} links")
        if debug:
            print("vertices")
            for i, c in enumerate(self.commits, 1):
                print(f"{i}: {c.hash.text}")
                for n in self.neighbours[c]:
                    print(f"  {c.hash.text} -> {n.hash.text}")
            print("edges")
            for c, ns in self.neighbours.items():
                for n in ns:
                    print(f"{c.hash.text} -> {n.hash.text}")

    # unfortunately this requires to be made in an instant
    def flush(self, scene):
        scene.play(Transform(self, self.update_target()), run_time=0)

    # regular copies will miss the management
    # of current_commit that od course needs
    # to be a reference among self.commits
    def copy(self):
        c = super().copy()
        for cs, cd in zip(self.commits, c.commits):
            if cs == self.current_commit:
                c.current_commit = cd
        return c

    def deepcopy(self):
        c = super().deepcopy()
        for cs, cd in zip(self.commits, c.commits):
            if cs == self.current_commit:
                c.current_commit = cd
        return c

    def set_current_commit(self, commit):
        commit = self.find_commit(commit)
        if self.current_commit:
            self.current_commit.is_current = False
        commit.is_current = True
        self.current_commit = commit

    def find_commit(self, commit_or_hash):
        for c in self.commits:
            if c is commit_or_hash or c.hash.text == commit_or_hash:
                return c
        print(f"ERROR - could not find {commit_or_hash} in repo")

    def add_commit(self, commit, *linked, current=True):
        self.commits.append(commit)
        for c in linked:
            self.add_link(commit, self.find_commit(c))
        if current:
            self.set_current_commit(commit)
        return commit

    def delete_commit(self, commit):
        c = self.find_commit(commit)
        if not c:
            print(f"ERROR, cannot delete commit {commit}")
            return
        self.commits.remove(c)
        if c in self.neighbours:
            del self.neighbours[c]
        for src, dsts in self.neighbours.items():
            if c in dsts:
                dsts.remove(c)


    def add_link(self, c1, c2):
        self.neighbours[c1].insert(0, c2)

    def swap_commits(self, c1, c2):
        c1 = self.find_commit(c1)
        c2 = self.find_commit(c2)
        L = self.commits
        i1 = self.commits.index(c1)
        i2 = self.commits.index(c2)
        L[i1], L[i2] = L[i2], L[i1]


    def clear_layout(self):
        for c in self.commits:
            if hasattr(c, 'coords'):
                del c.coords

    def layout(self):
        """
        make sure all commits have a coords attribute
        use grandalf to compute one if not all commits have one
        """
        if all(hasattr(c, 'coords') for c in self.commits):
            # all nodes already positioned
            return
        # use grandalf algo to do the layout
        # it's a little messy to get the vertices in the order we want
        # which is first on the left
        v_index = {commit: Vertex((i, commit.hash))
                   for i, commit in enumerate(self.commits)}

        V = list(v_index.values())

        E = [Edge(v_index[c1], v_index[c2])
             for c1, neighbours in self.neighbours.items()
             for c2 in (neighbours)]
        # that's the tricky part, sort the whole set of edges
        def edge_key(e):
            src, dst = e.v
            return (src.data[0], -dst.data[0])
        E.sort(key=edge_key, reverse=True)

        if self.debug_graph:
            print("-- in layout: vertices")
            for i, v in enumerate(V, 1):
                print(f"v{i}: {v.data[1].text}")
            print("-- in layout: edges")
            for i, e in enumerate(E, 1):
                f, t = e.v
                print(f"{i} {f.data[1].text} -> {t.data[1].text}")

        ###
        g = GrandalfGraph(V, E)
        connex = g.C[0]

        for v in V:
            v.view = DefaultView()
        sug = SugiyamaLayout(connex)
        roots = [v for v in connex.sV if not v.e_in()]
        sug.init_all(roots=roots)
        sug.draw()

        # grandalf does top to bottom
        miny, maxy = 1000, -1000
        for c in self.commits:
            x, y = v_index[c].view.xy
            c.coords = [x/self.GR_X_RATIO*self.x_stretch,
                        y/self.GR_Y_RATIO*self.y_stretch]
            miny = min(miny, c.coords[1])
            maxy = max(maxy, c.coords[1])
        def upside_down(y):
            return miny+maxy-y
        for c in self.commits:
            c.coords[1] = upside_down(c.coords[1])


    def add_target(self):
        return self._make_target(first_time=True)
    def update_target(self):
        return self._make_target(first_time=False)


    def _make_target(self, first_time=False):
        """
        move commits according to their coords
        """
        self.layout()
        target = self.__class__() if not first_time else self

        # clear the VGroup contents
        for x in self[:]:
            self.remove(x)

        for c in self.commits:
            x, y = c.coords
            c.reset_decoration_sizes()
            c.move_to(x*RIGHT+y*UP)
            c.add_in(target)
        for com1, neighbours in self.neighbours.items():
            for com2 in neighbours:
                c1, c2 = com1.get_center(), com2.get_center()
                v = c2-c1
                # compute the ends of the link - not overlapping the circles
                l = np.linalg.norm(v)
                x1, y1, _ = c1 + (v/l*com1.commit_width/2)
                x2, y2,_ = c2 - (v/l*com2.commit_width/2)
                e1, e2 = x1*RIGHT+y1*UP, x2*RIGHT+y2*UP
                # adding tip_length=10 to Arrow creation below
                # behaves odd, forget about arrow tips for now
                target.add(Arrow(e1, e2, buff=0)
                           .set_color(self.arrow_color)
                           .set_stroke(width=self.arrow_width,
                                       color=self.arrow_color))
        self.nail(target)
        return target



class ObsoleteRepo(VGroup):
    CONFIG = dict(
        direction=DOWN,
        arrow_height=0.5,
        down_scaling=None,
        buff=0,
    )
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    def nail(self, other):
        return self

    def adopt_initial(self, c: Commit):
        self.add_to_back(c.circle)
        self.arrange(self.direction, buff=self.buff)
        self.nail(self)
        self.move_commits_in_their_circles()

    def adopt_further(self, c: Commit):
        if self.down_scaling is not None:
            for x in self.submobjects:
                x.scale(self.down_scaling)
                if isinstance(x, CommitCircle):
                    x.propagate_scale(self.down_scaling)
        a = Arrow(-self.direction, self.direction)
        a.set_height(self.arrow_height)
        self.add_to_back(a)
        self.add_to_back(c.circle)
        self.arrange(self.direction, buff=self.buff)
        self.nail(self)
        self.move_commits_in_their_circles()

    def move_commits_in_their_circles(self):
        for c in self.submobjects:
            if isinstance(c, CommitCircle):
                c.commit.move_in_circle()
