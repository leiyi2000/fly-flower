import sys

sys.path.append("../")
import random

from flyflower.trie import ZipTrie


def gen_paragraph():
    while True:
        # 随机长度
        n = random.randint(1, 10)
        # 随机字符串
        yield "".join(random.choices("ab", k=n))


def test_exist():
    # 测试空初始化
    trie = ZipTrie()
    batch = 100000000
    iter = gen_paragraph()
    while batch > 0:
        # 随机长度
        paragraph = next(iter)
        trie.add(paragraph)
        ok = trie.exist(paragraph)
        assert ok
        batch -= 1


def test_remove():
    trie = ZipTrie()
    batch = 1000000
    iter = gen_paragraph()
    paragraphs = []
    while batch > 0:
        # 随机长度
        paragraph = next(iter)
        paragraphs.append(paragraph)
        trie.add(paragraph)
        batch -= 1
    # 随机选择删除
    paragraph_remove = random.choices(paragraphs, k=int(batch * 0.25))
    for paragraph in paragraph_remove:
        trie.remove(paragraph)
        ok = not trie.exist(paragraph)
        assert ok
        trie.add(paragraph)
        ok = trie.exist(paragraph)
        assert ok


if __name__ == "__main__":
    test_remove()
