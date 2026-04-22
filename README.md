# Paramal

一款简洁高效的图片处理工具，支持 Alpha 转灰度图、Alpha 转法线图等功能。

## 功能特点

- **Alpha 转灰度图**：将图片的 Alpha 通道转换为灰度图
- **Alpha 转法线图**：将图片的 Alpha 通道转换为法线图
- 简单易用的图形界面

## 使用方法

下载 `dist/Paramal.exe` 直接运行即可。

## 开发

```bash
# 安装依赖
pip install pillow pyinstaller

# 运行源码
python alpha_to_grayscale.py

# 打包
pyinstaller Paramal.spec
```

## 技术栈

- Python
- Pillow (图像处理)
- PyInstaller (打包)
