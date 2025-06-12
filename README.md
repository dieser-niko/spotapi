# SpotAPI

> [!WARNING]
> This is still a WIP

> [!CAUTION]
> This API is undocumented and may change at any time.
> It is not recommended to use this API in production.
> Make sure to check if [spotipy](https://github.com/spotipy-dev/spotipy) satisfies your needs before using this API.

## What is SpotAPI?

SpotAPI is a Python wrapper for the endpoint `https://api-partner.spotify.com/`.
Its normal usage is to be used in the frontend of a web application and can unlock some features that are not available in the official Spotify API.

## Installation

Just clone the repository and install the requirements:

```bash
git clone https://github.com/dieser-niko/spotapi.git
cd spotapi
pip install -r requirements.txt
```

## Usage

Generate `functions.json` file with the following command:

```bash
python get_functions.py
```

Then you can run the `main.py` file to use the API:

```bash
python main.py
```

I might convert this to an actual package in the future, but for now it is just a script that you can run.

# TODO

- [ ] Nested function finder