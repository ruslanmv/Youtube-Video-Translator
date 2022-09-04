# How to translate videos in YouTube with Python

Hello everyone, today we are going to build an interesting application in **Python** that translates the audio language from **YouTube**  into another language.

This interesting tool may be useful, for example if you want to see any video from **YouTube**  that you cannot understand and you can translate the video into your favorite language. Moreover can be helpful to people who has visual problems and but can listen as well.



For example if you have this video in **English**, 

<iframe src="https://player.vimeo.com/video/746346327?h=e96b96f665&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" width="500" height="281" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Youtube Video Translator - English ( Original)"></iframe>

and you want to translate for example to **Spanish** 

<iframe src="https://player.vimeo.com/video/746346348?h=0952bb6849&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" width="500" height="281" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Youtube Video Translator -  Video translated to Spanish"></iframe>



or even to **Japanese**.

<iframe src="https://player.vimeo.com/video/746346369?h=392d2d8750&amp;title=0&amp;byline=0&amp;portrait=0&amp;speed=0&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" width="500" height="281" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Youtube Video Translator -  Video translated to Japanse"></iframe>



# Introduction 

I have developed this program taking the **subscripts** of **YouTube** and **translate** them, if they do not exist, then it is extracted the audio and is  applied the technique of  **speech recognition** and then applied the technique of  **text to speech**  then  it is replaced the audio video with the translated audio.

Notice that this program is **not designed** to translate **musical videos** or **videos larger than 10 minutes**. Because there are limits of the **APIs** used in this program.  Moreover, the quality of the audio should be good.

Well, is time to explain how to use this program, first at all we need to create our environment.

## Step 1. Creation of the environment

### Installation of Conda

First you need to install anaconda at this [link](https://www.anaconda.com/products/individual)

![img](assets/images/posts/README/1.jpg)

additionally we need **Git** , you can download [here](https://git-scm.com/downloads).

You can create an environment called **youtube-translator**, but you can put the name that you like.

```
conda create -n youtube-translator python==3.8
```

If you are running anaconda for first time, you should init conda with the shell that you want to work, in this case I choose the cmd.exe

```
conda init cmd.exe
```

and then close and open the terminal

```
conda activate youtube-translator
```

if you want to use the notebook to run this app  type the following commands:

```
conda install ipykernel
python -m ipykernel install --user --name youtube-translator --display-name "Python (Youtube)"
```

For this project we need to install the the following repository

```
git clone https://github.com/ruslanmv/Youtube-Video-Translator.git
```

then we enter to the directory

```
cd Youtube-Video-Translator.git
```

then you enter to the folder that have been created

```
cd Youtube-Video-Translator
```

and for today, we  are going to run a simple WebApp so go to the folder gradio

```
cd gradio
```

and then we install al the requirements by typing

```
pip install -r requirements.txt
```

once was installed  then you are ready to execute the app.

![image-20220904205915226](assets/images/posts/README/image-20220904205915226.png)

## Step 2.  Run the app



To execute the app just type

```
python app.py
```

and then  you will see

![](assets/images/posts/README/run.jpg)

then copy the **local URL** and open your favorite **WebBrowser** and paste it,  

or just click  [http://127.0.0.1:7860/](http://127.0.0.1:7860/) and will open somthing like

![image-20220904210750257](assets/images/posts/README/image-20220904210750257.png)



Then just for example click over **the first example** and **click submit** , you wait like a minute



![image-20220904210907983](assets/images/posts/README/image-20220904210907983.png)

and then play.

You can  choose **initial language** that  is the source **originally** and **final language** is the language that you want.



from **English** also you can translate to **German**

<iframe src="https://player.vimeo.com/video/746346337?h=757bf0bf74&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" width="500" height="281" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Youtube Video Translator -  Video translated to German"></iframe>

and **Italian**

<iframe src="https://player.vimeo.com/video/746346357?h=7966a7a290&amp;title=0&amp;byline=0&amp;portrait=0&amp;speed=0&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" width="500" height="281" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Youtube Video Translator -  Video translated to Italian"></iframe>



For more videos, you can visit the result of this **WebApp** here :



**Congratulations!**  You have played with me creating amazing videos from **YouTube** with **Python**.
