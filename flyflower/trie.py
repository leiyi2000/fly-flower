from typing import Dict, Tuple


class TrieNode:
    """节点"""

    def __init__(
        self,
        value: str = "",
        children: Dict[str, "TrieNode"] | None = None,
        end: bool = False,
    ):
        self.children: Dict[str, TrieNode] | None = children
        self.value = value
        self.end = end

    def add(self, node: "TrieNode"):
        if self.children is None:
            self.children = {}
        self.children[node.value] = node


class ZipTrie:
    """压缩字典树"""

    def __init__(self):
        self.root = TrieNode()

    def _find(self, paragraph: str) -> Tuple[TrieNode, int]:
        """查询段落是否存在.

        Args:
            paragraph (str): 段落.

        Returns:
            Tuple[TrieNode, int]: 节点和匹配长度.
        """
        prefix = ""
        node = self.root
        match_count = 0
        for char in paragraph:
            prefix += char
            if node.children and prefix in node.children:
                node = node.children[prefix]
                match_count += len(prefix)
                prefix = ""
        return node, match_count

    def _find_from_children(
        self,
        paragraph: str,
        node: TrieNode
    ) -> Tuple[TrieNode, int]:
        """查询当前节点的所有子节点的公共前缀.

        Args:
            paragraph (str): 段落.
            node (TrieNode): 节点.

        Returns:
            Tuple[TrieNode, int]: 节点和匹配长度.
        """
        if node.children is None:
            return node, -1
        for key in node.children:
            i = 0
            while i < len(paragraph) and i < len(key):
                if paragraph[i] != key[i]:
                    break
                i += 1
            i -= 1
            if i >= 0:
                return node.children[key], i
        return node, -1

    def insert(self, paragraph: str) -> None:
        """
        Inserts a paragraph into the trie.
        """
        # 找出和当前层节点匹配的子节点
        node, match_count = self._find(paragraph)
        if match_count == len(paragraph):
            node.end = True
            return
        # 将剩余不匹配的字符添加到子节点中
        suffix = paragraph[match_count:]
        node, prefix_index = self._find_from_children(suffix, node)
        if prefix_index == -1:
            # 新建节点
            node.add(TrieNode(value=suffix, end=True))
        elif len(suffix) > len(node.value):
            # suffix: ABCC
            # node.value: ABC
            node.add(TrieNode(value=suffix[prefix_index + 1 :], end=True))
        elif len(suffix) < len(node.value):
            # suffix: ABC
            # node.value: ABCD
            node.add(
                TrieNode(
                    value=node.value[prefix_index + 1 :],
                    children=node.children,
                    end=node.end,
                )
            )
            node.value = suffix
            node.end = True
        return

    def exist(self, paragraph: str) -> bool:
        """
        Returns if the paragraph prefixes are similar.
        """
        node, match_count = self._find(paragraph)
        return node.end and match_count == len(paragraph)
