# Report
my github [repository](https://github.com/starrywiki/Terrain-Generation)
## Task1
这个task我主要实现了naive的`PerlinNoise`,最开始不太理解`lattice` `nmap`等的含义入手稍稍困难
```python
#例如nlattice指的是x/z轴方向的晶格数目，总的chunk数目应该是nlattice*nlattice
self.nlattice = lattice_size // nmap
```
后面主要是卡在如何使用minecraft正确生成地形，一开始遇到的问题是没有出现std:test
![alt text](29490b2b628be961eba42f2488a49f0.png){: style="width:500px; height:auto"}
询问masterFHC得知是test里面有不合法的指令，发现是xyz坐标没有设置成整数的原因，通过把gen.py里面的噪声值int后解决问题
然后是无法重新渲染地图，我解决问题主要依靠，先清空地图， 通过手动运行：
```
/gamerule commandModificationBlockLimit 999999999
/fill 0 -64 0 512 255 512 minecraft:air
```
然后退出游戏重启游戏 再运行：
```
/reload
/gamerule commandModificationBlockLimit 999999999
/function std:test
```
此时便可正常渲染
我设置的参数为：
```python
lattice_size = 8 # in perlin.py
nmap = 64 # in perlin.py
noise = perlin.get_perlin(x, z) # in gen.py
height = int(noise * 30.0 + 5) # in gen.py
```

Task1的效果图如下：
![alt text](image-7.png){: style="width:700px; height:auto"}
## Task2
在这个task中我完成了用多层噪声叠加的方法来生成一片更加“层峦叠嶂”的地形，其中比较困难的是调参以及如何正确叠加噪声层
**叠加噪声层：**
  
```python
ls = lattice_size * (2**i)  # 重新设置lattice_size为第i层的2倍
nm = 512 // ls
perlin = PerlinNoise(seed=698 + i, lattice_size=ls, nmap=max(1, nm)) # 调用函数生成新的噪声层
```

然后再通过计算叠加并归一化noise即可：
```python
def get_perlin_octave(x: float, z: float, perlin_array: list) -> float:
    # Generate the 2D perlin noise with octaves
    noise = 0
    amplitude = 1.0  # 影响度
    total_amplitude = 0.0
    for octave in perlin_array:
        noise += amplitude * octave.get_perlin(x, z)
        total_amplitude += amplitude
        amplitude *= 0.5
    noise /= total_amplitude
    return noise
```
在我的gen.py中的参数设置：
```python
PerlinNoiseArray = GeneratePerlinNoiseArray(3, lattice_size=4, nmap=128) # in gen.py
noise = get_perlin_octave(x, z, PerlinNoiseArray) # in gen.py
height = int(noise * 80.0 + 5) # in gen.py
```
未使用spline Method，叠加三层柏林噪声的初步效果图：![alt text](image-8.png){: style="width:700px; height:auto"}
如果设置为`PerlinNoiseArray = GeneratePerlinNoiseArray(3, lattice_size=8, nmap=64)` 效果图则如下：
 ![alt text](image-9.png){: style="width:300px; height:auto"}    ![alt text](image-10.png){: style="width:500px; height:auto"}
然后我们考虑用上spline method，观察其变化
我分别采取了三种不一样的spline_table,分别是plain、mountain和plateau
我定义的spline方法以及预设如下：
```python
def spline(noise: float, spline_table: dict) -> float:
    keys = sorted(spline_table.keys())
    if noise < keys[0]:
        return spline_table[keys[0]]
    if noise > keys[-1]:
        return spline_table[keys[-1]]
    for i in range(len(keys) - 1):
        if keys[i] <= noise <= keys[i + 1]:
            x0, x1 = keys[i], keys[i + 1]
            y0, y1 = spline_table[x0], spline_table[x1]
            alpha = (noise - x0) / (x1 - x0)
            return lerp(y0, y1, alpha)
# 几种spline table预设
spline_table_plain = {
    -1.0: 5,
    -0.5: 15,
    0.0: 25,
    0.5: 35,
    1.0: 45,
}

spline_table_plataeu = {
    -1.0: 120,
    -0.5: 110,
    0.0: 100,
    0.5: 80,
    1.0: 60,
}

spline_table_mountain = {
    -1.0: 10,
    -0.5: 40,
    0.0: 80,
    0.5: 120,
    1.0: 150,
}
```

`spline_table_plain`:
![alt text](image-13.png){: style="width:500px; height:auto"}
`spline_table_plataeu`:
![alt text](image-14.png){: style="width:500px; height:auto"}
`spline_table_mountain`:
![alt text](image-12.png){: style="width:500px; height:auto"}