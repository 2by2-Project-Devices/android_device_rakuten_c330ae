/*
 * Copyright (C) 2019,2021 The LineageOS Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#define LOG_TAG "vendor.lineage.touch-service.glovemode"

#include "GloveMode.h"

#include <android-base/file.h>
#include <android-base/logging.h>
#include <android-base/strings.h>

using ::android::base::ReadFileToString;
using ::android::base::Trim;
using ::android::base::WriteStringToFile;

namespace aidl {
namespace vendor {
namespace lineage {
namespace touch {

static constexpr const char kControlPath[] = "/sys/devices/platform/soc/78b7000.i2c/i2c-3/3-0038/fts_glove_mode";

GloveMode::GloveMode() {}

ndk::ScopedAStatus GloveMode::getEnabled(bool* _aidl_return) {
    std::string buf;
    if (!ReadFileToString(kControlPath, &buf, true)) {
        LOG(ERROR) << "Failed to read from " << kControlPath;
        *_aidl_return = false;
        return ndk::ScopedAStatus::ok();
    }
    *_aidl_return = (std::stoi(Trim(buf)) == 1);
    return ndk::ScopedAStatus::ok();
}

ndk::ScopedAStatus GloveMode::setEnabled(bool enabled) {
    if (!WriteStringToFile(enabled ? "1" : "0", kControlPath, true)) {
        LOG(ERROR) << "Failed to write to " << kControlPath;
        return ndk::ScopedAStatus::fromExceptionCode(EX_ILLEGAL_STATE);
    }
    return ndk::ScopedAStatus::ok();
}

}  // namespace touch
}  // namespace lineage
}  // namespace vendor
}  // namespace aidl
