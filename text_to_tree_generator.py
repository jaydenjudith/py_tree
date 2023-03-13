import py_trees
import re
import jieba

node_number = 0


# 判断控制节点和行为节点
def find_node_type(word):
    parallel_list = ["同时", "并行", "一起"]
    if any(x in word for x in parallel_list):
        return "parallel"
    sequence_list = ["顺序", "依次", "按序"]
    if any(x in word for x in sequence_list):
        return "sequence"
    selector_list = ["任一", "选择"]
    if any(x in word for x in selector_list):
        return "selector"
    condition_list = ["如果", "要是"]
    if any(x in word for x in condition_list):
        return "decorator"
    # 所有的行为节点, 写在一个txt文件中, 读取从而确定机器一共拥有的 基元action
    action_list = ["action1", "action2", "action3", "action4", "action5", "action6"]
    for x in action_list:
        if x in word:
            return x
    return None


# 判断是不是行为节点
def isActionNode(word):
    list = ["parallel", "sequence", "selector", "condition"]
    return not any(x in word for x in list)


# 命名重名问题
def create_node(node_type):
    if "parallel" in node_type:
        return py_trees.composites.Parallel(name="parallel", policy=py_trees.common.ParallelPolicy.Base)
    if "sequence" in node_type:
        return py_trees.composites.Sequence(name="sequence", memory=False)
    if "selector" in node_type:
        return py_trees.composites.Selector(name="selector", memory=False)
    if "action" in node_type:
        return py_trees.behaviours.Running(name="worker")


# 根据一句话创建基元字数的方法, 返回这个树的根节点以及排列的list
def create_sub_tree(seg_list):
    list = []
    root = None
    for word in seg_list:
        print(word + " ")
        node_type = find_node_type(word)
        if node_type is not None:
            if root is not None:
                # 如果是控制节点，添加一个索引位置，如果是行为节点直接添加
                if isActionNode(node_type):
                    action_node = create_node(node_type)
                    root.add_child(action_node)
                else:
                    list.append(node_type)
            else:
                node = create_node(node_type)
                root = node
                list.append(node)
    return root, list


# 倒叙查找list进行子树的链接
def link_tree(sub_tree_root, list):
    if len(list) == 0 or sub_tree_root == None:
        return None
    # 之前有节点,需要进行来链接
    for node in reversed(list):
        for parent_node in reversed(node):
            if type(parent_node) == type('str'):
                if sub_tree_root.name in parent_node:
                    node[0].add_child(sub_tree_root)
                    return

    return



def text_to_tree(task, list):
    # 1 语句以句号作为一个节点的生成, 每一句话都是一个子树基元
    tasks = re.split(r"[.。]", task)
    # 2 每一次循环产生一个基元任务
    for task in tasks:
        seg_list = jieba.cut(task)
        # 3 对任务进行子树构建
        sub_tree_root, sub_tree_list = create_sub_tree(seg_list)
        # 4 判断是否又父节点,有就链接
        link_tree(sub_tree_root, list)
        list.append(sub_tree_list)
    return list


if __name__ == '__main__':
    list = []
    task = "同时进行顺序任务和选择任务."
    list = text_to_tree(task, list)
    task = "顺序任务进行action1,action2和顺序任务."
    list = text_to_tree(task, list)
    task = "选择任务进行action3,action4."
    list = text_to_tree(task, list)
    task = "顺序任务执行action5和action6."
    list = text_to_tree(task, list)
    root = list[0][0]
    py_trees.display.render_dot_tree(root)
