# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import javalang.ast
import javalang.parse
import javalang.tree


class ManyPrimaryCtors(object):
    def value(self, filename: str):
        tree = self.__file_to_ast(filename)

        return self.__traverse_node(tree)

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """

        with open(filename) as file:
            return javalang.parse.parse(file.read())

    def __traverse_node(self, tree: javalang.ast.Node):
        lines = list()

        for _, class_declaration in tree.filter(javalang.tree.ClassDeclaration):
            primary_ctors = list(filter(_is_primary, class_declaration.constructors))

            if len(primary_ctors) > 1:
                lines.extend(ctor.position.line for ctor in primary_ctors)

        return lines


def _is_primary(constructor: javalang.tree.ConstructorDeclaration):
    for _, assignment in constructor.filter(javalang.tree.Assignment):
        if _is_instance_variable_assignment(assignment):
            return True

    return False


def _is_instance_variable_assignment(assignment: javalang.tree.Assignment):
    return isinstance(assignment.expressionl, javalang.tree.This)
