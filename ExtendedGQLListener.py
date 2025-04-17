from grammar.GQLListener import GQLListener
from grammar.GQLParser import GQLParser
from collections import deque
from algebra import BaseNode, NodePattern, EdgePattern, TriplePattern, DummyNode, Variable, LabelExpression, QueryTree

class ExtendedGQLListener(GQLListener):
    stack = deque[BaseNode]()
    
    triple_pattern_list: list[TriplePattern] = []
    
    filter_conditions: list[str] = []
    
    return_statement: str = ""
    
    def enterPathTerm(self, ctx: GQLParser.PathTermContext):
        self.stack.append(DummyNode())
    
    def exitPathTerm(self, ctx: GQLParser.PathTermContext):
        path_pattern_seq: list[BaseNode] = []
        
        while True:
            if len(self.stack) == 0:
                raise Exception("Stack is empty")
            
            top_node = self.stack.pop()
            
            if isinstance(top_node, DummyNode):
                break
            elif isinstance(top_node, NodePattern) or isinstance(top_node, EdgePattern):
                path_pattern_seq.append(top_node)
            else:
                raise Exception(f"undefined node type in path pattern sequence: {type(top_node)}")
        
        if len(path_pattern_seq) % 2 == 0:
            raise Exception("path pattern sequence must have odd number of elements")
        
        path_pattern_seq.reverse()
        
        # node_pattern_seq := path_pattern_seq[0, 2, 4, ...]
        # edge_pattern_seq := path_pattern_seq[1, 3, 5, ...]
        
        node_pattern_seq: list[NodePattern] = []
        edge_pattern_seq: list[EdgePattern] = []
        
        for i in range(len(path_pattern_seq)):
            if i % 2 == 0:
                node_pattern_seq.append(path_pattern_seq[i])
            else:
                edge_pattern_seq.append(path_pattern_seq[i])
        
        if not all(isinstance(node, NodePattern) for node in node_pattern_seq):
            raise Exception("all elements in node_pattern_seq must be of the same type")
        
        if not all(isinstance(edge, EdgePattern) for edge in edge_pattern_seq):
            raise Exception("all elements in edge_pattern_seq must be of the same type")
        
        self.triple_pattern_list = []
        
        for i in range(len(node_pattern_seq) - 1):
            triple_pattern = TriplePattern(node_pattern_seq[i], edge_pattern_seq[i], node_pattern_seq[i + 1])
            self.triple_pattern_list.append(triple_pattern)
    
    def exitNodePattern(self, ctx: GQLParser.NodePatternContext):
        node_pattern = NodePattern(ctx.getText())
        self.stack.append(node_pattern)
    
    def exitEdgePattern(self, ctx: GQLParser.EdgePatternContext):
        edge_pattern = EdgePattern(ctx.getText())
        self.stack.append(edge_pattern)
    
    def exitSearchCondition(self, ctx: GQLParser.SearchConditionContext):
        search_condition = ctx.getText()
        self.filter_conditions.append(search_condition)
    
    def exitReturnStatement(self, ctx: GQLParser.ReturnStatementContext):
        return_statement = ctx.getText()
        self.return_statement = return_statement

    def returnQueryTree(self):
        return QueryTree(self.triple_pattern_list, self.filter_conditions, self.return_statement)
