# Paramal
[中文] | [[EN]](README.md)  

将 Alpha 通道转换为法线贴图的命令行工具。

## 功能

- 将 Alpha 通道作为高度信息转换为法线贴图
- 支持 OpenGL 和 DirectX 法线贴图模式
- 可调节法线强度参数
- 支持 `simple`、`sobel`、`scharr` 三种梯度算子
- 可选的叠加混合模式与原图混合
- 支持图像缩放以获得更高分辨率输出
- 自动创建输出目录

## 使用方法

```bash
Paramal <输入路径> <输出路径> [选项]
```

### 选项

- `-s, --strength`: 法线强度（默认: 5.0）
- `-m, --mode`: 法线模式 - `opengl` 或 `dx`（默认: opengl）
- `-o, --operator`: 梯度算子 - `simple`、`sobel` 或 `scharr`（默认: scharr）
- `--mix`: 使用叠加模式将原图与法线贴图混合
- `--scale`: 缩放倍数（默认: 1，例如 8 表示 16x16 -> 128x128）

### 示例

```bash
# 基础转换
Paramal input.png output.png

# 自定义强度并使用 DirectX 模式
Paramal input.png output.png -s 3.0 -m dx

# 使用最原始的上下左右采样方式
Paramal input.png output.png -o simple

# 使用 Scharr 算子
Paramal input.png output.png -o scharr

# 与原图混合并放大
Paramal input.png output.png --mix --scale 4
```

## 依赖

```bash
pip install Pillow numpy
```

## 构建

```bash
pip install Pillow numpy PyInstaller
python -m PyInstaller --onefile --name Paramal --icon logo.ico Paramal.py README.md README_CN.md
```
