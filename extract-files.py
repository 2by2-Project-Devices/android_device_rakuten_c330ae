#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/rakuten/c330ae',
    'hardware/qcom-caf/msm8953',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/display',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None
lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
}

# Define the blob fixups
blob_fixups: blob_fixups_user_type = {
    # Camera - Path fixups
    'vendor/bin/mm-qcamera-daemon': blob_fixup()
        .binary_regex_replace(b'/data/misc/camera/cam_socket', b'/data/vendor/qcam/cam_socket'),
    'vendor/lib/libmmcamera2_sensor_modules.so': blob_fixup()
        .binary_regex_replace(b'/system/etc/camera', b'/vendor/etc/camera'),
    ('vendor/lib/libmmcamera2_cpp_module.so', 'vendor/lib/libmmcamera2_dcrf.so', 'vendor/lib/libmmcamera2_iface_modules.so', 'vendor/lib/libmmcamera2_imglib_modules.so', 'vendor/lib/libmmcamera2_mct.so', 'vendor/lib/libmmcamera2_pproc_modules.so', 'vendor/lib/libmmcamera2_q3a_core.so', 'vendor/lib/libmmcamera2_sensor_modules.so', 'vendor/lib/libmmcamera2_stats_algorithm.so', 'vendor/lib/libmmcamera2_stats_modules.so', 'vendor/lib/libmmcamera_dbg.so', 'vendor/lib/libmmcamera_imglib.so', 'vendor/lib/libmmcamera_pdafcamif.so', 'vendor/lib/libmmcamera_pdaf.so', 'vendor/lib/libmmcamera_tintless_algo.so', 'vendor/lib/libmmcamera_tintless_bg_pca_algo.so', 'vendor/lib/libmmcamera_tuning.so'): blob_fixup()
        .binary_regex_replace(b'/data/misc/camera/', b'/data/vendor/qcam/'),
    # Camera - Property fixup
    'vendor/lib/libmmcamera_dbg.so': blob_fixup()
        .binary_regex_replace(b'persist.camera.debug.logfile', b'persist.vendor.camera.dbglog'),
    # Camera - - libstdc++.so' -> 'libstdc++_vendor.so
    ('vendor/lib/libmmcamera_hdr_gb_lib.so', 'vendor/lib/libmpbase.so', 'vendor/lib/liboptizoom.so', 'vendor/lib/libseemore.so', 'vendor/lib/libtrueportrait.so', 'vendor/lib/libubifocus.so', 'vendor/lib/libchromaflash.so'): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    # Camera - shims, uneeded & VNDK fixups
    'vendor/lib/libmmcamera_ppeiscore.so': blob_fixup()
        .add_needed('libppeiscore_shim.so')
        .replace_needed('libGLESv2.so', 'libGLESv2_adreno.so'),
    'vendor/lib/libmmcamera_tuning.so': blob_fixup()
        .remove_needed('libmm-qcamera.so'),
    ('vendor/lib/libmmcamera2_stats_modules.so', 'vendor/lib/libmpbase.so'): blob_fixup()
        .add_needed('libcamshim.so')
        .remove_needed('libandroid.so'),
    # Camera - liblog dep.
    ('vendor/lib/libmmcamera_dbg.so', 'vendor/lib/libmmcamera_pdafcamif.so', 'vendor/lib/libmmcamera_pdaf.so', 'vendor/lib/libmmcamera_imx258_mono.so', 'vendor/lib/libjpegehw.so', 'vendor/lib/libjpegdhw.so', 'vendor/lib/libmmcamera_hdr_gb_lib.so', 'vendor/lib/libmmcamera_imx258_ofilm.so', 'vendor/lib/libmmcamera_imx258_sunny.so', 'vendor/lib/libmmcamera2_sensor_modules.so', 'vendor/lib/libjpegdmahw.so', 'vendor/lib/libmmcamera_imx258.so', 'vendor/lib/libmmcamera_imx258_qtech.so', 'vendor/lib/libmmcamera_le2464c_master_eeprom.so', 'vendor/lib/libmmcamera_tintless_bg_pca_algo.so', 'vendor/lib/libqomx_jpegenc.so', 'vendor/lib/libqomx_jpegdec.so', 'vendor/lib/libqomx_jpegenc_pipe.so'): blob_fixup()
        .add_needed('liblog.so'),
    # Dolby
    ('vendor/lib64/libdlbdsservice.so', 'vendor/lib/libstagefright_soft_ddpdec.so'): blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    # Fingerprint - shims & uneeded
    'vendor/bin/gx_fpd': blob_fixup()
        .remove_needed('libunwind.so')
        .remove_needed('libbacktrace.so')
        .add_needed('libshims_gxfpd.so')
        .add_needed('fakelogprint.so'),
    'vendor/lib64/libfpservice.so': blob_fixup()
        .add_needed('libbinder_shim.so'),
    ('vendor/lib64/hw/fingerprint.goodix.so', 'vendor/lib64/gxfingerprint.default.so'): blob_fixup()
        .add_needed('fakelogprint.so'),
    # Fingerprint - liblog dep.
    ('vendor/lib64/libfp_client.so', 'libfpservice.so'): blob_fixup()
        .add_needed('liblog.so'),
    # Fingerprint - libstdc++.so' -> 'libstdc++_vendor.so
    ('vendor/lib64/libfp_client.so', 'vendor/lib64/libfpservice.so', 'vendor/lib64/libfpnav.so', 'vendor/lib64/hw/fingerprint.goodix.so', 'vendor/lib64/gxfingerprint.default.so'): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    # Fingerprint - so name fixups
    ('vendor/lib64/hw/fingerprint.goodix.so', 'vendor/lib64/hw/gxfingerprint.default.so'):blob_fixup()
        .fix_soname(),
    # Thermal
    'vendor/lib64/libthermalfeature.so': blob_fixup()
        .binary_regex_replace(b'system/etc/', b'vendor/etc/'),
}  # fmt: skip

# Define the module
module = ExtractUtilsModule(
    'c330ae',
    'rakuten',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
