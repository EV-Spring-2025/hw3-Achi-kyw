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

## Adjustments and PSNR Change

The baseline default values are: `n_grid=100`, `substep_dt=1e-4`, `grid_v_damping_scale=0.9999`, `softening=0.1`

| Material |      Parameter      | value | PSNR  |
|----------|---------------------|-------|-------|
|  jelly   |        n_grid       |   10  | 22.14 |
|  jelly   |        n_grid       |   1   | 22.22 |
|  jelly   |      substep_dt     | 1e-5  | 20.99 |
|  jelly   |      substep_dt     | 1e-6  | 20.50 |
|  jelly   |grid_v_damping_scale | 0.999 | 22.13 |
|  jelly   |      softening      | 1.0   | 20.29 |
|  metal   |        n_grid       |   10  | 14.80 |
|  metal   |      substep_dt     | 1e-5  | 14.73 |
|  metal   |grid_v_damping_scale | 0.999 | 15.22 |
|  metal   |      softening      | 1.0   | 39.89 |

## Observation and Insights

因為運算資源限制，我都是往運算資源小或不影響太多的方向調整。

首先是 n_grid，降到 10 之後樹枝幾乎就不會動了，更不用說降到 1，這個 PSNR 下降在 metal 更為明顯，因為 meatl 在放開之後會直接躺下，所以 PSNR 才會變差那麼多。在運算資源好的情況下應該調高。

其次是 substep_dt，可以發現調整為 1e-5 或 1e-6 可以說學不到太多東西。並且隨著 dt 越小跑的時間越久，整個樹枝幾乎沒有動靜。在運算資源好的情況下應該調高。

再者是 grid_v_damping_scale 我們把其調低，也就是增加阻尼，可以看到不論是 jelly 還是 metal 他的阻力會更大，所以 jelly 會馬上彈回來，metal 會躺不下去。

最後是 softening ，可以看到我們將 softening 調高對於 jelly 的影響是他彈回速度和力道降低很多，所以造成 PSNR 的差距，但是 metal 就沒什麼差，推測是這個材質本身就比較堅硬，加上 softening 影響也不大。

## Video Link

這間為了簡化，我把包含兩種不同材料的 Baseline video 以及調整參數後的所有東西放在同一部影片。

Link: [https://youtu.be/O_n2cQJ1rjc](https://youtu.be/O_n2cQJ1rjc)

## Bonus

提供一段影片，train 一個模型去學習這些參數。一開始會預設這些參數值，然後跑出來的影片使用 PSNR 或其他比較的方式來評估跟原本的影片的差異，讓模型學習參數如何調整。也可以綁個 LLM 先推斷材質的各種參數，從這個初始參數下去會快很多。

# Reference
```bibtex
@inproceedings{xie2024physgaussian,
    title     = {Physgaussian: Physics-integrated 3d gaussians for generative dynamics},
    author    = {Xie, Tianyi and Zong, Zeshun and Qiu, Yuxing and Li, Xuan and Feng, Yutao and Yang, Yin and Jiang, Chenfanfu},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
    year      = {2024}
}
```
