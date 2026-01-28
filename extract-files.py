#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import ( blob_fixup, blob_fixups_user_type )
from extract_utils.fixups_lib import ( lib_fixups, lib_fixup_remove )
from extract_utils.main import ( ExtractUtils, ExtractUtilsModule )

namespace_imports = [
    "hardware/oplus",
    "hardware/qcom-caf/sm8850",
    "vendor/oplus/sm8850-common",
    "vendor/qcom/opensource/commonsys-intf/display",
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    'android.hardware.camera.device-V2-ndk': 'android.hardware.camera.device-V3-ndk',
    'android.hardware.camera.metadata-V2-ndk': 'android.hardware.camera.metadata-V3-ndk',
    'android.hardware.graphics.allocator-V1-ndk': 'android.hardware.graphics.allocator-V2-ndk',
    'vendor.oplus.hardware.charger-V8-ndk': lambda lib, part: 'vendor.oplus.hardware.charger-V9-ndk',
    (
        'android.hardware.camera.common-V1-ndk',
        'android.hardware.graphics.common-V5-ndk',
        'vendor.qti.hardware.camera.offlinecamera-V2-ndk',
        'libstdc++',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/com.oplus.mcx.linearmapper.so': blob_fixup()
        .replace_needed('vendor.oplus.hardware.charger-V8-ndk.so', 'vendor.oplus.hardware.charger-V9-ndk.so'),
    'vendor/lib64/vendor.oplus.hardware.charger-V1-service-impl.so': blob_fixup()
        .replace_needed('vendor.oplus.hardware.charger-V8-ndk.so', 'vendor.oplus.hardware.charger-V9-ndk.so'),
    'vendor/lib64/vendor.qti.hardware.camera.offlinecamera-service-impl.so': blob_fixup()
        .replace_needed('android.hardware.camera.metadata-V2-ndk.so', 'android.hardware.camera.metadata-V3-ndk.so')
        .replace_needed('android.hardware.camera.device-V2-ndk.so', 'android.hardware.camera.device-V3-ndk.so')
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so'),
    'vendor/lib64/camera/components/com.qti.node.dewarp.so': blob_fixup()
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so'),
    'odm/etc/camera/CameraHWConfiguration.config': blob_fixup()
        .regex_replace(r'(enableSWfdForThirdCamUnit += )TRUE', r'\1FALSE')
        .regex_replace(r'(fdSupport += )TRUE;', r'\1FALSE;'),
    'odm/etc/init/init.camera_process.rc': blob_fixup()
        .regex_replace('    delete_recursion', '    #delete_recursion'),
    (
        'odm/etc/libnfc-mtp-SN220.conf_23821',
        'odm/etc/libnfc-mtp-SN220.conf_23893'
    ): blob_fixup()
        .regex_replace('(NXPLOG_.*_LOGLEVEL)=0x03', '\\1=0x02')
        .regex_replace('NFC_DEBUG_ENABLED=1', 'NFC_DEBUG_ENABLED=0'),
    'odm/firmware/fastchg/24831/charging_hyper_mode_config.txt': blob_fixup()
        .regex_replace(r"(PROJECT:=)23893", r"\g<1>24831"),
    'odm/lib64/libAlgoProcess.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V6-ndk.so'),
    (
        'odm/lib64/libAncHumanSegFigureFusion.so',
        'odm/lib64/libEIS.so',
        'odm/lib64/libHIS.so',
        'odm/lib64/libOPAlgoCamAiBeautyFaceRetouchCn.so',
        'odm/lib64/libOPAlgoCamAiUnifySkin.so',
        'odm/lib64/libOPAlgoCamFaceBeautyCap.so',
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_acquire')
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'odm/lib64/libextensionlayer.so': blob_fixup()
        .replace_needed('vendor.oplus.hardware.performance-V1-ndk_platform.so', 'vendor.oplus.hardware.performance-V1-ndk.so'),
    'odm/lib64/libsensorbridge.so': blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),
    'vendor/etc/libnfc-nci.conf': blob_fixup()
        .regex_replace('NFC_DEBUG_ENABLED=1', 'NFC_DEBUG_ENABLED=0'),
}  # fmt: skip

module = ExtractUtilsModule(
    "infinity",
    "oplus",
    namespace_imports=namespace_imports,
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    add_firmware_proprietary_file=True,
)

if __name__ == "__main__":
    utils = ExtractUtils.device_with_common(module, "sm8850-common", module.vendor)
    utils.run()
