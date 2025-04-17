from grammar.GQLListener import GQLListener
from grammar.GQLParser import GQLParser
from collections import deque

class ExtendedGQLListener(GQLListener):
    stack = deque()
  
    def enterGqlProgram(self, ctx: GQLParser.GqlProgramContext):
        pass
    
    def exitFullEdgePointingRight(self, ctx: GQLParser.FullEdgePointingRightContext):
        pass
    
    def enterLabelName(self, ctx: GQLParser.LabelNameContext):
        label = ctx.getText()
        self.stack.append(label)
    
    
    
    