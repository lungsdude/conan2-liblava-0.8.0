import os
import shutil
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import copy, rmdir
from conan.tools.build import check_min_cppstd
from conan.tools.scm import Git

class LiblavaConan(ConanFile):
    name = "liblava"
    version = "0.8.0"
    license = "MIT"
    author = "Lava Block OÜ (code@liblava.dev)"
    url = "https://github.com/liblava/liblava.git"
    description = "A modern and easy-to-use library for the Vulkan API"
    topics = ("vulkan", "graphics", "rendering")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False],
        "test": [True, False],
        "demo": [True, False]
    }
    default_options = {
        "fPIC": True,
        "test": False,
        "demo": False
    }
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "LICENSE"
    no_copy_source = True

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        check_min_cppstd(self, "20")

    def source(self):
        git = Git(self)
        git.clone(self.url, self.source_folder, args=["-b", self.version])

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON" if self.options.get_safe("fPIC") else "OFF"
        tc.variables["LIBLAVA_TEST"] = "ON" if self.options.get_safe("test") else "OFF"
        tc.variables["LIBLAVA_DEMO"] = "ON" if self.options.get_safe("demo") else "OFF"
        tc.variables["LIBLAVA_TEMPLATE"] = "OFF"
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib/cmake"))
        copy(self, "LICENSE", dst="licenses", src=self.source_folder)

    def package_info(self):
        self.cpp_info.includedirs = [
            "include",
            "include/liblava/ext"
        ]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]

        self.cpp_info.defines += ["SPDLOG_COMPILED_LIB"]

        self.cpp_info.libs = [
            "lava.engine",
            "lava.app",
            "lava.block",
            "lava.frame",
            "lava.asset",
            "lava.resource",
            "lava.base",
            "lava.file",
            "lava.util",
            "lava.core",
            "shaderc_combined",
            "glfw3",
            "physfs" if self.settings.compiler != "msvc" else "physfs-static",
            "spdlog"
        ]

        if self.settings.get_safe("compiler.libcxx") == "libstdc++11":
            self.cpp_info.system_libs += ["stdc++fs"]

        if self.settings.get_safe("compiler") in ["gcc", "clang"]:
            thread_flag = "-pthread"
            self.cpp_info.sharedlinkflags.append(thread_flag)
            self.cpp_info.exelinkflags.append(thread_flag)
            self.cpp_info.system_libs += ["dl"]
