def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result


def unique_elements(list1, list2):
    result = set(list1 + list2)
    return list(result)


class Node(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class TermNode(Node):
    def __init__(self, term, search_function):
        Node.__init__(self, term)
        self.term = term
        self.search_function = search_function
        self.result = []

    def search(self):
        """
        Calls the external search function that performs a search for the term of the node
        in a data source. The results from the search are added to the nodes result set.
        """
        result = self.search_function(self.term)

        if result is not None and len(result) > 0:
            self.result += result


class OperatorNode(Node):
    def __init__(self, operator):
        Node.__init__(self, operator)
        self.operator = operator
        self.result = []

    def evaluate(self, left, right):
        """
        Excludes results from NOT operator nodes.

        Args:
            left: the left child of the current node.
            right: the right child of the current node.
        """
        excludes = []

        if isinstance(left, NotOperatorNode):
            excludes += left.result
        if isinstance(right, NotOperatorNode):
            excludes += right.result

        for exclude in excludes:
            self.result.remove(exclude)


class AndOperatorNode(OperatorNode):
    def __init__(self):
        OperatorNode.__init__(self, "AND")
        self.operator = "AND"

    def evaluate(self, left, right):
        """
        Creates an intersection from the results of its left and right child. The result includes
        all items that are present in the left AND right result sets.

        Args:
            left: the left child of the current node.
            right: the right child of the current node.
        """
        if left is not None and right is not None:
            self.result += common_elements(left.result, right.result)

            OperatorNode.evaluate(self, left, right)


class OrOperatorNode(OperatorNode):
    def __init__(self):
        OperatorNode.__init__(self, "OR")
        self.operator = "OR"

    def evaluate(self, left, right):
        """
        Creates a union from the results of its left and right child. The result includes
        all but unique items.

        Args:
            left: the left child of the current node.
            right: the right child of the current node.
        """
        if left is not None and right is not None:
            self.result += unique_elements(left.result, right.result)

            OperatorNode.evaluate(self, left, right)


class NotOperatorNode(OperatorNode):
    def __init__(self):
        OperatorNode.__init__(self, "NOT")
        self.operator = "NOT"

    def evaluate(self, left, _):
        """
        Adds the result of the left child to itself. These results must be excluded from
        the final result.

        Args:
            left: the left child of the current node.
            _: the right child is ignored.
        """
        if left is not None:
            excludes = set(left.result)
            self.result += excludes


class BinaryTree:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.parent = None
        self.value = value

    def get_left_child(self):
        return self.left

    def get_right_child(self):
        return self.right

    def get_parent(self):
        return self.parent

    def set_node_value(self, value):
        self.value = value

    def get_node_value(self):
        return self.value

    def insert_right(self, new_node):
        """
        Creates a new BinaryTree instance and adds it as the right child of the current node.
        If a right child is already present, then the sub nodes of the existing child node
        will be added to the new tree instance.

        Args:
            new_node: an instance of Node.

        Returns:
            The newly inserted or updated tree node.
        """
        tree = BinaryTree(new_node)
        tree.parent = self

        if self.right is None:
            self.right = tree
        else:
            tree.right = self.right
            self.right = tree

        return self.right

    def insert_left(self, new_node):
        """
        Creates a new BinaryTree instance and adds it as the left child of the current node.
        If a left child is already present, then the sub nodes of the existing child node
        will be added to the new tree instance.

        Args:
            new_node: an instance of Node.

        Returns:
            The newly inserted or updated tree node.
        """
        tree = BinaryTree(new_node)
        tree.parent = self

        if self.left is None:
            self.left = tree
        else:
            tree.left = self.left
            self.left = tree

        return self.left

    def create_node_list(self):
        """
        Creates a list of every tree node from bottom to top.

        Returns:
            An array of tree nodes.
        """
        nodes = []
        queue = [self]

        while queue:
            copy = queue[:]
            queue = []

            for node in copy:
                if node is None:
                    queue.append(None)
                    queue.append(None)
                else:
                    nodes.append(node)
                    queue.append(node.get_left_child())
                    queue.append(node.get_right_child())

            if all((x is None for x in queue)):
                break

        return reversed(nodes)

    def evaluate(self):
        """
        Evaluates every tree node from bottom to top. The search terms in the TermNodes will be searched
        in a data source and the results will be stored temporarily. Then, the results of the TermNodes
        will be joined by the OperatorNodes. AND and OR operators need left and right child nodes. NOT
        operators need only the left child. The last tree node is also the root node and contains the
        final result, that is returned from the function.

        Returns:
            An array of the final results from the root tree node.
        """
        nodes = self.create_node_list()

        for node in nodes:
            if node is None:
                continue

            value = node.get_node_value()
            if isinstance(value, TermNode):
                value.search()
            elif isinstance(value, AndOperatorNode) or isinstance(value, OrOperatorNode):
                value.evaluate(node.get_left_child().get_node_value(), node.get_right_child().get_node_value())
            elif isinstance(value, NotOperatorNode):
                value.evaluate(node.get_left_child().get_node_value(), None)

            if node.parent is None:
                return node.get_node_value().result
