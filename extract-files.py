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
    (
        'product/etc/permissions/vendor.qti.hardware.data.connection-V1.0-java.xml',
        'product/etc/permissions/vendor.qti.hardware.data.connection-V1.1-java.xml',
    ): blob_fixup()
        .regex_replace('version="2.0"', 'version="1.0"'),
    'system_ext/lib64/lib-imscamera.so': blob_fixup()
        .add_needed('libshim_imscamera.so'),
    'vendor/etc/seccomp_policy/atfwd@2.0.policy': blob_fixup()
        .add_line_if_missing('gettid: 1'),
    (
        'vendor/lib/libts_detected_face_hal.so',
        'vendor/lib/libts_face_beautify_hal.so',
    ): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/libril-qc-hal-qmi.so': blob_fixup()
        .binary_regex_replace(b'android.hardware.radio.config@1.0.so', b'android.hardware.radio.c_shim@1.0.so')
        .binary_regex_replace(b'android.hardware.radio.config@1.1.so', b'android.hardware.radio.c_shim@1.1.so')
        .binary_regex_replace(b'android.hardware.radio.config@1.2.so', b'android.hardware.radio.c_shim@1.2.so'),
    (
        'vendor/lib64/libwvhidl.so',
        'vendor/lib64/mediadrm/libwvdrmengine.so',
    ): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so')
        .binary_regex_replace(b'libprotobuf-cpp-lite-3.9.1.so', b'libprotobuf-cpp-full-3.9.1.so'),
    (
        'vendor/lib/vendor.tinno.camera.vendorimageeffect@1.0.so',
        'vendor/lib64/vendor.qti.esepowermanager@1.0.so',
        'vendor/lib64/vendor.qti.hardware.qteeconnector@1.0.so',
    ): blob_fixup()
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
    'vendor/lib/libmmqjpeg_codec.so': blob_fixup()
        .binary_regex_replace(
            b'\x04\xf1\xf0\x00\x02\xf0\x36\xfd\x04\xf1\xf4\x00\x02\xf0\x3a\xfd',
            b'\x04\xf1\xf0\x00\x00\xbf\x00\xbf\x04\xf1\xf4\x00\x02\xf0\x3a\xfd'
        )
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
