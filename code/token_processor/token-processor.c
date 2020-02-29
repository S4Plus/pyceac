#include <stdio.h>
#include <stdbool.h>
#include <fcntl.h>
#include <clang-c/Index.h>

bool printIdentifier(CXTranslationUnit tu) {
    CXCursor cursor = clang_getTranslationUnitCursor(tu);
    CXSourceRange range = clang_getCursorExtent(cursor);
    CXToken *tokens = 0;
    unsigned int nTokens = 0;
    clang_tokenize(tu, range, &tokens, &nTokens);
    for (unsigned int i = 0; i < nTokens - 1; i++) { // the last token cannot be a function name
        if (clang_getTokenKind(tokens[i]) == CXToken_Identifier) {
            if (clang_getTokenKind(tokens[i + 1]) == CXToken_Punctuation && 
                strcmp(clang_getCString(clang_getTokenSpelling(tu, tokens[i + 1])), "(") == 0) {
                    const char *tokenSpelling = clang_getCString(clang_getTokenSpelling(tu, tokens[i]));
                    printf("%s\n", tokenSpelling);
                }
        }
    }
    return true;
}

int main(int argc, char *argv[]) {
    int result = open(argv[1], O_RDONLY);
    if (result == -1) {
        printf("Can't open the file: %s.\n", argv[1]);
        return -1;
    }

    CXIndex Index = clang_createIndex(0,0);
    CXTranslationUnit TU = clang_parseTranslationUnit(Index, 0, argv, argc,
                                                      0, 0,
                                                      CXTranslationUnit_None);

    printIdentifier(TU);

    clang_disposeTranslationUnit(TU);
    clang_disposeIndex(Index);
    return 0;
}
