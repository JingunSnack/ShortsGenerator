# ShortsGenerator

Youtube Shorts movie generation using GenAI


## Prerequisite

### ImageMagick

Install [ImageMagick](https://www.imagemagick.org/script/download.php) for MoviePy text clips.


## Installation

```bash
pip install shorts-generator
```

## How to use

Before running the script, you have to provide an OpenAI API key in the configuration yaml file.

And you may add/remove/modify actors in the configuraiton file. Please refer to `config_example.yaml`.

```bash
generate-shorts --config-file config.yaml \
--content-file input.txt \
--workspace-dir ./output \
--num-images 4 \
--zoom-image \
--bgm-file bgm.mp3
```

## Example Youtube channels

- [@AliceWaBob](https://www.youtube.com/@AliceWaBob)
