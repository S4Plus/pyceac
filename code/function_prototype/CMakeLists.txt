CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
PROJECT(function-prototype)

ADD_EXECUTABLE(function-prototype function-prototype.c)
INCLUDE_DIRECTORIES(./clang-c/)
INCLUDE_DIRECTORIES(/usr/local/include/)

#Need to do more about find library#
FIND_LIBRARY(LIBCLANG_PATH clang HINTS /usr/local/lib/)

TARGET_LINK_LIBRARIES(function-prototype ${LIBCLANG_PATH})
