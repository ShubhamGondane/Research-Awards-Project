import json
import csv

def is_dict(item, ans=[]):
    tree = []
    for k,v in item.items():
        if isinstance(v,dict):
            ans.append(str(k))
            tree.extend(is_dict(v, ans))
            ans=[]
        else:
            if ans:
                ans.append(str(k))
                key = ','.join(ans).replace(',','.')
                tree.extend([(key, str(v))])
                ans.remove(str(k))
            else:
                tree.extend([(str(k),str(v))])
    return tree

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except (ValueError,TypeError) as e:
        return False
    return True

def get_tree(item):
    tree = []
    if isinstance(item, dict):
        tree.extend(is_dict(item, ans=[]))
        return tree
    elif isinstance(item, list):
        tree = []
        for i in item:
            if is_json(i) == True:
                i = json.loads(i)
            tree.append(get_tree(i))
        return tree
    elif isinstance(item, str):
        if is_json(item) == True:
            item = json.loads(item)
            tree.extend(is_dict(item, ans=[]))
            return tree
    else:
        tree.extend([(key, item)])
    return tree

def render_csv(header, data, out_path):
    input = []
    with open(out_path, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=header)
        dict_writer.writeheader()
        if not isinstance(data[0],list):
            input.append(dict(data))
        else:
            for i in data:
                input.append(dict(i))
        dict_writer.writerows(input)
    return

def main(obj, out_path):
    tree = get_tree(obj)
    if isinstance(obj, list):
        header = [i[0] for i in tree[0]]
    else:
        header =[i[0] for i in tree]
    return render_csv(header, tree, out_path)
