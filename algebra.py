class BaseNode:
    pass

class NodePattern(BaseNode):
    name_and_label: str
    
    def __init__(self, name_and_label: str):
        self.name_and_label = name_and_label
    
    def __str__(self):
        return f"Node({self.name_and_label})"

class EdgePattern(BaseNode):
    name_and_label: str
    
    def __init__(self, name_and_label: str):
        self.name_and_label = name_and_label
    
    def __str__(self):
        return f"Edge(--[{self.name_and_label}]--)"

class RightDirectedEdge(EdgePattern):
    def __str__(self):
        return f"Edge(--[{self.name_and_label}]-->)"

class LeftDirectedEdge(EdgePattern):
    def __str__(self):
        return f"Edge(<--[{self.name_and_label}]--)"

class TriplePattern(BaseNode):
    left: NodePattern
    edge: EdgePattern
    right: NodePattern
    
    def __init__(self, left: NodePattern, edge: EdgePattern, right: NodePattern):
        self.left = left
        self.edge = edge
        self.right = right
    
    def __str__(self):
        return f"Triple({self.left} {self.edge} {self.right})"

class DummyNode(BaseNode):
    pass

class Variable(BaseNode):
    name: str
    
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self):
        return f"Variable({self.name})"

class LabelExpression(BaseNode):
    label: str
    
    def __init__(self, label: str):
        self.label = label
    
    def __str__(self):
        return f"LabelExpression({self.label})"

class QueryTree:
    triple_pattern_list: list[TriplePattern]
    
    projection: list[str]
    filter_conditions: list[str]

    def __init__(self, triple_pattern_list, projection, filter_conditions):
        self.triple_pattern_list = triple_pattern_list
        self.projection = projection
        self.filter_conditions = filter_conditions
    
    def __str__(self):
        return f"""
PROJECTION: {self.projection}
FILTER CONDITIONS: {self.filter_conditions}
TRIPLE PATTERNS:
{
    "\n".join([str(triple_pattern) for triple_pattern in self.triple_pattern_list])
}
        """
