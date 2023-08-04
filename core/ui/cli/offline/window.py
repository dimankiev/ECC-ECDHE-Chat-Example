from rich.console import Group
from rich.layout import Layout
from rich.tree import Tree
from rich.text import Text
from rich import print


class Window:
    __layout: Layout

    __layout_peers: Layout
    __tree_peers: Tree

    __layout_chat: Layout
    __tree_chat: Tree

    def __init__(self):
        self.render([], [])

    def render(self, peers: list[str], messages: list[list[str, bool]]):
        self.__init_tree(peers)
        self.__init_layout_peers()
        self.__init_layout_chat(messages)
        self.__init_layout()
        print(self.__layout)

    def __init_layout(self):
        self.__layout = Layout()
        self.__layout.split_row(
            self.__layout_peers,
            self.__layout_chat
        )

    def __init_layout_chat(self, messages: list[list[str, bool]]):
        self.__layout_chat = Layout(name="Chat")
        message_objects: list[Text] = []
        for message in messages:
            if message[1]:
                message_objects.append(Text(message[0], justify="right"))
            else:
                message_objects.append(Text(message[0], justify="left"))
        messages_group = Group(*message_objects)
        self.__layout_chat.update(messages_group)

    def __init_layout_peers(self):
        self.__layout_peers = Layout(self.__tree_peers, name="Peers")

    def __init_tree(self, peers: list[str]):
        self.__tree_peers = Tree("Peers")
        for peer in peers:
            self.__add_peer(peer)

    def __add_peer(self, peer: str):
        self.__tree_peers.add(peer)
