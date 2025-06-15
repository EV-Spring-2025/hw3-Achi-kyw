[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/SdXSjEmH)
# EV-HW3: PhysGaussian

This homework is based on the recent CVPR 2024 paper [PhysGaussian](https://github.com/XPandora/PhysGaussian/tree/main), which introduces a novel framework that integrates physical constraints into 3D Gaussian representations for modeling generative dynamics.

You are **not required** to implement training from scratch. Instead, your task is to set up the environment as specified in the official repository and run the simulation scripts to observe and analyze the results.


## Getting the Code from the Official PhysGaussian GitHub Repository
Download the official codebase using the following command:
```
git clone https://github.com/XPandora/PhysGaussian.git
```


## Environment Setup
Navigate to the "PhysGaussian" directory and follow the instructions under the "Python Environment" section in the official README to set up the environment.


## Running the Simulation
Follow the "Quick Start" section and execute the simulation scripts as instructed. Make sure to verify your outputs and understand the role of physics constraints in the generated dynamics.


## Homework Instructions
Please complete Part 1–2 as described in the [Google Slides](https://docs.google.com/presentation/d/13JcQC12pI8Wb9ZuaVV400HVZr9eUeZvf7gB7Le8FRV4/edit?usp=sharing).

## How to run

Follow the instruction of PhysGaussian, and then run the sample ficus video.

註：安裝時會遇到一些問題，像是 `simple_knn.cu` 要加上 `#include <cfloat>` 之外，工作站上的 cuda 是 12.8，還需要安裝版本符合的 pytorch。另外還要把版本符合的 g++ 跟 NVCC 安裝進入 conda 裡面並把 `CUDA_HOME`、`PATH`、`LD_LIBRARY_PATH` 指定成裝好的位置。

For adjustment, just simply modify `config/ficus_config.json` to change the parameters.

Simply run a python script to calculate PSNR by `from skimage.metrics import peak_signal_noise_ratio`.

I provided a psnr script in `run_psnr.py`

## Adjustments and PSNR Change

The baseline default values are: `n_grid=50`, `substep_dt=1e-4`, `grid_v_damping_scale=0.9999`, `softening=0.1`

| Material |      Parameter      | value | PSNR  |
|----------|---------------------|-------|-------|
|  jelly   |        n_grid       |   10  | 22.14 |
|  jelly   |        n_grid       |   1   | 22.22 |
|  jelly   |      substep_dt     | 1e-5  | 20.99 |
|  jelly   |      substep_dt     | 1e-6  | 20.50 |
|  jelly   |grid_v_damping_scale | 0.999 | 22.13 |
|  jelly   |grid_v_damping_scale | 0.99  | 21.98 |
|  jelly   |      softening      | 1.0   | 20.29 |
|  jelly   |      softening      | 0.01   | 41.72 |
|  metal   |        n_grid       |   10  | 14.80 |
|  metal   |        n_grid       |   1   | 14.72 |
|  metal   |      substep_dt     | 1e-5  | 14.73 |
|  metal   |      substep_dt     | 1e-6  | 14.72 |
|  metal   |grid_v_damping_scale | 0.999 | 15.22 |
|  metal   |      softening      | 1.0   | 39.89 |
|  metal   |      softening      | 0.01   | 14.77 |

## Observation and Insights

在運算資源限制下，我的參數調整主要朝向降低或不顯著影響計算量的方向進行，獲得以下發現：

首先是 n_grid，我發現此參數存在一個關鍵的「解析度閾值」。當 n_grid 降到 10 之後，網格變得過於粗糙，無法解析樹枝的細長幾何結構，導致計算出的作用力無法產生有效的彎曲力矩，因此能觀察到「樹枝幾乎就不會動了」。這個 PSNR 下降在 metal 上更為明顯，不僅是因為 metal 在影片中盆栽會直接「躺下」，更是因為它的預期動態範圍（從直立到倒下）遠大於 jelly 的輕微晃動。當 n_grid 過低導致這個主要動態完全消失時，與 baseline 的巨大差異自然會造成 PSNR 的劇烈惡化。因此，在運算資源好的情況下，應優先考慮調高 n_grid 以確保物理行為的正確性。

其次是 substep_dt，我觀察到當 dt 調整為 1e-5 或 1e-6 時，在 Module 時間花費極長，在 1e-6 可能會超過一小時，因此從影片和極低的 PSNR 中可以看到效果很差。不過調高 dt 則可能會讓運算資源承受不住，因此原本的 1e-4 可能還是比較好的選擇。

再者是 grid_v_damping_scale，我將其調低以增加阻尼，觀察到這會顯著改變兩種材質的動態行為。這背後是 damping 作為一個全局參數，與不同材質的主要驅動力產生了不同的交互作用。對於 jelly，其動態由彈性主導，增加的阻尼快速耗散了其內部能量，使其無法持續震盪，所以會「馬上彈回來」並迅速靜止。對於 metal，其主要動態是重力驅動的倒塌，而強阻尼就像一種黏滯力，抵抗了這個過程，所以會「躺不下去」。

最後是 softening，數據揭示了此參數對兩種材質都有影響，但其作用機制不同。對於 jelly，softening 直接影響其可見的「彈性」與「柔軟度」。softening 提高時，材質變得過軟，導致 PSNR 下降。而對於 metal，較高的 softening 值 PSNR 相當高，而過低的值卻導致了模擬較差。這說明了 softening 在不同材質下作用的效果也有所差距。
## Video Link

這間為了簡化，我把包含兩種不同材料的 Baseline video 以及調整參數後的所有東西放在同一部影片。另外附上自己測試的其他材料

Link: [https://youtu.be/mhZwrJ0YE_Q](https://youtu.be/mhZwrJ0YE_Q)

## Bonus

我會設計一個基於「反向模擬」的框架。這個系統會以目標材料的影片作為輸入，反覆進行「模擬、比較、調整」的優化循環。接著，這個系統能算出「如何調整參數才能減少差異」的梯度，並據此自動更新參數。為了加速這個過程，還可以整合一個大型語言模型 (LLM)，讓它根據影片內容或文字描述（如「有彈性的金屬」）提供一組高品質的初始參數猜測，使優化能從一個更好的起點開始，從而更快收斂到理想結果。

# Reference
```bibtex
@inproceedings{xie2024physgaussian,
    title     = {Physgaussian: Physics-integrated 3d gaussians for generative dynamics},
    author    = {Xie, Tianyi and Zong, Zeshun and Qiu, Yuxing and Li, Xuan and Feng, Yutao and Yang, Yin and Jiang, Chenfanfu},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
    year      = {2024}
}
```
