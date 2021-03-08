# VRepair
Vulnerability Repair scripts

## First experiment

For experiments located in `/cephyr/NOBACKUP/groups/snic2021-23-24/vulnerability_repair/only_first_line_context3_models/`

\begin{table}[]
\begin{tabular}{|l|l|l|l|l|l|l|}
\hline
Sweep number & Learning rate & Hidden size & Pre-train validation token accuracy & Fine-tune validation token accuracy & Pre-train test sequence accuracy & Fine-tune test sequence accuracy \\ \hline
0            & 0.001         & 128         & 73.76\% (580k/1m)                   & 71.2\% (1100/5000)                  & 13.21\% (42/318)                 & 12.89\% (41/318)                 \\ \hline
1            & 0.001         & 256         & 74.3\% (460k/1m)                    & 72\% (1400/5000)                    & 12.58\% (40/318)                 & 14.47\% (46/318)                 \\ \hline
2            & 0.001         & 512         & 37.89\% (540k/1m)                   & 33.14\% (200/5000)                  & 0.63\% (2/318)                   & 0.63\% (2/318)                   \\ \hline
3            & 0.001         & 1024        & 37.71\% (460k/1m)                   & 33.93\% (100/5000)                  & 0\% (0/318)                      & 0\% (0/318)                      \\ \hline
4            & 0.005         & 128         & 38.55\% (420k/1m)                   & 34.04\% (1000/5000)                 & 0.31\% (1/318)                   & 0.63\% (2/318)                   \\ \hline
5            & 0.005         & 256         & 34.04\% (140k/1m)                   & 30.47\% (400/5000)                  & 0.63\% (2/318)                   & 0.63\% (2/318)                   \\ \hline
6            & 0.005         & 512         & 31.65\% (160k/1m)                   & 28.06\% (400/5000)                  & 0\% (0/318)                      & 0\% (0/318)                      \\ \hline
7            & 0.005         & 1024        & 32.9\% (220k/1m)                    & 29.61\% (1600/5000)                 & 0.63\% (2/318)                   & 0.63\% (2/318)                   \\ \hline
8            & 0.0001        & 128         & 71.14\% (500k/1m)                   & 69.16\% (200/5000)                  & 13.21\% (42/318)                 & 14.15\% (45/318)                 \\ \hline
9            & 0.0001        & 256         & 74.86\% (540k/1m)                   & 72.59\% (500/5000)                  & 15.09\% (48/318)                 & 15.41\% (49/318)                 \\ \hline
10           & 0.0001        & 512         & 76.41\% (420k/1m)                   & 75.48\% (1700/5000)                 & 15.72\% (50/318)                 & 16.67\% (53/318)                 \\ \hline
11           & 0.0001        & 1024        & 76.91\% (480k/1m)                   & 77.46\% (300/5000)                  & 17.3\% (55/318)                  & 17.92\% (57/318)                 \\ \hline
12           & 0.00005       & 128         & 68.67\% (500k/1m)                   & 66.22\% (500/5000)                  & 9.43\% (30/318)                  & 10.06\% (32/318)                 \\ \hline
13           & 0.00005       & 256         & 72.52\% (480k/1m)                   & 70.79\% (800/5000)                  & 12.58\% (40/318)                 & 12.89\% (41/318)                 \\ \hline
14           & 0.00005       & 512         & 75.12\% (440k/1m)                   & 73.39\% (400/5000)                  & 14.47\% (46/318)                 & 16.04\% (51/318)                 \\ \hline
15           & 0.00005       & 1024        & 76.33\% (380k/1m)                   & 76.2\% (200/5000)                   & 16.35\% (52/318)                 & 16.35\% (52/318)                 \\ \hline
16           & 0.0005        & 128         &                                     &                                     &                                  &                                  \\ \hline
17           & 0.0005        & 256         &                                     &                                     &                                  &                                  \\ \hline
18           & 0.0005        & 512         &                                     &                                     &                                  &                                  \\ \hline
19           & 0.0005        & 1024        &                                     &                                     &                                  &                                  \\ \hline
\end{tabular}
\end{table}

## Second experiment

Experiments at CSU using a model with starting learning rate of 0.0005 and hidden size of 256.

| File                         | Samples (Lines) | Average tokens per sample |
|------------------------------|-----------------|---------------------------|
| BugFix_train_src.txt         | 524724          | 248.9                     |
| BugFix_train_tgt.txt         | 524724          |  25.2                     |
| BugFixFine_train_src.txt     | 2990            | 285.5                     |
| BugFixFine_train_tgt.txt     | 2990            |  27.8                     |
| BugFixFine_2019_test_src.txt | 187             | 279.9                     |
| BugFixFine_2019_test_tgt.txt | 187             |  27.1                     |

| Step count    |                           | Beam width 50               |
| Pretrain+Tune | Training token accuracy   | 2019 test sequence accuracy |
|---------------|---------------------------|-----------------------------|
| 300K+0        |   77.67%                  | 12.3% (23 out of 187)      |
| 360K+0        |   78.08%                  | 11.8% (22 out of 187)      |
| 360K+200      |   77.04%                  | 10.2% (19 out of 189)      |
| 360K+1000     |   79.30%                  |  9.1% (17 out of 189)      |
