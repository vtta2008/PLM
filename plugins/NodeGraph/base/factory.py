#!/usr/bin/python

from cores.Errors import NodeRegistrationError


class NodeFactory(object):

    __aliases = {}
    __names = {}
    __nodes = {}

    @property
    def names(self):
        return self.__names

    @property
    def aliases(self):
        return self.__aliases

    @property
    def nodes(self):
        return self.__nodes

    def create_node_instance(self, node_type=None, alias=None):

        if alias and self.aliases.get(alias):
            node_type = self.aliases[alias]

        NodeClass = self.__nodes.get(node_type)
        if not NodeClass:
            print('can\'t find node type {}'.format(node_type))
        return NodeClass

    def register_node(self, node, alias=None):
        if node is None:
            return

        name = node.NODE_NAME
        node_type = node.type_

        if self.__nodes.get(node_type):
            raise NodeRegistrationError(
                'id "{}" already registered! '
                'Please specify a new plugin class name or __identifier__.'
                .format(node_type))
        self.__nodes[node_type] = node

        if self.__names.get(name):
            self.__names[name].append(node_type)
        else:
            self.__names[name] = [node_type]

        if alias:
            if self.__aliases.get(alias):
                raise NodeRegistrationError(
                    'Alias: "{}" already registered to "{}"'
                    .format(alias, self.__aliases.get(alias))
                )
            self.__aliases[alias] = node_type
            
    def clear_registered_nodes(self):
        self.__nodes.clear()
        self.__names.clear()
        self.__aliases.clear()
