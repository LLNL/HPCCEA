# this file was copied directly from cisco_ucs/Makefile.am

MAINTAINERCLEANFILES	= Makefile.in

TARGET			= fence_powerman

SRC			= $(TARGET).py

EXTRA_DIST		= $(SRC)

sbin_SCRIPTS		= $(TARGET)

#man_MANS		= $(TARGET).8

# this next line was in the cisco_ucs file, but there currently aren't tests defined
# for this fencing device
# FENCE_TEST_ARGS         = -l test -p test -a test -n 1

include $(top_srcdir)/make/fencebuild.mk
include $(top_srcdir)/make/fenceman.mk
include $(top_srcdir)/make/agentpycheck.mk
