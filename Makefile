define root.patched/pre
		fab-apply-overlay gems.overlay $O/root.patched
endef

WEBMIN_FW_TCP_INCOMING = 22 80 443 3690 4155 8080 9418 12320 12321

COMMON_CONF = mercurial-apache

include $(FAB_PATH)/common/mk/turnkey/revisioncontrol.mk
include $(FAB_PATH)/common/mk/turnkey/rails.mk
include $(FAB_PATH)/common/mk/turnkey.mk
