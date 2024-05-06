import argparse
import logging
from pathlib import Path

import yaml
from openai import OpenAI

from shorts_generator.configs.actor import Actor
from shorts_generator.generator import ShortsGenerator
from shorts_generator.workspace import Workspace

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate YoutubeShorts using GenAI",
    )
    parser.add_argument(
        "--config-file", type=str, required=True, help="Path to the configuration file"
    )
    parser.add_argument(
        "--workspace-dir",
        type=str,
        required=True,
        help="Path to the workspace directory",
    )
    parser.add_argument(
        "--num-images",
        type=int,
        required=False,
        default=2,
        help="Number of images to be generated",
    )
    parser.add_argument(
        "--zoom-image",
        help="Activate zooming images in the Shorts",
        action="store_true",
    )
    parser.add_argument("--content-file", type=str, required=True, help="Path to the content file")
    parser.add_argument(
        "--bgm-file",
        type=str,
        required=False,
        default=None,
        help="Path to the content file",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.config_file) as f:
        config = yaml.safe_load(f)

    client = OpenAI(api_key=config["openai_api_key"])

    actors = [Actor.from_dict(actor) for actor in config["actors"]]

    Path(args.workspace_dir).mkdir(parents=True, exist_ok=True)

    workspace = Workspace(args.content_file, args.workspace_dir, args.bgm_file)

    shorts_generator = ShortsGenerator(
        openai_client=client,
        actors=actors,
        workspace=workspace,
        num_images=args.num_images,
        zoom_image=args.zoom_image,
    )

    shorts_generator.generate_video()
