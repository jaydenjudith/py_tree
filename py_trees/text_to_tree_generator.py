import py_trees
import re

# 用hashmap存储每个节点

def return_node(node):
    if node.find("同时") == 0:
        print("创建一个parallel")
        return "parallel"
    if node.find("顺序") == 0:
        print("创建一个sequence")
        return "sequence"
    if node.find("选择") == 0:
        print("创建一个选择任务")
        return "selector"
    if node.find("修饰器") == 0:
        print("创建一个修饰器")
        return "decorator"
    """ 如果不是控制节点, 则为行为节点(condition或者action), 还有子树idiom"""


def text_to_tree(str):
    # 1 语句以句号作为一个节点的生成
    result_list = re.split(r"[.]", str)
    # 2 每一次循环产生一个节点
    for node in result_list:
        t = return_node(node)
        # 3节点如何进行拼接问题
        # 3.1 如果是控制节点, 暂存这个控制节点, 等到下一个控制节点获得后
        #          并在字符串中查找数量词, 如果没有表示只有一个
        # 3.2 如果是行为节点,

    return "hello world"


if __name__ == '__main__':
    str = "同时进行两个任务.一个顺序任务.一个选择任务.顺序任务依次进行action1,action2.选择任务进行action3,action4"
    print(text_to_tree(str))
