#!/usr/bin/env python
#-*- coding: ascii -*-

from __future__ import print_function
import os, sys
from blib_util import *

def build_Boost(build_info, compiler_info):
	with_filesystem = True
	with_system = True
	if build_info.is_dev_platform:
		with_program_options = True
	else:
		with_program_options = False
	if (0 == build_info.project_type.find("vs")) or ("gcc" == build_info.compiler_name) or ("mgw" == build_info.compiler_name):
		with_filesystem = False
		with_system = False

	need_install = False
	additional_options = " -DWITH_FILESYSTEM:BOOL="
	if with_filesystem:
		additional_options += "\"ON\""
		need_install = True
	else:
		additional_options += "\"OFF\""
	additional_options += " -DWITH_PROGRAM_OPTIONS:BOOL="
	if with_program_options:
		additional_options += "\"ON\""
		need_install = True
	else:
		additional_options += "\"OFF\""
	additional_options += " -DWITH_SYSTEM:BOOL="
	if with_system:
		additional_options += "\"ON\""
		need_install = True
	else:
		additional_options += "\"OFF\""
	build_a_project("boost", "External/boost", build_info, compiler_info, build_info.is_windows and need_install, additional_options)

def build_Python(build_info, compiler_info):
	build_a_project("Python", "External/Python", build_info, compiler_info, False)

def build_libogg(build_info, compiler_info):
	build_a_project("libogg", "External/libogg", build_info, compiler_info)

def build_libvorbis(build_info, compiler_info):
	build_a_project("libvorbis", "External/libvorbis", build_info, compiler_info)

def build_freetype(build_info, compiler_info):
	build_a_project("freetype", "External/freetype", build_info, compiler_info)

def build_7z(build_info, compiler_info):
	build_a_project("7z", "External/7z", build_info, compiler_info, build_info.is_windows)

def build_UniversalDXSDK(build_info, compiler_info):
	build_a_project("UniversalDXSDK", "External/UniversalDXSDK", build_info, compiler_info)

def build_OpenALSDK(build_info, compiler_info):
	build_a_project("OpenALSDK", "External/OpenALSDK", build_info, compiler_info)

def build_rapidxml(build_info, compiler_info):
	build_a_project("rapidxml", "External/rapidxml", build_info, compiler_info)

def build_wpftoolkit(build_info, compiler_info):
	build_a_project("wpftoolkit", "External/wpftoolkit", build_info, compiler_info)

def build_android_native_app_glue(build_info, compiler_info):
	build_a_project("android_native_app_glue", "External/android_native_app_glue", build_info, compiler_info)

def build_assimp(build_info, compiler_info):
	build_a_project("assimp", "External/assimp", build_info, compiler_info, True)

def build_nanosvg(build_info, compiler_info):
	build_a_project("nanosvg", "External/nanosvg", build_info, compiler_info)

def build_gtest(build_info, compiler_info):
	build_a_project("googletest", "External/googletest", build_info, compiler_info)

def build_FreeImage(build_info, compiler_info):
	build_a_project("FreeImage", "External/FreeImage", build_info, compiler_info, build_info.is_windows)

def build_external_libs(build_info):
	for compiler_info in build_info.compilers:
		build_Boost(build_info, compiler_info)
		build_Python(build_info, compiler_info)
		build_7z(build_info, compiler_info)
		build_rapidxml(build_info, compiler_info)
		build_android_native_app_glue(build_info, compiler_info)
		build_libogg(build_info, compiler_info)
		build_libvorbis(build_info, compiler_info)

		if build_info.is_dev_platform:
			build_freetype(build_info, compiler_info)
			build_assimp(build_info, compiler_info)
			build_nanosvg(build_info, compiler_info)
			build_gtest(build_info, compiler_info)
			build_FreeImage(build_info, compiler_info)

			if (compiler_info.arch != "arm") and (compiler_info.arch != "arm64"):
				build_UniversalDXSDK(build_info, compiler_info)

			if ("win" == build_info.target_platform) and (compiler_info.arch != "arm") and (compiler_info.arch != "arm64"):
				build_OpenALSDK(build_info, compiler_info)

		if build_info.is_windows_desktop and ("x64" == compiler_info.arch) and ("vc" == build_info.compiler_name):
			build_wpftoolkit(build_info, compiler_info)

if __name__ == "__main__":
	cfg = cfg_from_argv(sys.argv)
	bi = build_info(cfg.compiler, cfg.archs, cfg.cfg)

	build_external_libs(bi)
