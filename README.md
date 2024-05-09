### 说明

本脚本主要用来计算神经元（swc文件）在不同脑区轴突/树突的总长度，支持单个文件处理以及批处理。同时支持对neuron进行smooth处理。

### 环境

建议使用python 3.8，另外需要两个库，使用下面命令安装：
```commandline
pip install allensdk pynrrd
```
如果需要smooth功能，需要有R环境（建议的R版本4.3.2），以及对应的nat库，安装命令为：
```R
install.packages("nat")
```
建议使用集群zqj00at00swzlab账户，上述环境都已安装好，使用下面命令激活环境即可：
```commandline
# 加载python环境
source activate py38
# 加载R环境
module load R/4.3.2
```

### 参数说明
```python
### parames
# 批处理时swc_path设置为swc文件所在文件夹路径；单个处理时swc_path设为swc文件路径
swc_path = r"D:\_Data\Sun_WenZhi\wuwei\test"
# swc文件里面的坐标的单位，多少um
swc_coord_unit = 10
# allen注释文件路径
annotation_filepath = r"D:\_Data\CCF\mouse_ccf\annotation\ccf_2017\annotation_10.nrrd"
# allen注释文件space，即一个像素的真实物理尺寸（单位，um），因为allen提供的这几个注释文件xyz都是均匀的，所以这里使用一个值来表示
annotation_space = 10
# 执行smooth的R脚本路径
r_script_path = 'smooth.R'
# smooth开关, True or False
smooth = True
# 平滑参数 The standard deviation of the Gaussian smoothing kernel
sigma = 2
```

Allen annotation文件获取地址：
[Annotation](https://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/)

下载的annotation文件里面的数字代表其space值，比如annotation_10.nrrd，代表space为10 um。

### 运行方式
打开python文件，修改参数，开始运行。
```commandline
python main.py
```

### 输出
结果会在swc文件所在路径下保存，如下：
```
19.swc          # 输入文件
19_smooth.swc   # smooth后的文件
19_smooth.json  # 针对smooth的结果计算的长度结果
```

### 结果说明
结果以json文件形式保存，里面保存了该神经元所在的所有脑区（并不是总共所有的脑区）的对应结果信息，比如其中一个脑区的结果如下：
```json
"214": {
    "name": "Red nucleus",
    "structure_id_path": [
      997,
      8,
      343,
      313,
      323,
      214
    ],
    "length": 109.70814150343088
  }
```
"214"代表脑区id

"name"代表该脑区名字

"structure_id_path"代表该脑区层级结构，比如上述这个例子中的含义是：214脑区的父脑区id是323，323脑区的父脑区id是313，以此类推。

"length"代表计算出来的该神经元在该脑区的长度，单位与swc文件里面坐标的单位保持一致。