from typing import Dict, Tuple


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
        node, match_length = self.find(paragraph)
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
                prefix_node = node.fission(key, prefix_length)
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
        # TODO
        pass

    def fission(self, paragraph: str, length: int) -> "ZipTrie":
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

    def find(self, paragraph: str) -> Tuple["ZipTrie", int]:
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
        node, match_length = self.find(paragraph)
        return node.end and match_length == len(paragraph)
