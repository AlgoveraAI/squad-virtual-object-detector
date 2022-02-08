<img src="images/virtual.jpeg" width="100%">

# Squad: Virtual Object Detector
This project aims to build object detection for the metaverse by training models with the [ImageAI](https://github.com/OlafenwaMoses/ImageAI) library on web images captured using [Puppeteer](https://github.com/puppeteer/puppeteer).

# Contents

- [👪 Squad](#-squad)
- [🏗 Initial Setup](#-initial-setup)
- [🏛 License](#-license)
- [Information](#-information)

# 👪 Squad

Lead: alextitonis (GitHub)

Grant Proposal: https://forum.algovera.ai/t/virtual-object-detector/25

Notion: https://algovera.notion.site/Squads-194768658a044302a0cdc24d5d758b9d?p=13587733017d4524832fd51f3780969a

# 🏗 Initial Setup 

## Set up environment

Open a new terminal and:
```console
#clone repo
git clone https://github.com/AlgoveraAI/squad-virtual-object-detector.git
cd squad-virtual-object-detector

#create a virtual environment
python3 -m venv venv

#activate env
source venv/bin/activate

#Install libraries.
pip install -r requirements.txt

#Edit the variables
Rename the .env.default to .env and edit the variables inside
```

To run the trainer use the trainer.py
For the detector is the detector.py
For the editor run the /editor/editor.py file
The editor includes functions for train and detection (images, videos)
The capturers folder includes varius scripts that can be used to capture images:
* browser.py -> is the wrapper for puppeteer (using pyppeteer) it includes some example functions to enter a website and capture images
* fullScreen.py -> includes a function to capture a screenshot in full screen
* gameWindow.py -> includes a function to capture a screenshot from a window (not only from games) using the window title - windows only
* videoCapturer.py -> includes a function that captures frames from a video and turns them into images

# Information
## How to train a new model
Create a folder, inside create 2 new folders called test and train, inside each add the same folders with the names of the images (car, human, etc)
For example:
trees/train/pine
trees/train/oak
trees/test/pine
trees/test/oak

Train images should be atleast 500, while the test folder should include atleast 200 images to train a proper model.

To train it you can either run the trainer.py script using command line or through the editor tab - trainer, upload a zip file with all the folders/images and it will do the job for you!

# 🏛 License

The license is MIT. [Details](LICENSE)
