# Customer Support System

This project is a Flask web application that generates customer comments about electronics products using the OpenAI GPT model. It supports translation into various languages, handles moderation of comments, and prevents prompt injections.

## Project Structure

├── app.py # Main Flask application 
├── products.py # Contains list of products 
├── templates
    └── index.html # HTML template for the front-end 
├── data
    └── products.json
├── evaluation_part_1.py # Evaluation based on user question
├── evaluation_part_2.py # Evaluation based on user question
├── .env # API key configuration file 
├── requirements.txt # Python dependencies 
└── README.md # Project documentation


## Features

1. **Generate Comments**: Generate customer comments about selected products.
2. **Translate Comments**: Translate generated comments into different languages.
3. **Moderation**: Check the moderation status of user inputs.
4. **Prompt Injection Protection**: Secure the application from prompt injection attacks.
5. **Chain of Thought Reasoning**: Answer user questions using step-by-step reasoning.
6. **Factual or Non-Factual**: Answer if Output is Factual or Non Factual.
7. **Evaluation**:  Evaluate based on user questions.

## Prerequisites

Make sure you have the following installed:
- Python 3.7+
- Flask
- OpenAI API key (sign up for one [here](https://beta.openai.com/signup/))
- dotenv for loading environment variables

## Installation

Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/customer-support-system.git
cd customer-support-system/
```

Step 2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

Step 3. Install the required Python packages:
   requirements.txt includes
    Flask==2.3.2
    openai==0.27.0
    python-dotenv==1.0.0
    ```bash
   pip install -r requirements.txt
   ```

Step 4. Create a `.env` file in the root directory of the project and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key # Replace with your api key
   ```

Step 5. Run the `.env` file:
   ```bash
   source /.env
   ```
   
Step 4. Create a `.env` file in the root directory of the project and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key # Replace with your api key
   ```

Step 55. Run the `.env` file:
   ```bash
   source /.env
   ```
   
## Usage

1. Run the Flask app:
   ```bash
   flask run
   ```

2. Open your browser and go to the local server link (usually http://127.0.0.1:5000/) to interact with the chatbot. Then do the following:

    Select a Product: Choose a product from the dropdown list.
    Select Language: Choose the language for translating the comment (if needed).
    Generate Comment: Click the 'Generate Comment' button to create a customer review.
    Ask a Question: Input a question about the generated comment and submit to get a response.
    Check Moderation and Prompt Injection: View moderation and prompt injection results for the question asked.
    Chain of Thoughts: Get the response about the question asked with proper reasoning.
    Check Output: Check if output is factual or non factual.

3. Run the python files:
    ```bash
    python3 evaluation_part_1.py
    python3 evaluation_part_2.py
    ```

## Contact
For any queries, feel free to reach out to the project maintainer at vaishnavigpatil21640@gmail.com.

## Screenshot of execution results

![alt text](Execution_1.png)
![alt text](Execution_2.png)
![alt text](Execution_3.png)
![alt text](Execution_4.png)
![alt text](Execution_5.png)
![alt text](Execution_6.png)