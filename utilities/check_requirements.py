#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# ungoogled-chromium: Modifications to Google Chromium for removing Google integration
# and enhancing privacy, control, and transparency
# Copyright (C) 2016  Eloston
#
# This file is part of ungoogled-chromium.
#
# ungoogled-chromium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ungoogled-chromium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ungoogled-chromium.  If not, see <http://www.gnu.org/licenses/>.

"""Checks build requirements"""

import subprocess
import sys
import shutil
import argparse

def check_common_requirements(python2_command="python", ninja_command="ninja"):
    """Checks common requirements"""
    print("Checking common requirements...")
    print("Checking Python 2 command...")
    result = subprocess.run([python2_command, "-c",
                             ("import sys;print('{}.{}.{}'.format("
                              "sys.version_info.major, sys.version_info.minor, "
                              "sys.version_info.micro))")],
                            stdout=subprocess.PIPE, universal_newlines=True)
    if not result.returncode is 0:
        raise Exception("Python 2 command returned non-zero exit code {}".format(
            result.returncode))
    if not result.stdout.split(".")[0] is "2":
        raise Exception("Unsupported Python version '{!s}'".format(
            result.stdout.strip("\n")))
    print("Using Python version '{!s}'".format(result.stdout.strip("\n")))

    print("Checking ninja command...")
    result = subprocess.run([ninja_command, "--version"],
                            stdout=subprocess.PIPE, universal_newlines=True)
    if not result.returncode is 0:
        raise Exception("Ninja command returned non-zero exit code {}".format(
            result.returncode))
    print("Using ninja version '{!s}'".format(result.stdout.strip("\n")))

def check_gnu_patch(patch_command="patch"):
    """Checks the GNU patch command"""
    print("Checking GNU patch command...")
    result = subprocess.run([patch_command, "--version"], stdout=subprocess.PIPE,
                            universal_newlines=True)
    if not result.returncode is 0:
        raise Exception("patch command returned non-zero exit code {}".format(
            result.returncode))
    print("Using patch command '{!s}'".format(result.stdout.split("\n")[0]))

def check_quilt(quilt_command="quilt"):
    """Checks the quilt command"""
    print("Checking quilt command...")
    result = subprocess.run([quilt_command, "--version"], stdout=subprocess.PIPE,
                            universal_newlines=True)
    if not result.returncode is 0:
        raise Exception("quilt command returned non-zero exit code {}".format(
            result.returncode))
    print("Using quilt command '{!s}'".format(result.stdout.strip("\n")))

def check_windows():
    """Checks Windows-specific requirements"""
    print("Checking bison command...")
    result = subprocess.run(["bison", "--version"], stdout=subprocess.PIPE,
                            universal_newlines=True)
    if not result.returncode is 0:
        raise Exception("bison command returned non-zero exit code {}".format(
            result.returncode))
    result_which = shutil.which("bison")
    if result_which:
        if " " in result_which:
            raise Exception("Spaces are not allowed in the path to bison: {}".format(
                result_which))
    else:
        raise Exception("shutil.which returned unexpected value: {}".format(
            result_which))
    print("Using bison command '{!s}'".format(result.stdout.split("\n")[0]))

    print("Checking gperf command...")
    result = subprocess.run(["gperf", "--version"], stdout=subprocess.PIPE,
                            universal_newlines=True)
    if not result.returncode is 0:
        raise Exception("gperf command returned non-zero exit code {}".format(
            result.returncode))
    result_which = shutil.which("gperf")
    if result_which:
        if " " in result_which:
            raise Exception("Spaces are not allowed in the path to gperf: {}".format(
                result_which))
    else:
        raise Exception("shutil.which returned unexpected value: {}".format(
            result_which))
    print("Using gperf command '{!s}'".format(result.stdout.split("\n")[0]))

def check_macos():
    """Checks macOS-specific requirements"""
    print("Checking macOS SDK version...")
    result = subprocess.run(["xcrun", "--show-sdk-version"], stdout=subprocess.PIPE,
                            universal_newlines=True)
    if not result.returncode is 0:
        raise Exception("xcrun command returned non-zero exit code {}".format(
            result.returncode))
    if not result.stdout.strip() in ["10.10", "10.11", "10.12"]:
        raise Exception("Unsupported macOS SDK version '{!s}'".format(
            result.stdout.strip()))
    print("Using macOS SDK version '{!s}'".format(result.stdout.strip()))

def main(args_list):
    """Entry point"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--common", action="append_const", dest="check_methods",
                        const=check_common_requirements, help="Checks common requirements")
    parser.add_argument("--gnu-patch", action="append_const", dest="check_methods",
                        const=check_gnu_patch, help="Checks for GNU patch")
    parser.add_argument("--quilt", action="append_const", dest="check_methods",
                        const=check_quilt, help="Checks for quilt")
    parser.add_argument("--windows", action="append_const", dest="check_methods",
                        const=check_windows, help="Checks Windows-specific utilities")
    parser.add_argument("--macos", action="append_const", dest="check_methods",
                        const=check_macos, help="Checks macOS-specific utilities")
    args = parser.parse_args(args_list)
    for method in args.check_methods:
        method()

    print("All checks passed")
    return 0

if __name__ == "__main__":
    exit(main(sys.argv[1:]))
