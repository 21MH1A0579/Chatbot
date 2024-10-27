# Neura, The Deep-Learning Chatbot

## Overview
Neura is an intelligent, multi-purpose chatbot designed using Python and powered by deep learning. It leverages Natural Language Processing (NLP) and machine learning to analyze user messages, classify intents, and respond accurately. From casual chatting to helping with daily tasks, Neura is a robust virtual assistant capable of handling varied interactions. The chatbot is hosted using Flask for seamless performance and easy web deployment.

## Features
- **Real-Time Conversations**: Neura can engage in interactive chats and respond to user queries efficiently.
- **Task Management**: Assists in setting timers, providing weather updates, and fetching information via Google.
- **Deep Learning Integration**: Utilizes TensorFlow and NLP to understand and classify user intents with precision.
- **Modular Design**: The chatbot’s codebase is modular, allowing easy updates and scaling.
- **Flask Hosting**: Hosted on Flask for straightforward deployment and local testing.

## Project UI
**Home Page**  
The main screen welcomes users and provides a button to initiate the chat experience with Neura.

![Home Page](https://github.com/21MH1A0579/Chatbot/blob/23071373c505051d4442dcfe6bc770dc9456d58d/UI/main_screen.png)

## Chat Page
The chat page allows users to interact with Neura in real-time. It features a user-friendly interface where users can type their messages and receive responses from the chatbot. The conversation history is displayed, providing context for ongoing discussions.

![Chat Page](https://github.com/21MH1A0579/Chatbot/blob/7bbb7cedeb5ea8fe171c24f7989c8a35187493a6/UI/chat_screen.png)



## Getting Started
Follow these steps to set up and run Neura locally:

### Prerequisites
1. **Python 3.8+**: Ensure you have Python installed on your system.
2. **Required Libraries**: Install the libraries listed in `requirements.txt` to run the project smoothly.

### Installation Steps

1. **Clone the Repository**  
   Open your terminal or Command Prompt and clone the repository with:
   ```bash
   git clone https://github.com/21mh1a0579/Chatbot.git

2. **Navigate to the Project Directory**  
   Change to the project directory by running:
   ```bash
   cd Chatbot
3. **Install Required Libraries**
   Ensure you have all the required libraries listed in requirements.txt. Install them by running:
   ```bash
   pip install -r requirements.txt
4. **Set Up Environment Variables**
   To run the Flask application, set the environment variable for Flask. Use the following command based on your operating system:
   ```bash
   set FLASK_APP=chatbot.py
5. **Run the Application**
   Start the Flask server with the following command:
   ```bash
   flask run
   
