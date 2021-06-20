from conans import ConanFile
from conans import tools
import os


class QtConan(ConanFile):

    name = "qt"
    version = "5.12.10"

    description = "Qt GUI toolkit"
    license = "LGPL"

    settings = {
        "os": [ "Linux", "Windows" ],
        "arch": [ "x86_64" ],
        "compiler": [ "gcc", "Visual Studio" ],
        "build_type": None
    }

    options = {
        "enable_qt3d": [True, False],
        "enable_qtactiveqt": [True, False],
        "enable_qtandroidextras": [True, False],
        "enable_qtbase": [True, False],
        "enable_qtcanvas3d": [True, False],
        "enable_qtconnectivity": [True, False],
        "enable_qtdeclarative": [True, False],
        "enable_qtdoc": [True, False],
        "enable_qtgraphicaleffects": [True, False],
        "enable_qtimageformats": [True, False],
        "enable_qtlocation": [True, False],
        "enable_qtmacextras": [True, False],
        "enable_qtmultimedia": [True, False],
        "enable_qtquickcontrols": [True, False],
        "enable_qtquickcontrols2": [True, False],
        "enable_qtscript": [True, False],
        "enable_qtsensors": [True, False],
        "enable_qtserialbus": [True, False],
        "enable_qtserialport": [True, False],
        "enable_qtsvg": [True, False],
        "enable_qttools": [True, False],
        "enable_qttranslations": [True, False],
        "enable_qtwayland": [True, False],
        "enable_qtwebchannel": [True, False],
        "enable_qtwebengine": [True, False],
        "enable_qtwebsockets": [True, False],
        "enable_qtwebview": [True, False],
        "enable_qtwinextras": [True, False],
        "enable_qtx11extras": [True, False],
        "enable_qtxmlpatterns": [True, False]
    }

    default_options = "=False\n".join(options.keys()) + "=False"

    default_options_args = {
        "enable_qt3d": "-skip qt3d",
        "enable_qtactiveqt": "-skip qtactiveqt",
        "enable_qtandroidextras": "-skip qtandroidextras",
        "enable_qtbase": "-skip qtbase",
        "enable_qtcanvas3d": "-skip qtcanvas3d",
        "enable_qtconnectivity": "-skip qtconnectivity",
        "enable_qtdeclarative": "-skip qtdeclarative",
        "enable_qtdoc": "-skip qtdoc",
        "enable_qtgraphicaleffects": "-skip qtgraphicaleffects",
        "enable_qtimageformats": "-skip qtimageformats",
        "enable_qtlocation": "-skip qtlocation",
        "enable_qtmacextras": "-skip qtmacextras",
        "enable_qtmultimedia": "-skip qtmultimedia",
        "enable_qtquickcontrols": "-skip qtquickcontrols",
        "enable_qtquickcontrols2": "-skip qtquickcontrols2",
        "enable_qtscript": "-skip qtscript",
        "enable_qtsensors": "-skip qtsensors",
        "enable_qtserialbus": "-skip qtserialbus",
        "enable_qtserialport": "-skip qtserialport",
        "enable_qtsvg": "-skip qtsvg",
        "enable_qttools": "-skip qttools",
        "enable_qttranslations": "-skip qttranslations",
        "enable_qtwayland": "-skip qtwayland",
        "enable_qtwebchannel": "-skip qtwebchannel",
        "enable_qtwebengine": "-skip qtwebengine",
        "enable_qtwebsockets": "-skip qtwebsockets",
        "enable_qtwebview": "-skip qtwebview",
        "enable_qtwinextras": "-skip qtwinextras",
        "enable_qtx11extras": "-skip qtx11extras",
        "enable_qtxmlpatterns": "-skip qtxmlpatterns"
    }

    short_paths = True

    build_dir = "qt-everywhere-src-%s" % version

    def source(self):

        if tools.os_info.is_windows:
            md5 = "a067fcd4576bfc078d8f3a028cdac48c"
            extension = ".zip"
        else:
            md5 = "a781a0e247400e764c0730b8fb54226f"
            extension = ".tar.xz"

        zip_name = "%s%s" % (self.build_dir, extension)
        url = "http://download.qt.io/official_releases/qt/5.12/%s/single/%s" % (self.version, zip_name)

        tools.download(url, zip_name)
        tools.check_md5(zip_name, md5)

        if tools.os_info.is_windows:
            tools.unzip(zip_name)
        else:
            self.run("tar xf %s" % zip_name)

        os.unlink(zip_name)


    # def configure(self):
    #     if self.settings.compiler == "gcc":
            # self.requires("gstreamer/1.14.5@media/stable")
            # self.requires("gst-plugins-base/1.14.5@media/stable")

    def build(self):

        flags = []

        flags.append("-prefix %s" % self.package_folder)

        flags.append("-%s" % str(self.settings.build_type).lower())
        flags.append("-opensource")
        flags.append("-confirm-license")
        flags.append("-shared")
        flags.append("-make tools")
        flags.append("-nomake tests")
        flags.append("-nomake examples")
        flags.append("-opengl desktop")
        flags.append("-qt-freetype")
        flags.append("-qt-harfbuzz")
        flags.append("-qt-pcre")
        flags.append("-qt-libjpeg")
        flags.append("-no-strip")
        flags.append("-no-mtdev")
        flags.append("-no-iconv")
        flags.append("-no-libproxy")
        flags.append("-no-cups")
        flags.append("-no-evdev")
        flags.append("-no-pch")
        flags.append("-no-ltcg")
        flags.append("-no-use-gold-linker")
        flags.append("-no-separate-debug-info")
        flags.append("-no-system-proxies")
        flags.append("-no-warnings-are-errors")
        flags.append("-no-sql-tds")
        flags.append("-no-sql-sqlite")
        flags.append("-no-sql-sqlite2")
        flags.append("-no-sql-odbc")
        flags.append("-no-sql-mysql")
        flags.append("-no-sql-psql")
        flags.append("-no-sql-oci")
        flags.append("-no-sql-ibase")
        flags.append("-no-sql-db2")
        flags.append("-reduce-relocations")

        for key, value in self.default_options_args.items():
            option_value_prop = getattr(self.options, key)
            if not option_value_prop:
                flags.append(value)

        if self.settings.compiler == "gcc":
            self.build_gcc(flags)
        else:
            self.build_msvc(flags)

    def build_gcc(self, flags):

        flags.append("-icu")
        flags.append("-optimized-qmake")
        flags.append("-no-glib")
        flags.append("-eglfs")
        flags.append("-xcb-xlib")
        flags.append("-qt-xcb")
        flags.append("-no-journald")
        flags.append("-no-syslog")
        flags.append("-no-kms")
        flags.append("-no-gbm")
        flags.append("-no-directfb")
        flags.append("-no-linuxfb")
        flags.append("-no-mirclient")
        flags.append("-no-libinput")
        flags.append("-no-tslib")
        flags.append("-no-dbus")
        flags.append("-no-openssl")

        # root_gstreamer = self.deps_cpp_info["gstreamer"].rootpath
        # root_gst_plugins_base = self.deps_cpp_info["gst-plugins-base"].rootpath

        # flags.append("-I %s/include/" % root_gstreamer)
        # flags.append("-I %s/include/gstreamer-1.0" % root_gstreamer)
        # flags.append("-I %s/include/" % root_gst_plugins_base)
        # flags.append("-I %s/include/gstreamer-1.0" % root_gst_plugins_base)
        # flags.append("-gstreamer 1.0")

        flags = " ".join(flags)

        with tools.environment_append({}):
            # "LD_RUN_PATH" : "%s/lib:%s/lib" % (root_gstreamer, root_gst_plugins_base),
            # "PKG_CONFIG_PATH" : "%s/lib/pkgconfig:%s/lib/pkgconfig" % (root_gstreamer, root_gst_plugins_base),
            # "GST_PLUGIN_PATH" : "%s/lib/gstreamer-1.0:%s/lib/gstreamer-1.0" % (root_gstreamer, root_gst_plugins_base)
            self.run("cd %s && ./configure %s" % (self.build_dir, flags))
            self.run("cd %s && make -j%s" % (self.build_dir, tools.cpu_count()))
            self.run("cd %s && make install" % self.build_dir)

    def build_msvc(self, flags):

        flags.append("-mp")
        flags.append("-no-ssl")
        flags.append("-no-angle")

        flags = " ".join(flags)
		
        with tools.environment_append({
            "CL" : "/MP"
            }):
            self.run("cd %s && configure %s" % (self.build_dir, flags))
            self.run("cd %s && jom /J %s || nmake" % (self.build_dir, dict(os.environ)["NUMBER_OF_PROCESSORS"]))
            self.run("cd %s && jom install /J %s || nmake install" % (self.build_dir, dict(os.environ)["NUMBER_OF_PROCESSORS"]))
