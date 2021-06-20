set(CONTRIB_DIR ${CMAKE_SOURCE_DIR}/contrib/build/${BUILD_TYPE})

include(${CONTRIB_DIR}/qt/conanbuildinfo.cmake)

set(CMAKE_CXX_FLAGS "\
    -Wall \
    -pthread \
    -fPIC \
    -funsigned-char \
    -rdynamic \
    ")

set(QT5_ROOT ${CONAN_QT_ROOT})

set(CMAKE_PREFIX_PATH ${QT5_ROOT})

find_package(Qt5Core REQUIRED)
find_package(Qt5Gui REQUIRED)
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Quick REQUIRED)
find_package(Qt5Qml REQUIRED)
find_package(Qt5Svg REQUIRED)

set(QT5_CORE_LIB       Qt5::Core)
set(QT5_GUI_LIB        Qt5::Gui)
set(QT5_WIDGETS_LIB    Qt5::Widgets)
set(QT5_QUICK_LIB      Qt5::Quick)
set(QT5_QML_LIB        Qt5::Qml)
set(QT5_SVG_LIB        Qt5::Svg)

if(UNIX)
    find_package(Qt5X11Extras REQUIRED)
    set(QT5_X11_EXTRAS_LIB Qt5::X11Extras)
endif()

find_package(Qt5LinguistTools REQUIRED)
set(QT5_LUPDATE_EXECUTABLE ${Qt5_LUPDATE_EXECUTABLE})

set(QMLLINT_EXECUTABLE ${QT5_ROOT}/bin/qmllint)

conan_basic_setup(NO_OUTPUT_DIRS)

qt5_add_resources(RCC ./ui/qml.qrc)
add_executable(app main.cpp ${RCC})

target_link_libraries( app
    ${QT5_CORE_LIB}
    ${QT5_WIDGETS_LIB}
    ${QT5_QUICK_LIB}
    )
