#! python
# @Time    : 2024/4/24 16:34
# @Author  : azzhu 
# @FileName: main.py
# @Software: PyCharm
from pathlib import Path
import json

import allensdk.core.swc as swc
from allensdk.core.reference_space_cache import ReferenceSpaceCache
import nrrd

### parames
# swc文件路径
swc_filepath = r"D:\_Data\sunwenzhi_lab\wuwei\19.swc"
# swc文件里面的坐标的单位，多少um
swc_coord_unit = 10
# allen注释文件路径
annotation_filepath = r"D:\_Data\CCF\mouse_ccf\annotation\ccf_2017\annotation_10.nrrd"
# allen注释文件space，即一个像素的真实物理尺寸（单位，um），因为allen提供的这几个注释文件xyz都是均匀的，所以这里使用一个值来表示
annotation_space = 10
# 输出json文件的路径
output_path = r"D:\_Data\sunwenzhi_lab\wuwei\19_out.json"

if __name__ == '__main__':
    # load swc file
    morphology = swc.read_swc(swc_filepath)
    compartment_list = morphology.compartment_list

    # laod allen structure tree
    rspc = ReferenceSpaceCache(
        resolution=10,
        reference_space_key='annotation/ccf_2017',
        manifest='manifest.json')
    tree = rspc.get_structure_tree()
    name_map = tree.get_name_map()

    # 把swc坐标空间转到annotation像素坐标空间
    scale = annotation_space / swc_coord_unit
    if scale != 1:
        for c in compartment_list:
            c['x'] *= scale
            c['y'] *= scale
            c['z'] *= scale
            c['radius'] *= scale

    # load annotation
    # ann, header = nrrd.read(annotation_filepath, index_order='C')
    ann, header = nrrd.read(annotation_filepath, index_order='F')
    ann_z, ann_y, ann_x = ann.shape

    # lb = set(ann.reshape([-1]))
    # print(lb)
    # print(len(lb))
    # exit()

    outlier = 0
    # 计算跟父节点的距离，判断属于哪个annotation，保存结果
    res = {}  # ann_id: [node,]
    for node in compartment_list:
        x, y, z = node['x'], node['y'], node['z']

        # dist_to_parent
        if node['parent'] < 0:  # 根节点
            node['dist_to_parent'] = 0
        else:
            parent_node = compartment_list[node['parent']]
            x_, y_, z_ = parent_node['x'], parent_node['y'], parent_node['z']
            dist_to_parent = ((x - x_) ** 2 +
                              (y - y_) ** 2 +
                              (z - z_) ** 2) ** 0.5
            node['dist_to_parent'] = dist_to_parent

        # get annotation
        if 0 <= x < ann_x and \
                0 <= y < ann_y and \
                0 <= z < ann_z:
            node['annotation'] = int(ann[
                                         int(round(z)),
                                         int(round(y)),
                                         int(round(x)),
                                     ])
        else:
            node['annotation'] = 0

        if node['annotation'] == 0:
            outlier += 1

        if node['annotation'] in res:
            res[node['annotation']].append(node)
        else:
            res[node['annotation']] = [node]

    #  计算距离和
    dists = {}
    for r, v in res.items():
        dists[r] = {
            'name': name_map[r],
            'structure_id_path': tree.get_structures_by_id([r])[0]['structure_id_path'],
            'length': sum([_['dist_to_parent'] for _ in v]) / scale  # 使用原始单位
        }

    # print outlier
    # print(f'{outlier}/{len(compartment_list)}')

    # save
    with open(output_path, 'w') as f:
        json.dump(dists, f, indent=2)
