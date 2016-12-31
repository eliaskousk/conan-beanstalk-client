from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake

class BeanstalkClientConan(ConanFile):
    name = "beanstalk-client"
    version = "1.3.0"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "gtest": [True, False]}
    default_options = "shared=True", "gtest=False"
    url="http://github.com/eliaskousk/conan-beanstalk-client"
    license="https://opensource.org/licenses/MIT"
    exports= "CMakeLists.txt", "change_dylib_names.sh"
    zip_name = "v%s.tar.gz" % version
    unzipped_name = "beanstalk-client-%s" % version

    def config(self):
        if self.options.gtest == True:
            self.requires.add("gtest/1.8.0@eliaskousk/stable", private=False)

    def source(self):
        url = "https://github.com/deepfryed/beanstalk-client/archive/%s" % self.zip_name
        download(url, self.zip_name)
        unzip(self.zip_name)
        os.unlink(self.zip_name)

        # Or clone the repo and possibly checkout a branch
        #
        # self.run("git clone https://github.com/deepfryed/beanstalk-client.git beanstalk-client-%s" % self.version)
        # self.run("cd beanstalk-client-%s && git checkout v1.3.0" % self.version)

    def build(self):
        self.run("cd %s && make libbeanstalk.so" % (self.unzipped_name))


    def package(self):

        if self.settings.os == "Macos" and self.options.shared:
            self.run("bash ./change_dylib_names.sh")

        # Copying headers
        self.copy(pattern="*.h", dst="include", src=".", keep_path=False)
        self.copy(pattern="*.hpp", dst="include", src=".", keep_path=False)


        libdir = "."
        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=libdir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['beanstalk']
