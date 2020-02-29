#include <stdio.h>
#include <stdbool.h>
#include <fcntl.h>
#include <clang-c/Index.h>

bool print_function_prototype(CXCursor cursor)
{
    CXType type = clang_getCursorType(cursor);
    // printf("%s\n", clang_getCString(clang_getCursorSpelling(cursor)));
    // printf("%s\n", clang_getCString(clang_getTypeSpelling(type)));

    enum CXCursorKind kind = clang_getCursorKind(cursor);
    if (kind == CXCursor_FunctionDecl || 
        kind == CXCursor_CXXMethod || 
        kind == CXCursor_FunctionTemplate || 
        kind == CXCursor_Constructor/* ||
        kind == CXCursor_MacroDefinition || 
        kind == CXCursor_MacroExpansion || 
        kind == CXCursor_MacroInstantiation*/) {
            const char *function_name = clang_getCString(clang_getCursorSpelling(cursor));
            const char *return_type = clang_getCString(clang_getTypeSpelling(clang_getResultType(type)));
            printf("%s,%s(", return_type, function_name);

            int num_args = clang_Cursor_getNumArguments(cursor);
            for (int i = 0; i < num_args - 1; ++i) {
                // CXCursor arg_cursor = clang_Cursor_getArgument(cursor, i);
                // const char *arg_name = clang_getCString(clang_getCursorSpelling(arg_cursor));
                // if (strcmp(arg_name, "") == 0) {
                //     arg_name = "no name!";
                // }
                const char *arg_data_type = clang_getCString(clang_getTypeSpelling(clang_getArgType(type, i)));
                printf("%s,", arg_data_type);
            }
            const char *arg_data_type = clang_getCString(clang_getTypeSpelling(clang_getArgType(type, num_args - 1)));
            printf("%s", arg_data_type);

            printf(")\n");
        }
    return true;
}

enum CXChildVisitResult functionVisitor(CXCursor cursor, CXCursor parent, CXClientData clientData)
{
    if (clang_Location_isFromMainFile(clang_getCursorLocation(cursor)) == 0)
        return CXChildVisit_Continue;

    enum CXCursorKind kind = clang_getCursorKind(cursor);
    if ((kind == CXCursor_FunctionDecl || 
         kind == CXCursor_CXXMethod || 
         kind == CXCursor_FunctionTemplate || 
         kind == CXCursor_Constructor || 
         kind == CXCursor_MacroDefinition || 
         kind == CXCursor_MacroExpansion || 
         kind == CXCursor_MacroInstantiation)) {
        print_function_prototype(cursor);
    }

    return CXChildVisit_Continue;
}

int main(int argc, char *argv[])
{
    int result = open(argv[1], O_RDONLY);
    if (result == -1) {
        printf("Can't open the file: %s.\n", argv[1]);
        return -1;
    }

    CXIndex Index = clang_createIndex(0,0);
    CXTranslationUnit TU = clang_parseTranslationUnit(Index, 0, argv, argc,
                                                      0, 0,
                                                      CXTranslationUnit_None);
    CXCursor C = clang_getTranslationUnitCursor(TU);
    
    //print_function_prototype(C);
    clang_visitChildren(C, print_function_prototype, NULL);

    clang_disposeTranslationUnit(TU);
    clang_disposeIndex(Index);
    return 0;
}
