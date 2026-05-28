/*
 * Copyright (C) 2019 The LineageOS Project
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

#define LOG_TAG "vendor.lineage.touch-service.rakuten_c330ae"

#include "GloveMode.h"

#include <android-base/logging.h>
#include <android/binder_manager.h>
#include <android/binder_process.h>

using aidl::vendor::lineage::touch::GloveMode;

int main() {
    ABinderProcess_setThreadPoolMaxThreadCount(0);

    std::shared_ptr<GloveMode> gloveMode = ndk::SharedRefBase::make<GloveMode>();

    const std::string instanceGlove =
            std::string(GloveMode::descriptor) + "/default";

    CHECK_EQ(AServiceManager_addService(gloveMode->asBinder().get(),
                                        instanceGlove.c_str()), STATUS_OK)
        << "Failed to register GloveMode HAL service.";

    LOG(INFO) << "Touch HAL AIDL service is ready.";
    ABinderProcess_joinThreadPool();

    return EXIT_FAILURE;
}
