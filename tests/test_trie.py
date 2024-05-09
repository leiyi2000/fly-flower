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


def main():
    # 测试空初始化
    trie = ZipTrie()
    batch = 1000000000
    iter = gen_paragraph()
    while batch > 0:
        # 随机长度
        paragraph = next(iter)
        trie.add(paragraph)
        ok = trie.exist(paragraph)
        assert ok
        batch -= 1


if __name__ == "__main__":
    main()
