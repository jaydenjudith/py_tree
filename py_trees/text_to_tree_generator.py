import py_trees
import re
import queue


def sub_task_number(str):
    number = re.findall("\d+\.?\d*", str)
    print(number)
    return number


def parse_text_to_tree(str):
    if str.find("同时") == 0:
        node = py_trees.composites.Parallel(name="parallel", policy=False)
        print("创建一个parallel")
        return node
    if str.find("顺序") == 0:
        node = py_trees.composites.Sequence(name="sequence", memory=False)
        print("创建一个sequence")
        return node
    if str.find("选择") == 0:
        node = py_trees.composites.Selector(name="selector", memory=False)
        print("创建一个选择任务")
        return node
    if str.find("修饰器") == 0:
        node = py_trees.decorators.Decorator(name="decorator")
        print("创建一个修饰器")
        return node
    """ 如果不是控制节点, 则为行为节点(condition或者action), 还有子树idiom"""
    return py_trees.behaviours.Running()


def is_controller_node(t: object) -> bool:
    if isinstance(t, py_trees.composites.Parallel) \
            or isinstance(t, py_trees.composites.Sequence) \
            or isinstance(t, py_trees.composites.Selector) \
            or isinstance(t, py_trees.decorators.Decorator):
        return True
    return False


def text_to_tree(str):
    q = queue.Queue()
    # 1 语句以句号作为一个节点的生成
    result_list = re.split(r"[.]", str)
    # 2 每一次循环产生一个节点, 如果是控制节点则用队列保存一个字典保存, K(控制节点),V(控制节点名, 有多少个子节点)
    for str in result_list:
        node = parse_text_to_tree(str)
        number = sub_task_number(str)
        node_map = {node: number}
        q.put(node_map)

    # 3节点如何进行拼接问题
    # 并在字符串中查找控制节点名称, 数量词, 如果没有表示只有一个
    root = None;
    while not q.empty():
        node, number = q.get().item()
        # 递归
        add_child(q, node, number)
        while number != 0:
            sub_node, sub_number = q.get().item()
            node.add_child(sub_node)
            number -= 1
    # 根据map的K创建这个节点, 并且根据map的V循环次数

    # 3.2 如果是行为节点,
    return "hello world"


def add_child(q, node, number):
    for i in number:
        sub_node, sub_number = q.get().item()
        add_child(q,sub_node,sub_number)
        node.add_child(sub_node)

if __name__ == '__main__':
    str = "同时进行2个任务.1个顺序任务.1个选择任务.顺序任务依次进行action1,action2.选择任务进行action3,action4"
    print(text_to_tree(str))
