LIBS = bricks.py repo.py coloredfile.py

CURRENT = dev-push

current: $(CURRENT)

all: medium

everything: low medium high ultra
files: files-low files-medium

# $(1) = the Python classname
# $(2) = the Python source .py
# $(3) = the shorcut to build make targets
define scene_target
$(3): medium-$(3)

ultra:: media/videos/$(subst .py,,$(2))/1440p60/$(1).mp4
ultra-$(3): media/videos/$(subst .py,,$(2))/1440p60/$(1).mp4
media/videos/$(subst .py,,$(2))/1440p60/$(1).mp4: $(2) $(LIBS)
	manim $(2) $(1)

high:: media/videos/$(subst .py,,$(2))/1080p60/$(1).mp4
high-$(3): media/videos/$(subst .py,,$(2))/1080p60/$(1).mp4
media/videos/$(subst .py,,$(2))/1080p60/$(1).mp4: $(2) $(LIBS)
	manim --high_quality --leave_progress_bars $(2) $(1)

medium:: media/videos/$(subst .py,,$(2))/720p30/$(1).mp4
medium-$(3): media/videos/$(subst .py,,$(2))/720p30/$(1).mp4
media/videos/$(subst .py,,$(2))/720p30/$(1).mp4: $(2) $(LIBS)
	manim -m --leave_progress_bars $(2) $(1)

low:: media/videos/$(subst .py,,$(2))/480p15/$(1).mp4
low-$(3): media/videos/$(subst .py,,$(2))/480p15/$(1).mp4
media/videos/$(subst .py,,$(2))/480p15/$(1).mp4: $(2) $(LIBS)
	manim -l --leave_progress_bars $(2) $(1)

dev-$(3): 
	manim -lp --leave_progress_bars $(2) $(1)

files-medium::
	-@ls -1 media/videos/$(subst .py,,$(2))/720p30/$(1).mp4
files-low::
	-@ls -1 media/videos/$(subst .py,,$(2))/480p15/$(1).mp4
files-$(3):
	-@ls -1 media/videos/$(subst .py,,$(2))/*/$(1).mp4
files-all::
	-@ls -1 media/videos/$(subst .py,,$(2))/*/$(1).mp4
files-all::
	-@ls -1 media/videos/$(subst .py,,$(2))/*/$(1).mp4
clean::
	rm media/videos/$(subst .py,,$(2))/*/$(1).mp4
endef

$(eval $(call scene_target,NoIndex,scenesindex.py,noindex))
$(eval $(call scene_target,WithIndex,scenesindex.py,withindex))
$(eval $(call scene_target,CloneAndPull,scenespull.py,clone))
$(eval $(call scene_target,PullDiverge,scenespull.py,diverge))
$(eval $(call scene_target,PushAndNeedPull,scenespush.py,push))
