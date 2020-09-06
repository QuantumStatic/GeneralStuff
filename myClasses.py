from myFunctionsG import execute_this, nearMatching
from statistics import mean
from random import shuffle
from copy import deepcopy

class BinarySearchTree:
    class Node:
        __slots__ = ['parent', 'right', 'left', 'value', 'repititions']
        def __init__(self, parent=None, rightChild=None, leftChild=None, value=int()):
            self.parent, self.right, self.left, self.value, self.repititions = parent, rightChild, leftChild, value, int()

        def __str__(self):
            return str({'value':self.value, 'parent':self.parent.value if self.parent is not None else None, 'right':self.right.value if self.right is not None else None, 'left':self.left.value if self.left is not None else None, 'repititions': self.repititions})
            
        def __call__(self):
            return (self)
        
        def copy(self):
            return deepcopy(self)

    def __init__(self, *args):
        elements = BinarySearchTree.breaker(args)
        index = nearMatching(elements,mean(elements))
        self.root = self.Node(value=elements[index])
        del elements[index]
        shuffle(elements)
        self.addElements(elements)

    def __str__(self):
        returnString = '|< '
        def inordertreewalk(itr):
            nonlocal returnString
            if itr.left is not None:
                inordertreewalk(itr.left)
            returnString += f"{itr.value} "
            if itr.right is not None:
                inordertreewalk(itr.right)
        inordertreewalk(self.root)
        returnString += '>|'
        return returnString

    @staticmethod
    def breaker(toBreak):
        final = list()
        for x in toBreak:
            if isinstance(x,int):
                final.append(x)
            elif isinstance(x, list) or isinstance(x,tuple) or isinstance(x,set):
                final.extend(BinarySearchTree.breaker(x))
            else:
                raise Exception(f"{x} of type {type(x)} isn't supported yet")
        return final

    def addElements(self,*toAdd):
        newElements = BinarySearchTree.breaker(toAdd)
        for num in newElements:
            iterator = self.root
            while True:
                if num == iterator.value:
                    iterator.repititions += 1
                    break
                elif num > iterator.value:
                    if iterator.right is not None:
                        iterator = iterator.right
                    else:
                        iterator.right = self.Node(parent=iterator, value=num)
                        break
                else:
                    if iterator.left is not None:
                        iterator = iterator.left
                    else:
                        iterator.left = self.Node(parent=iterator, value=num)
                        break

    def find(self, value,returnNode=False):
        iterator = self.root
        while iterator is not None:
            if value == iterator.value:
                if returnNode:
                    return iterator()
                return True
            if value > iterator.value:
                iterator = iterator.right 
            else:
                iterator = iterator.left 
        return False

    def iterGenerator(self, Node):
        if Node is None:
            return self.root
        if isinstance(Node, self.Node):
            if self.find(Node.value):
                return Node 
            else:
                raise ValueError(f"{type(Node)} with value {Node.value} doesn't exist in Tree")
        elif isinstance(Node, int):
            if (temp := self.find(Node, returnNode=True)) is not False:
                return temp
            else:
                raise ValueError(f"value {Node} doesn't exist in Tree")
        else:
            raise TypeError(f"object of type {type(Node)} doesn't exist in tree")

    def max(self, tree=None, returnNode=False):
        iterator = self.iterGenerator(tree)
        while True:
            if iterator.right is None:
                if returnNode:
                    return iterator()
                return iterator.value
            iterator = iterator.right

    def min(self, tree=None, returnNode=False):
        iterator = self.iterGenerator(tree)
        while True:
            if iterator.left is None:
                if returnNode:
                    return iterator()
                return iterator.value
            iterator = iterator.left

    def next(self, value, returnNode=False):
        iterator = self.iterGenerator(value)
        if iterator.value == self.max():
            return None
        if iterator.right is not None:
            return self.min(tree=iterator.right, returnNode=returnNode)
        while True:
            if iterator.parent.left == iterator:
                if returnNode:
                    return iterator.parent 
                return iterator.parent.value
            iterator = iterator.parent

    def prev(self, value, returnNode=False):
        iterator = self.iterGenerator(value)
        if iterator.value == self.min():
            return None
        if iterator.left is not None:
            return self.max(tree=iterator.left, returnNode=returnNode)
        while True:
            if iterator.parent.right == iterator:
                if returnNode:
                    return iterator.parent
                return iterator.parent.value

    def transplant(self, depriciatedTree, newTree):
        node = self.iterGenerator(depriciatedTree)
        if not isinstance(newTree, self.Node) and isinstance(newTree, int):
            newTree = self.Node(value=newTree)
        elif newTree is None or isinstance(newTree, self.Node):
            pass
        elif not isinstance(newTree, int):
            raise TypeError(f"{type(newTree)} is not supported yet.")
        if node == self.root:
            self.root = newTree
        elif node.parent.right == node:
            node.parent.right = newTree
        else:
            node.parent.left = newTree
        try:
            newTree.parent = node.parent
        finally:
            return (node)

    def remove(self, toRemove):
        toDelete = self.iterGenerator(toRemove)
        if toDelete.repititions:
            temp = toDelete.copy()
            toDelete.repititions -=1
            return temp
        if toDelete.left is None:
            return self.transplant(toDelete, toDelete.right)
        elif toDelete.right is None:
            return(self.transplant(toDelete, toDelete.left))
        else:
            replacement = self.next(toDelete)
            print(replacement)
            self.transplant(replacement, replacement.right)
            replacement.right, replacement.left = toDelete.right, toDelete.left
            return self.transplant(toDelete, replacement)



