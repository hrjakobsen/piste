cmake_minimum_required(VERSION 3.21)
project(piste C)

set(CMAKE_C_STANDARD 99)

add_library(piste piste.c)

add_library(piste_std piste_std.c)

add_executable(tester tester.c)

target_link_libraries(tester piste piste_std)

install(TARGETS piste piste_std DESTINATION lib)
install(FILES piste.h piste_std.h DESTINATION include)