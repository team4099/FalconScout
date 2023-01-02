# FalconScout Quick Start

## Download FalconScout

Go to your preferred folder and clone the repository.

```
git clone https://github.com/team4099/FalconScout.git
```

## Setup FalconScoutCore

Then enter the repository and the FalconScoutCore folder

```
cd FalconScout/falconscoutcore
```

Set up a virtual environment by typing the following commands. *Note:* that the following applies if you have Python 3.10 installed. If you don't visit the [Python Downloads Page](https://www.python.org/downloads/) and download Python 3.10. If you would like to use another version of Python, run the same command with the version replaced.
```
python3.10 -m venv venv
source venv/bin/activate
```

Now, install the dependencies.
```
pip install -r requirements.txt
```

### Running

Simply run the app by doing
```
python app.py
```

You should be good to go! The output will tell you what it's running on (usually on `localhost:5000`)