cmake_minimum_required(VERSION 3.20)
project(E2FSPROGS LANGUAGES C)

# CLion toolchain: C:/msys64/mingw64/bin/gcc.exe (MinGW-w64)
add_executable(native_probe native_probe.c)
if(MINGW)
  target_link_options(native_probe PRIVATE -static -static-libgcc)
endif()

# Original upstream e2fsprogs requires Win32 porting work.
add_custom_target(build_e2fsprogs
    COMMAND "C:/msys64/usr/bin/bash.exe" "${CMAKE_CURRENT_SOURCE_DIR}/build.sh"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    COMMENT "Build upstream e2fsprogs with MinGW-w64; porting required"
    VERBATIM
)
