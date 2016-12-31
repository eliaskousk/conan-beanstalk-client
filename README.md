# conan-beanstalk-client

[Conan.io](https://conan.io) package for Beanstalk Client library

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py
    
## Upload packages to server

    $ conan upload beanstalk-client/1.3.0@eliaskousk/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install beanstalk-client/1.3.0@eliaskousk/stable/
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    beanstalk-client/1.3.0@eliaskousk/stable

    [options]

    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files
*conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that
you need to link with your dependencies.
