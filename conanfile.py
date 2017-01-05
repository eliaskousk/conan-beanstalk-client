from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans.tools import replace_in_file
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

        # self.output.warn(env.command_line_env)

        # Fix makefile
        text_to_replace = 'CFLAGS       = -Wall -Wno-sign-compare -g -I.'
        replaced_text = '''CFLAGS       += -Wall -Wno-sign-compare -g -I.
'''
        replace_in_file(os.path.join(self.unzipped_name, "makefile"), text_to_replace, replaced_text)

        text_to_replace = 'LDFLAGS      = -L. -lbeanstalk'
        replaced_text = '#LDFLAGS      = -L. -lbeanstalk'
        replace_in_file(os.path.join(self.unzipped_name, "makefile"), text_to_replace, replaced_text)

        text_to_replace = '	$(CPP) $(LINKER) -o $(SHAREDLIB)  beanstalk.o beanstalkcpp.o'
        replaced_text = '	$(CPP) $(LDFLAGS) $(LINKER) -o $(SHAREDLIB)  beanstalk.o beanstalkcpp.o'
        replace_in_file(os.path.join(self.unzipped_name, "makefile"), text_to_replace, replaced_text)

        text_to_replace = '	$(CPP) $(CFLAGS) -fPIC -c -o beanstalkcpp.o beanstalk.cc'
        replaced_text = '	$(CPP) $(CPPFLAGS) -fPIC -c -o beanstalkcpp.o beanstalk.cc'
        replace_in_file(os.path.join(self.unzipped_name, "makefile"), text_to_replace, replaced_text)

        # Fix MSG_NOSIGNAL
        text_to_replace = '#ifndef BS_READ_CHUNK_SIZE'
        replaced_text = '''#ifndef MSG_NOSIGNAL
#define MSG_NOSIGNAL 0x0 //Don't request NOSIGNAL on systems where this is not implemented.
#endif

#ifndef BS_READ_CHUNK_SIZE
'''
        replace_in_file(os.path.join(self.unzipped_name, "beanstalk.c"), text_to_replace, replaced_text)

        if self.options.shared:
            if self.settings.os == "Macos":
                suffix = 'dylib'
            else:
                suffix = 'so'
        else:
            suffix = 'a'

        self.run("cd %s && %s make libbeanstalk.%s" % (self.unzipped_name, env.command_line_env, suffix))

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
