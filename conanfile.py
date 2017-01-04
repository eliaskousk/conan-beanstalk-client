from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake, ConfigureEnvironment

class BeanstalkClientConan(ConanFile):
    name = "beanstalk-client"
    version = "1.3.0"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url="http://github.com/eliaskousk/conan-beanstalk-client"
    license="https://opensource.org/licenses/MIT"
    exports= "CMakeLists.txt", "change_dylib_names.sh"
    zip_name = "v%s.tar.gz" % version
    unzipped_name = "beanstalk-client-%s" % version

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
        env = ConfigureEnvironment(self)
        env_line = env.command_line_env.replace('CFLAGS="', 'CFLAGS="-fPIC ')

        if self.options.shared:
            suffix = 'so'
        else:
            suffix = 'a'

        self.run("cd %s && %s make libbeanstalk.%s" % (self.unzipped_name, env_line, suffix))

    def package(self):
        if self.settings.os == "Macos" and self.options.shared:
            self.run("bash ./change_dylib_names.sh")

        # Copying headers
        self.copy(pattern="*.h", dst="include", src=".", keep_path=False)
        self.copy(pattern="*.hpp", dst="include", src=".", keep_path=False)

        libdir = "."
        if self.options.shared:
            # Copying dynamic libs
            self.copy(pattern="*.so*", dst="lib", src=libdir, keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", src=libdir, keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src=libdir, keep_path=False)
        else:
            # Copying static libs
            self.copy(pattern="*.a", dst="lib", src=libdir, keep_path=False)

        self.copy(pattern="*.lib", dst="lib", src=libdir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['beanstalk']
