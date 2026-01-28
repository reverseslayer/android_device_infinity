#
# Copyright (C) 2021-2025 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Partitions
BOARD_SUPER_PARTITION_SIZE := 13329498112

# Fix for mismatch of android.media.audio.common.types-V4 & V5 mismatch
BUILD_BROKEN_VINTF_PRODUCT_COPY_FILES := true

# Include the common OEM chipset BoardConfig.
include device/oplus/sm8850-common/BoardConfigCommon.mk

DEVICE_PATH := device/oplus/infinity

# Assert
TARGET_OTA_ASSERT_DEVICE := OP5D0DL1,OP5D55L1

# Display
TARGET_SCREEN_DENSITY := 640

# Kernel
TARGET_KERNEL_ADDITIONAL_FLAGS += CONFIG_CPH2749_DTB=y

# Properties
TARGET_ODM_PROP += $(DEVICE_PATH)/odm.prop
TARGET_SYSTEM_EXT_PROP += $(DEVICE_PATH)/system_ext.prop
TARGET_VENDOR_PROP += $(DEVICE_PATH)/vendor.prop

# Recovery
TARGET_RECOVERY_UI_MARGIN_HEIGHT := 103

# Include the proprietary files BoardConfig.
include vendor/oplus/infinity/BoardConfigVendor.mk
