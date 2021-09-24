from functools import total_ordering
@total_ordering
class TestClass:
    """ Represents an arbitrary thing, for testing the BST. """

    def __init__(self, field1, field2=None):
        """ Initialise an object. """
        self._field1 = field1
        self._field2 = field2

    def __str__(self):
        """ Return a short string representation of this object. """
        outstr = self._field1
        return outstr

    def full_str(self):
        """ Return a full string representation of this object. """
        outstr = self._field1 + ": "
        outstr = outstr + str(self._field2)
        return outstr

    def __eq__(self, other):
        """ Return True if this object has exactly same field1 as other. """
        if (other._field1 == self._field1):
            return True
        return False

    def __ne__(self, other):
        """ Return False if this object has exactly same field1 as other. """
        return not (self._field1 == other._field1)

    def __lt__(self, other):
        """ Return True if this object is ordered before other.

        A thing is less than another if it's field1 is alphabetically before.
        """
        if other._field1 > self._field1:
            return True
        return False


class BSTNode:
    """ An internal node for a Binary Search Tree.  """
    def __init__(self, item):
        """ Initialise a BSTNode on creation, with value==item. """
        self._element = item
        self._leftchild = None
        self._rightchild = None
        self._parent = None


    def __str__(self):
        if self:
            if self._leftchild or self._rightchild:
                ans = '(' + BSTNode.__str__(self._leftchild)
                ans += str(self._element)
                ans += BSTNode.__str__(self._rightchild) + ')'
                return ans
            else:
                return str(self._element)
        else:
            return ''

    def search(self, searchitem):
        """ Return object matching searchitem, or None.
        Args:
            searchitem: an object of any class stored in the BST
        """
        return BSTNode.search_node(self, searchitem)


    def search_node(self, searchitem):
        """ Return the BSTNode (with subtree) containing searchitem, or None.
        Args:
            searchitem: an object of any class stored in the BST
        """
        if self is None:
            return None
        if self._element > searchitem:
            return BSTNode.search_node(self._leftchild, searchitem)
        elif self._element < searchitem:
            return BSTNode.search_node(self._rightchild, searchitem)
        else:
            return self

    def findmaxnode(self):
        """ Return the BSTNode with maximal element at or below here. """
        if self._rightchild is None:
            return self
        return self._rightchild.findmaxnode()

    def add(self, obj):
        add = BSTNode.add
        if self._element != obj:
            if obj < self._element:
                if self._leftchild is None:
                    self._leftchild = BSTNode(obj)
                    self._leftchild._parent = self
                else:
                    add(self._leftchild, obj)
            else:
                if self._rightchild is None:
                    self._rightchild = BSTNode(obj)
                    self._rightchild._parent = self
                else:
                    add(self._rightchild, obj)

    def _stats(self):
        """ Return the basic stats on the tree. """
        return ('size = ' + str(self.size()) + '; height = ' + str(self.height()))

    def height(self):
        """ Return the height of this node.
        Note that with the recursive definition of the tree the height of the
        node is the same as the depth of the tree rooted at this node.
        """
        height = BSTNode.height
        if self is None:
            return 0
        elif self._leftchild is None and self._rightchild is None:
            return 0
        else:
            return 1 + max(height(self._leftchild), height(self._rightchild))

    def size(self):
        """ Return the size of this subtree.
        The size is the number of nodes (or elements) in the tree,
        including this node. """
        size = BSTNode.size
        count = 0
        if self:
            count += 1
            if self._leftchild:
                count += size(self._leftchild)
            if self._rightchild:
                count += size(self._rightchild)
        return count

    def leaf(self):
        """ Return True if this node has no children. """
        if self._leftchild is None and self._rightchild is None:
            return True
        return False

    def semileaf(self):
        """ Return True if this node has exactly one child. """
        if self._leftchild or self._rightchild:
            return True
        return False

    def full(self):
        """ Return true if this node has two children. """

        if self._leftchild and self._rightchild:
            return True
        return False

    def internal(self):
        """ Return True if this node has at least one child. """
        if self._leftchild or self._leftchild or (self._leftchild and self._rightchild):
            return True
        return False

    def remove(self, searchitem):
        """ Remove and return the object matching searchitem, if there.
        Args:
            searchitem - an object of any class stored in the BST
        Remove the matching object from the tree rooted at this node.
        Maintains the BST properties.
        """

        if BSTNode.search_node(self, searchitem):
            BSTNode.search_node(self, searchitem).remove_node()

    def remove_node(self):
        """ Remove this BSTNode from its tree, and return its element.
            Maintains the BST properties.
            """
        if BSTNode.size(self) < 1:
            return None
        elif BSTNode.full(self):
            node = self._leftchild.findmaxnode()
            if self._parent._leftchild == self:
                self._parent._leftchild = self._leftchild
               # node._rightchild = self._rightchild
                #node._rightchild._parent = self._parent._rightchild#node
                #node._parent = self._parent
            else:
                self._parent._rightchild = self._leftchild
                node._rightchild = self._rightchild
                node._rightchild._parent = self._parent._rightchild
                node._parent = self._parent
            return self._element
        elif BSTNode.leaf(self):
            if self._parent._leftchild == self:
                self._parent._leftchild = None
            else:
                self._parent._rightchild = None
            self._parent = None
            return self._element
        else:
            if self._leftchild is None:
                node = self._rightchild
            else:
                node = self._leftchild
            node.remove_node()
            node._parent = self._parent
            if self._parent:
                if self._parent._leftchild == self:
                    self._parent._leftchild = node
                else:
                    self._parent._rightchild = node
            else:
                self._element = node._element
            self._parent = None
            return node._element


    def _print_structure(self):
        """ (Private) Print a structured representation of tree at this node. """
        if self._isthisapropertree() == False:
            print("ERROR: this is not a proper Binary Search Tree. ++++++++++")
        outstr = str(self._element) + ' (hgt=' + str(self.height()) + ')['
        if self._leftchild is not None:
            outstr = outstr + "left: " + str(self._leftchild._element)
        else:
            outstr = outstr + 'left: *'
        if self._rightchild is not None:
            outstr = outstr + "; right: " + str(self._rightchild._element) + ']'
        else:
            outstr = outstr + '; right: *]'
        if self._parent is not None:
            outstr = outstr + ' -- parent: ' + str(self._parent._element)
        else:
            outstr = outstr + ' -- parent: *'
        print(outstr)
        if self._leftchild is not None:
            self._leftchild._print_structure()
        if self._rightchild is not None:
            self._rightchild._print_structure()

    def _properBST(self):
        """ Return True if this is the root of a proper BST; False otherwise.

        First checks that this is a proper tree (i.e. parent and child
        references all link up properly.

        Then checks that it obeys the BST property.
        """
        if not self._isthisapropertree():
            return False
        return self._BSTproperties()[0]

    def _BSTproperties(self):
        """ Return a tuple describing state of this node as root of a BST.

        Returns:
            (boolean, minvalue, maxvalue):
                boolean is True if it is a BST, and false otherwise
                minvalue is the lowest value in this subtree
                maxvalue is the highest value in this subtree
        """
        minvalue = self._element
        maxvalue = self._element
        if self._leftchild is not None:
            leftstate = self._leftchild._BSTproperties()
            if not leftstate[0] or leftstate[2] > self._element:
                return (False,None,None)
            minvalue = leftstate[1]

        if self._rightchild is not None:
            rightstate = self._rightchild._BSTproperties()
            if not rightstate[0] or rightstate[1] < self._element:
                return (False,None,None)
            maxvalue = rightstate[2]
        return (True, minvalue,maxvalue)

    def _isthisapropertree(self):
        """ Return True if this node is a properly implemented tree. """
        ok = True
        if self._leftchild is not None:
            if self._leftchild._parent != self:
                ok = False
            if self._leftchild._isthisapropertree() == False:
                ok = False
        if self._rightchild is not None:
            if self._rightchild._parent != self:
                ok = False
            if self._rightchild._isthisapropertree() == False:
                ok = False
        if self._parent is not None:
            if (self._parent._leftchild != self and self._parent._rightchild != self):
                ok = False
        return ok

    def _testadd():
        node = BSTNode(TestClass("Memento", "11/10/2000"))
        #node._print_structure()
        #print('> adding Melvin and Howard')
        node.add(TestClass("Melvin and Howard", "19/09/1980"))
        #node._print_structure()
        #print('> adding a second version of Melvin and Howard')
        node.add(TestClass("Melvin and Howard", "21/03/2007"))
        #node._print_structure()
        #print('> adding Mellow Mud')
        node.add(TestClass("Mellow Mud", "21/09/2016"))
        #node._print_structure()
        #print('> adding Melody')
        node.add(TestClass("Melody", "21/03/2007"))
        print('******')
        #node.remove(TestClass("Melvin and Howard", "19/09/1980"))
        #node.remove(TestClass())
        node._print_structure()

        return node

    def _test():
        node = BSTNode(TestClass("B", "b"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "A")
        node.add(TestClass("A", "a"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "A")
        node.remove(TestClass("A"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "C")
        node.add(TestClass("C", "c"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "C")
        node.remove(TestClass("C"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "F")
        node.add(TestClass("F", "f"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "B")
        node.remove(TestClass("B"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "C")
        node.add(TestClass("C", "c"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "D")
        node.add(TestClass("D", "d"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "C")
        node.add(TestClass("C", "c"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "E")
        node.add(TestClass("E", "e"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "B")
        node.remove(TestClass("B"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "D")
        node.remove(TestClass("D"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "C")
        node.remove(TestClass("C"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "E")
        node.remove(TestClass("E"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "L")
        node.add(TestClass("L", "l"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "H")
        node.add(TestClass("H", "h"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "I")
        node.add(TestClass("I", "i"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "G")
        node.add(TestClass("G", "g"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "L")
        node.remove(TestClass("L"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "H")
        node.remove(TestClass("H"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "I")
        node.remove(TestClass("I"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "G")
        node.remove(TestClass("G"))
        print('Ordered:', node)
        node._print_structure()
        print(node)


def main():
    BSTNode._testadd()
    BSTNode._test()

if __name__ == '__main__':
 main()

