from conans import ConanFile, CMake, tools
import os


class LibJsonRPCCPPConan(ConanFile):
    name = "libjson-rpc-cpp"
    version = "1.1.1"
    description = "C++ framework for json-rpc (json remote procedure call)"
    homepage = "https://github.com/cinemast/libjson-rpc-cpp"
    url = "http://gitlab.khomp.corp/conan/conan-libjson-rpc-cpp"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {"shared": [True, False], "fPIC": [True, False], "with_http_client": [True, False], "with_http_server": [True, False]}
    default_options = {'shared': True, 'fPIC': True, 'with_http_client': False, 'with_http_server': False}
    exports_sources = ["CMakeLists.txt", "cmake.patch"]
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    requires = "jsoncpp/1.9.2"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
        else:
            self.options["jsoncpp"].use_pic = self.options.fPIC

    def requirements(self):
        if self.options.with_http_client:
            self.requires.add("libcurl/7.67.0")
        if self.options.with_http_server:
            self.requires.add("libmicrohttpd/0.9.59@bincrafters/stable")

    def source(self):
        source_url = "https://github.com/cinemast/libjson-rpc-cpp"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["BUILD_STATIC_LIBS"] = not self.options.shared
        cmake.definitions["COMPILE_EXAMPLES"] = False
        cmake.definitions["COMPILE_TESTS"] = False
        cmake.definitions["COMPILE_STUBGEN"] = False
        # TODO (uilian): Hiredis
        cmake.definitions["REDIS_SERVER"] = False
        # TODO (uilian): Hiredis
        cmake.definitions["REDIS_CLIENT"] = False
        cmake.definitions["HTTP_SERVER"] = self.options.with_http_server
        cmake.definitions["HTTP_CLIENT"] = self.options.with_http_client
        cmake.definitions["TCP_SOCKET_SERVER"] = True
        cmake.definitions["TCP_SOCKET_CLIENT"] = True
        cmake.definitions["WITH_COVERAGE"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        tools.patch(base_path=self._source_subfolder, patch_file="cmake.patch")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self._source_subfolder)
        self.copy("*.h", src=os.path.join(self._source_subfolder, "src", "jsonrpccpp"), dst=os.path.join("include", "jsonrpccpp"))
        self.copy("*.h", src=os.path.join(self._build_subfolder, "gen"), dst=os.path.join("include"))
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
