from xml.dom.minidom import parse
import xml.dom.minidom
import os

if __name__ == '__main__':
    file_list = os.listdir()
    txtsavepath = ''

    ftrainval = open(txtsavepath + 'trainval.txt', 'w')
    ftest = open(txtsavepath + 'test.txt', 'w')
    ftrain = open(txtsavepath + 'train.txt', 'w')
    fval = open(txtsavepath + 'val.txt', 'w')
    # 使用minidom解析器打开 XML 文档
    for i in file_list:
        if i[-3:] == 'xml':
            DOMTree = xml.dom.minidom.parse(i)
            root = DOMTree.documentElement
            print(root.nodeName)
            print(root.nodeValue)
            print(root.nodeType)
            print(root.ELEMENT_NODE)
			
			# 依据xml文件的树形文件节点访问数据
            objects = root.getElementsByTagName("object")
            filename = root.getElementsByTagName('filename')[0]
			# 在末端的元素节点上访问其后的数据节点获得数据
            filename = filename.firstChild.data
            print(filename)
            for obj in objects:
                print("*****object*****")
                name = obj.getElementsByTagName('name')[0].firstChild.data
                box = obj.getElementsByTagName('bndbox')[0]
                x1 = box.getElementsByTagName('xmin')[0].firstChild.data
                x2 = box.getElementsByTagName('xmax')[0].firstChild.data
                y1 = box.getElementsByTagName('ymin')[0].firstChild.data
                y2 = box.getElementsByTagName('ymax')[0].firstChild.data
                str1 = filename + ' ' + ','.join([y1, x1, y2, x2, name]) + '\n'
                ftest.write(str1)
    ftest.close()
