from argparse import ArgumentParser
from grammar.GQLParser import GQLParser
from grammar.GQLLexer import GQLLexer
from ExtendedGQLListener import ExtendedGQLListener
from antlr4 import CommonTokenStream, ParseTreeWalker, InputStream

def main():
    parser = ArgumentParser()
    parser.add_argument("file", type=str, help="path to the gql file")
    args = parser.parse_args()
    
    print(f"file: {args.file}")
    
    with open(args.file, "r") as f:
        text = f.read()
        
    print("query:")
    print(text)
    
    input_stream = InputStream(text)
    lexer = GQLLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = GQLParser(tokens)
    
    parser.removeParseListeners()
    listener = ExtendedGQLListener()
    parser.addParseListener(listener)
    _ = parser.gqlProgram()

    query_tree = listener.returnQueryTree()
    
    print("extraction result:")
    print(query_tree)

if __name__ == "__main__":
    main()
