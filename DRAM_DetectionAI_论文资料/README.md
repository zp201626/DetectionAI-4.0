# DRAM DetectionAI 公开论文资料

本目录用于给 DRAM DetectionAI 提供公开的检测原理、缺陷信号和算法背景资料。

## 使用边界

这些论文可以支持光散射、表面缺陷和颗粒信号、电子束检测系统、全片宏观检测、缺陷签名分析、图像分类和模型漂移等通用判断。

这些论文没有公开 eScan、460、430、BF、F300 的内部 recipe、光学配置、阈值、扫描速度、焦距、灵敏度档位或放行规则。因此不能直接把论文中的数值转换成机台参数。实际推荐应优先使用公司内部受控的机台手册、recipe 历史、golden wafer、qualification/correlation 数据和 defect owner 规则。

本资料集按用户要求未纳入 SP 机台。

## 已下载的开放全文

| 文件 | 论文 | 关联方向 | 来源 |
|---|---|---|---|
| arxiv_1702.07051_Modeling_Laser_Beam_Scattering_by_Defects_on_Semiconductor_Wafers.pdf | Srikumar Sandeep, Alexander Kokhanovsky, Modeling Study of Laser Beam Scattering by Defects on Semiconductor Wafers (2017) | 光散射、颗粒/表面缺陷信号；可作为 BF 和宏观光学检测的物理背景 | https://arxiv.org/abs/1702.07051 |
| arxiv_0805.0495_Electron_Optic_Design_of_Arrayed_EBeam_Microcolumns.pdf | V. V. Kazmiruk, T. N. Savitskaja, Electron Optic Design of Arrayed E-Beam Microcolumns Based Systems for Wafer Defects Inspection (2008) | 电子束微柱、电子光学和 wafer defect inspection；可作为 eScan 类电子束检测的通用原理参考 | https://arxiv.org/abs/0805.0495 |
| arxiv_2302.09565_Optimizing_YOLOv7_for_Semiconductor_Defect_Detection.pdf | Enrique Dehaerne et al., Optimizing YOLOv7 for Semiconductor Defect Detection (2023) | 缺陷图像检测和模型评估；用于后端 defect classification，不用于推导物理 recipe | https://arxiv.org/abs/2302.09565 |
| arxiv_2407.12724_Continual_Learning_for_Advanced_Node_Defect_Inspection.pdf | Amit Prasad et al., An Evaluation of Continual Learning for Advanced Node Semiconductor Defect Inspection (2024) | 工艺节点变化、数据漂移和持续学习；用于维护 DetectionAI 的案例库和模型评估 | https://arxiv.org/abs/2407.12724 |
| osti_940544_Whole_Wafer_Macroscale_Inspection_Software.pdf | K. W. Tobin, Development of a Whole-Wafer, Macroscale Inspection Software Method for Semiconductor Wafer Analysis (ORNL, 2003) | 全片宏观检测、缺陷签名分析和分类；可作为宏观检测流程参考 | https://www.osti.gov/biblio/940544 |

## 用户提供的电子束论文

下列文件来自本机的“电子束论文”目录。其中已确认带有 Creative Commons Attribution 4.0 International License 的论文已复制到本资料集：

| 文件 | 论文 | DOI/来源 |
|---|---|---|
| 041605_1_In_situ_electrical_property_quantification_of_memory_devices.pdf | Muneyuki Fukuda et al., In situ electrical property quantification of memory devices by modulated electron microscopy | https://doi.org/10.1117/1.JMM.15.1.014001 |
| electronics-06-00087-v2_Smart_E-Beam.pdf | Ankush Oberai, Jiann-Shiun Yuan, Smart E-Beam for Defect Identification & Analysis in the Nanoscale Technology Nodes: Technical Perspectives | https://doi.org/10.3390/electronics6040087 |

这两篇资料对 memory-device voltage contrast、电子束剂量、缺陷电学对比和纳米节点缺陷分析有直接参考价值。

## 未复制到公共仓库的本地论文

本机目录中的 IEEE、Elsevier、会议论文和中文论文未确认具有允许公共再分发的开放许可，因此没有把原文上传到公共 GitHub。它们可以在本机继续阅读，并将题名、DOI 或摘要整理成内部知识库索引后再使用。

## 可补充检索的 DRAM 论文

- Defect requirements for advanced 300mm DRAM substrates, DOI: 10.1016/S1369-8001(02)00137-3
- Sensitivity Enhancement by Enabling Design-Based Inspection for DRAM, DOI: 10.1109/ASMC.2019.8791745
- Using statistical median to check sensitivity of defect inspection, DOI: 10.1109/SMTW.2002.1197404

可在 Google Scholar 中使用论文标题或 DOI 检索这些条目，并优先选择作者自存档、机构仓储或出版社明确开放的版本。

## 建议的 RAG 元数据字段

建议给每个 PDF 增加以下元数据：

source_type: public_paper
inspection_scope: optical | electron_beam | macro | algorithm
candidate_machine_family: BF | F300 | eScan | unknown
is_internal_recipe_source: false
requires_internal_validation: true

回答 DRAM layer 检测参数问题时，DetectionAI 应区分论文提供的通用物理原理、公司内部机台的已验证能力，以及当前产品、layer 和 defect owner 的具体限制。只有后两类资料齐全时，才可以给出可执行的 recipe 建议。
