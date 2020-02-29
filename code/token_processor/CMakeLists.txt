CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
PROJECT(token-processor)

ADD_EXECUTABLE(token-processor token-processor.c)
INCLUDE_DIRECTORIES(./clang-c/)

#Need to do more about find library#
FIND_LIBRARY(LIBCLANG_PATH clang HINTS /usr/local/lib/)

TARGET_LINK_LIBRARIES(token-processor ${LIBCLANG_PATH})
