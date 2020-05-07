# reconstructquality
measurement reconstruct quality with PSNR and SSIM

## Installation
```shell
pip install git+https://github.com/pureexe/reconstructquality/
```

## Usage
```shell
reconstructquality <source dir> <target dir>
```

## Sample output
```
------------------------------------
Reconstruction Quality by directory
------------------------------------
                PSRN      SSIM
directory
cam000     17.337255  0.828476
cam001     16.707481  0.816078
------------------------------------
Average Reconstruction Quality
------------------------------------
PSRN    17.022368
SSIM     0.822277
```

## Options
| name | usage | type | description |
| ---- | ----- | ---- | ------------ |
| mute | `--mute` | - | Do not print anything to standard output|
| ssim_window | `--ssim_window <int>` | int | size of window to calculate SSIM. default: 11 |
| threads | `--threads <int>` | int | number of threads to use to measurement reconstruction quality. default: 8 |
| csv | `--csv <filename>` | string | save value to `<filename>` for future calculation | 
