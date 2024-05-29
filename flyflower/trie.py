from typing import Dict, Tuple, List


SYMBOL = [",", "，", ".", "。"]


class ZipTrie:
    """压缩字典树"""

    def __init__(
        self,
        children: Dict[str, "ZipTrie"] | None = None,
        end: bool = False,
    ):
        self.children: Dict[str, ZipTrie] | None = children
        self.end = end

    def add(self, paragraph: str):
        """添加子节点.

        Args:
            paragraph (str): 节点.
        """
        paragraph = self._filter(paragraph)
        node, match_length = self._find(paragraph)
        if match_length == len(paragraph):
            node.end = True
            return
        # 剩余添加段落
        paragraph = paragraph[match_length:]
        if node.children is None:
            node.children = {}
        prefix_length = 0
        for key in node.children:
            # 查找公共前缀
            while prefix_length < len(paragraph) and prefix_length < len(key):
                if paragraph[prefix_length] == key[prefix_length]:
                    prefix_length += 1
                else:
                    break
            if prefix_length > 0:
                # 公共前缀长度大于0，则分裂
                prefix_node = node._fission(key, prefix_length)
                # 处理剩余添加段落
                if prefix_length < len(paragraph):
                    prefix_node.children[paragraph[prefix_length:]] = ZipTrie(end=True)
                else:
                    # 公共前缀长度等于paragraph, 直接标记end
                    node.children[paragraph].end = True
                break
        # 没有公共前缀
        if prefix_length == 0:
            node.children[paragraph] = ZipTrie(end=True)

    def remove(self, paragraph: str):
        """移除子节点.

        Args:
            node (paragraph): 节点.
        """
        paragraph = self._filter(paragraph)
        prefix = ""
        node = self
        # [(父节点, 子节点, 前缀), ...]
        node_stack: List[Tuple[ZipTrie, ZipTrie, str]] = []
        match_length = 0
        for char in paragraph:
            prefix += char
            if node.children and prefix in node.children:
                node_stack.append((node, node.children[prefix], prefix))
                node = node.children[prefix]
                match_length += len(prefix)
                prefix = ""
        # 判断是否为最后一个节点
        if match_length != len(paragraph) or not node.end:
            return
        while node_stack:
            node_parent, node, prefix = node_stack.pop()
            if node.children is None or len(node.children) == 0:
                # 节点没有子节点，则删除当前节点
                node_parent.children.pop(prefix)
            elif len(node.children) == 1:
                # 合并node_child到node_parent, 删除node
                prefix_child, node_child = node.children.popitem()
                # 父亲删除
                node_parent.children.pop(prefix)
                node_parent.children[prefix + prefix_child] = node_child
                break
            elif len(node.children) > 1:
                # 节点存在多个子节点，则删除当前节点
                node.end = False
                break

    def _fission(self, paragraph: str, length: int) -> "ZipTrie":
        """节点裂解.

        Args:
            paragraph (str): 段落.
            length (int): 分裂段落长度.

        Returns:
            ZipTrie: 分裂后的前缀节点.
        """
        if len(paragraph) == length:
            self.children[paragraph].end = True
            prefix_node = self.children[paragraph]
        else:
            suffix_node = self.children.pop(paragraph)
            prefix = paragraph[:length]
            suffix = paragraph[length:]
            prefix_node = self.children[prefix] = ZipTrie(
                children={suffix: suffix_node}, end=False
            )
        return prefix_node

    def _find(self, paragraph: str) -> Tuple["ZipTrie", int]:
        """查询段落是否存在.

        Args:
            paragraph (str): 段落.

        Returns:
            Tuple[ZipTrie, int]: 节点和匹配长度.
        """
        prefix = ""
        node = self
        match_length = 0
        for char in paragraph:
            prefix += char
            if node.children and prefix in node.children:
                node = node.children[prefix]
                match_length += len(prefix)
                prefix = ""
        return node, match_length

    def exist(self, paragraph: str) -> bool:
        """判断段落是否存在.

        Args:
            paragraph (str): 段落.

        Returns:
            bool: True 存在 or False 不存在.
        """
        paragraph = self._filter(paragraph)
        node, match_length = self._find(paragraph)
        return node.end and match_length == len(paragraph)

    def _filter(self, paragraph: str) -> str:
        """过滤段落.

        Args:
            paragraph (str): 段落.
        Returns:
            str: 过滤后的段落.
        """
        new_paragraph = ""
        for char in paragraph:
            if char not in SYMBOL:
                new_paragraph += char
        return new_paragraph


ztrie = ZipTrie()
