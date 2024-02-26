# Story Teller

This is a small experiment of an app which can be used to generate epic stories using LLMs.

## Pre-requisites

You will need to have an [OpenAI API key](https://platform.openai.com/api-keys) and in case you want to use the My Midjourney API, a [MyMidjourney Token](https://www.mymidjourney.ai/setup).

## Installation instructions

Please make sure to install [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) first.

```bash
conda create -n story_teller python=3.12
conda activate story_teller
pip install poetry
poetry install
# This is important for PDF generation
playwright install
```

## Running unit tests

```bash
python -m unittest
```

## Running the command line application

```bash
python.exe ./story_teller/story_teller_main_cli.py
```

## Running the local GUI application

```bash
python .\story_teller\ui\wx\main.py
```