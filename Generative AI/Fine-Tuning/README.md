Drug Malady Classification using OpenAI GPT Fine-Tuning

This project uses OpenAI's GPT model to classify the medical maladies associated with various drugs based on a given dataset of drug names and their corresponding maladies.

### 1. Set up the environment

1. Clone the repository or download the project files.
```bash
git clone https://github.com/vaishnavi477/Machine-Learning.git
cd Generative AI/Fine-Tuning
```

2. Install the required Python libraries by running:
```bash
pip install -r requirements.txt
```
3. Set up environment variables for OpenAI API:

Create a .env file in the project directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

4. Download the Medicine_description.xlsx dataset file. This should contain the following columns:
  Drug_Name: Name of the drug.
  Reason: Malady associated with the drug.

### 2. Download programs and related documentation

This project includes a Python script that will:

    Load an Excel dataset (Medicine_description.xlsx).
    Map maladies (reasons) to unique identifiers.
    Convert the data to JSONL format compatible with OpenAI's fine-tuning API.
    Upload the data for fine-tuning a GPT-3.5 model.
    Monitor the fine-tuning process.
    Test the fine-tuned model with sample drug descriptions.

### 3. Process of program execution

1. To run the program:
    Prepare the Excel Dataset:
        1. Ensure the Excel file Medicine_description.xlsx exists in the project directory.
        2. Ensure that the sheet contains two columns: Drug_Name and Reason.

2. Run the Script:
```bash
python3 Fine_Tuning_2000_Drugs.py
```

### 4. Screenshot of execution results



ug_malady.py:








