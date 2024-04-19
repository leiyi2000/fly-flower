import sys

sys.path.append("../")
from flyflower.trie import ZipTrie


def main():
    # 测试空初始化
    trie = ZipTrie()
    paragraphs = ["abdabd", "adad", "dad", "adadeeeee", "ad", "dad"]
    for paragraph in paragraphs:
        trie.insert(paragraph)
    for paragraph in paragraphs:
        print(trie.exist(paragraph))
    error_paragraphs = ["xxxx", "dax", "ada", "adade", "adadeeee"]
    for paragraph in error_paragraphs:
        print(trie.exist(paragraph))


if __name__ == "__main__":
    main()
