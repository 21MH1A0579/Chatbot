# Ted, The Deep-Learning Chatbot

## About this Project
Ted is a multipurpose chatbot made using Python3, capable of chatting and assisting with daily tasks. It uses NLP and Deep-Learning to analyze user messages, classify them into broader categories, and respond with suitable messages or necessary information. Ted is hosted using Flask and is available on Heroku at the link specified above.

## Project UI
Home Page:

![image](https://raw.githubusercontent.com/21mh1a0579/Chatbot/master/UI/main_screen.PNG?token=AKGUW5C2TMM37OQE5FSPXLS66D55O)

To run it locally on your system, follow these steps:

1. Clone this repository onto your system. On Command Prompt, run the following command:

    ```bash
    git clone https://github.com/21mh1a0579/Chatbot.git
    ```

2. Change your directory to Chatbot:

    ```bash
    cd Chatbot
    ```

3. Make sure you have all the required libraries listed in `requirements.txt`. If any are missing, install them using pip. Type this command into your Command Prompt, replacing 'Your-library-name' by the required library name:

    ```bash
    pip install Your-library-name 
    ```

4. Then, run the following commands to start the application:

    ```bash
    set FLASK_APP=chatbot.py
    flask run
    ```

5. Enter the URL provided after running the previous commands into your web browser.

Ted is now ready to chat!
