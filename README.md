# Anime Presence
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)


## Overview
This application shows that you are watching an anime on your own Discord profile !

![screen1](https://raw.githubusercontent.com/Guiguim255/database/master/anime_presence_screenshot.png)

## Get Started

### Requirements
This app requires to have [Python](https://www.python.org/downloads/) 3.7 or more, and the [pypresence](https://pypi.org/project/pypresence/), [Beatiful Soup](https://pypi.org/project/beautifulsoup4/), [aiohttp](https://pypi.org/project/aiohttp/) and [PyQt5](https://pypi.org/project/PyQt5/) python packages.

If you are missing one/some of them, use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies by doing : 
```
pip install -r requirements.txt
```

### How to use
You need to run the `main.py` file, a window will appear.
Then, write the name of the anime in the bar, a suggestion widget will appear.
Choose your anime, select the episode and the season (if there are), and click "Start".

### How to change the language
If you want to change the language of your application **and** the language of presence, click on the "Settings" button.
Go in the "LANGUAGE" section, then choose your language (if your language is not showing, it is not available. If you want to help to translate, feel free to PR !).

### How to use a personal presence application
You want a presence image with a specific anime, but it is not available with the base app ?
You can use your own app and add the presence image for any anime you want !

To use your own app, go to Settings > PERSONAL APPLICATION. Enable the checkbox and paste your app id (don't forget to save changes).
Now your presence app will be used by your client.

You can save the image of an anime by right-clicking on it in the anime suggest (⚠ keep the file name suggested by anime presence).
When you downloaded all the images you need, click on the "Add assets" button, it will open the assets manager of your app in your browser.
Click on "Add images" and select the images you downloaded. You are done !

## License
This project is under MIT License.
For more information, go check the [LICENSE][license].

## Credits
* Temporary "A" logo made by [DinosoftLabs](https://www.flaticon.com/authors/dinosoftlabs) from [Flaticon](https://www.flaticon.com/)
* Gear icon made by [Freepik](https://www.flaticon.com/authors/freepik) from [Flaticon](https://www.flaticon.com/)

[license]: https://github.com/Guiguim255/Anime-Presence/blob/master/LICENSE