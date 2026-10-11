# 儿童口腔临床资料生成工具包

Pediatric Dentistry Clinical Handouts & Slide Generator

用一套 Python 脚本生成**示意图 + 图解手册（DOCX/PDF）+ 讲解 PPT** 的儿童口腔临床资料，目前包含两个主题：

| 主题 | 图解手册 | 讲解 PPT |
|---|---|---|
| 固定式间隙保持器与改良 Nance 弓矫治器 | `固定式间隙保持器与改良Nance弓_图解手册.pdf` / `.docx` | `固定式间隙保持器与改良Nance弓_讲解PPT.pptx` / `.pdf` |
| 乳牙预成冠修复术 | `乳牙预成冠修复术_图解手册.pdf` / `.docx` | `乳牙预成冠修复术_讲解PPT.pptx` / `.pdf` |

另有早期文字详解版：`固定式间隙保持器与改良Nance弓矫治器_临床规范参考.pdf` / `.docx`

## 项目结构

```
fig_lib.py              绘图库：牙齿 / 弓丝 / 带环 / 腭托 / 前牙冠 等图元，支持合面观牙弓、旋转牙体、斜线阴影
fig_make.py             → figs/           间隙保持器主题的 12 张示意图
fig_make_crown.py       → figs_crown/     乳牙预成冠主题的 10 张示意图

build_space_maintainer.py  早期文字详解版（DOCX）
build_v2.py            → 间隙保持器 · 图解手册（DOCX）
build_v3.py            → 乳牙预成冠 · 图解手册（DOCX）
build_ppt.py           → 间隙保持器 · 讲解 PPT（30 页，含备注）
build_ppt_crown.py     → 乳牙预成冠 · 讲解 PPT（25 页，含备注）

figs/                   间隙保持器示意图（PNG，含拆图）
figs_crown/             乳牙预成冠示意图（PNG，含拆图）
```

## 环境要求

- Python 3（脚本使用 `python-docx`、`python-pptx`、`Pillow`）
- 中文字体：微软雅黑 / 宋体（Windows 自带）
- 可选：LibreOffice / soffice 用于把 DOCX、PPTX 转成 PDF

## 使用方法

```bash
# 1) 生成示意图（输出到 figs/ 或 figs_crown/）
python fig_make.py
python fig_make_crown.py

# 2) 生成图解手册 DOCX
python build_v2.py            # 间隙保持器
python build_v3.py            # 乳牙预成冠

# 3) 生成讲解 PPT
python build_ppt.py           # 间隙保持器
python build_ppt_crown.py     # 乳牙预成冠

# 4) 转 PDF（LibreOffice）
soffice --headless --convert-to pdf "乳牙预成冠修复术_图解手册.docx"
```

## 设计约定

- **少文字、多示意图**：每页以图为主体，配"要点条"与速查表
- 示意图全部由代码绘制（Pillow），可复现、可改色、可改标注，无第三方素材版权问题
- 牙位采用 **FDI 记号法**，牙弓合面观统一为"画面左侧 = 患者右侧"
- 装置尺寸、力值、复诊间隔均为**临床常用参考范围**，非诊疗标准

## 免责声明

本项目产出的是**临床参考与教学资料**，不构成诊疗建议。实际应用须结合患者年龄、牙列阶段、影像学表现、龋风险与依从性个体化判断，并遵循最新版指南、教材与产品说明书。

## 关于

由 DeepSeek Harness 辅助生成的可编辑资料模板，欢迎按本院规范自行修改。
