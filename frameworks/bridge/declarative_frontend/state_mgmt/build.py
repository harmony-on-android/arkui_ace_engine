#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Description
#
# This script is invoked by the build system and does not need to be executed directly by the developer.
# It is called after state_mgmt_npm_install (managed by GN) ensures node_modules are ready.
# It runs npm run build_release to compile TypeScript to distRelease/stateMgmt.js,
# then copies the result to the GN output directory with size validation.

import os
import sys
import time
import shutil
import subprocess


def is_tsc_available(node_modules_path):
    tsc_path = os.path.join(node_modules_path, "typescript", "lib", "tsc.js")
    if os.path.exists(tsc_path):
        print(f"StateMgmt: tsc found at {tsc_path}")
        return True
    print(f"StateMgmt: tsc not found at {tsc_path}")
    return False


def main(argv):
    if len(argv) < 4:
        print("Usage: python script.py <path_to_project> <path_to_node_modules> <js_output_path> [--release]")
        sys.exit(1)

    # Determine if it's a release build
    is_release = len(argv) > 4 and argv[4] == "--release"
    print(f": is_release set to {is_release}")

    # If not a release build, print an error and exit
    if not is_release:
        print("ERROR: state_mgmt/build.py requires a release build. Exiting...")
        sys.exit(1)

    project_path = os.path.abspath(argv[1])
    node_modules_path = os.path.abspath(argv[2])
    js_output_path = os.path.abspath(argv[3])

    output_file = os.path.join(js_output_path, "stateMgmt.js")

    print(f"StateMgmt: Changing directory to {project_path}. Out dir = {js_output_path}")
    os.chdir(project_path)

    # Verify tsc is available (npm install should have been handled by GN)
    if not is_tsc_available(node_modules_path):
        print(f"Error: tsc not found at {node_modules_path}/typescript/lib/tsc.js")
        print("The npm_install_guard GN action should have handled this.")
        sys.exit(1)

    # Determine the npm script to run. Currently only build_release supported.
    script = "build_release"
    print(f"StateMgmt: Running npm script '{script}'")

    try:
        subprocess.check_call(["npm", "run", script])
    except subprocess.CalledProcessError as e:
        print(f"Error: npm run {script} failed with exit code {e.returncode}.")
        print("Error: State management build failed. See log output for failing .ts files")
        sys.exit(e.returncode)

    source_folder = "distRelease"
    built_file = os.path.join(project_path, source_folder, "stateMgmt.js")

    if not os.path.exists(built_file):
        print(f"Error: Built file not found at {built_file}")
        sys.exit(1)

    # Ensure the output directory exists
    if not os.path.exists(js_output_path):
        os.makedirs(js_output_path)

    print(f"StateMgmt: Copying {built_file} to {output_file}")

    try:
        shutil.copy(built_file, output_file)
        # Validate: output must be at least 100 KB (empty/stale file is ~3 bytes)
        output_size = os.path.getsize(output_file)
        if output_size < 100000:
            print(f"Error: stateMgmt.js is too small ({output_size} bytes). Build may have failed silently.")
            sys.exit(1)
        print(f"StateMgmt: File successfully copied to {output_file} ({output_size} bytes)")
    except Exception as e:
        print(f"Error: Failed to copy file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"StateMgmt: build time: {elapsed_time:.2f} seconds")
