import pandas as pd
import openai, os
import time, json
from dotenv import load_dotenv, find_dotenv

# Load environment variables for OpenAI API
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the data from Excel (Medicine_description.xlsx)
def load_data_from_excel(file_path, nrows=2000):
    """
    Loads the first 'nrows' rows of data from the Excel file.
    """
    try:
        df = pd.read_excel(file_path, sheet_name='Sheet1', header=0, nrows=nrows)
        print(f"\nData loaded successfully from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading data from Excel: {e}")
        return None

# Map each malady (Reason) to a unique identifier
def map_maladies_to_ids(df):
    """
    Maps each malady to a unique identifier.
    """
    reasons = df["Reason"].unique()
    reasons_dict = {reason: i for i, reason in enumerate(reasons)}
    return reasons_dict

# Convert the data to JSONL format
def create_chat_format(df, reasons_dict, output_jsonl_path):
    """
    Converts the DataFrame to chat format and saves it in JSONL format.
    """
    try:
        chat_data = df.apply(create_chat_format_row, axis=1, reasons_dict=reasons_dict)
        
        # Convert to JSONL format and save it
        with open(output_jsonl_path, "w") as jsonl_file:
            for record in chat_data:
                jsonl_file.write(json.dumps(record) + '\n')
        
        print(f"\nConversion successful! Data saved as {output_jsonl_path}")
    except Exception as e:
        print(f"Error during chat format creation: {e}")

# Helper function for converting each row into chat format
def create_chat_format_row(row, reasons_dict):
    user_message = f"Drug: {row['Drug_Name']}\nMalady:"
    assistant_message = f" {reasons_dict[row['Reason']]}"
    
    return {
        "messages": [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": assistant_message}
        ]
    }

# Upload the training file to OpenAI
def upload_file(file_path):
    try:
        response = openai.files.create(file=open(file_path, "rb"), purpose="fine-tune")
        print(f"\nFile uploaded: {response.id}")
        return response.id
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

# Start the fine-tuning job
def start_fine_tuning(training_file_id, model="gpt-3.5-turbo-0125"):
    try:
        response = openai.fine_tuning.jobs.create(
            training_file=training_file_id,
            model=model,
            suffix="drug_malady_data"  # Adding the suffix directly in the fine-tuning job
        )
        print(f"\nFine-tuning job started: {response.id}")
        return response.id
    except Exception as e:
        print(f"Error starting fine-tuning: {e}")
        return None

# Monitor the fine-tuning job and save metrics to CSV
def monitor_and_save(job_id):
    try:
        while True:
            job_status = openai.fine_tuning.jobs.retrieve(job_id)
            if job_status.status == 'succeeded':
                print("\nFine-tuning completed successfully!")
                print("Fine Tuned model: ", job_status.fine_tuned_model)
                return job_status.fine_tuned_model  # Return fine-tuned model ID
            elif job_status.status == 'failed':
                print("Fine-tuning failed!")
                break
            else:
                print(f"Fine-tuning in progress... (status: {job_status.status})")
                time.sleep(90)  # Wait for 120 seconds before checking again
    except Exception as e:
        print(f"Error monitoring job: {e}")

# Testing the fine-tuned model with sample data
def test_fine_tuned_model(model):
    # Sample drugs for testing
    drugs = [
        "What is 'A CN Gel(Topical) 20gmA CN Soap 75gm' drug used for?",
        "What is 'Coralan 5mg Tablet 14'S' drug used for?",
        "What is 'Carnisurge Syrup 100ml' drug used for?",
        "What is 'Strozina 250mg Injection 4mlStrozina Syrup 60ml' drug used for?"
    ]

    # Class mapping
    class_map = {
        0: "Acne",
        1: "ADHD",
        2: "Allergies",
        3: "Alzheimer",
        4: "Amoebiasis",
        5: "Anaemia",
        6: "Angina",
    }

    # Test the fine-tuned model with each drug
    for drug in drugs:
        
        drug_name = drug.split("'")[1] if "'" in drug else drug

        prompt = f"Drug: {drug_name}\nMalady:"
        
        try:
        # Call OpenAI's API with the fine-tuned model
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )

            # Check if the response has content
            if len(response.choices) > 0:
                class_prediction = response.choices[0].message.content.strip() # type: ignore

                # Try to match the class prediction to the class map
                try:
                    predicted_class = int(class_prediction)  # Convert to integer
                    malady = class_map.get(predicted_class, "unknown class")
                    print(f"\n'{drug_name}' is used for {malady}.")
                    print(f"Predicted class: {predicted_class}")

                except ValueError:
                        print(f"Unexpected response: {class_prediction}")
            else:
                    print("No valid response from the model.")
        
        except Exception as e:
                print(f"Error for drug '{drug_name}': {e}")

# Main function to drive the fine-tuning process and testing
def main():
    input_excel_path = "Medicine_description.xlsx"  # Path to the input Excel file
    output_jsonl_path = "drug_malady_chat_data.jsonl"  # Path to save the JSONL file
    
    # Step 1: Load data from the Excel file
    df = load_data_from_excel(input_excel_path)
    if df is None:
        return  # Exit if the data loading fails
    
    # Step 2: Map maladies to unique identifiers
    reasons_dict = map_maladies_to_ids(df)
    
    # Step 3: Convert data to JSONL format
    create_chat_format(df, reasons_dict, output_jsonl_path)
    
    # Step 4: Upload the JSONL file
    training_file_id = upload_file(output_jsonl_path)
    if not training_file_id:
        return  # Exit if the file upload fails
    
    # Step 5: Start the fine-tuning job
    job_id = start_fine_tuning(training_file_id)
    if not job_id:
        return  # Exit if the fine-tuning job fails to start
    
    # Step 6: Monitor the fine-tuning job
    # model_id = monitor_and_save("ftjob-8l8wdei4AiWqJTzdpxZ4BBY2")
    model_id = monitor_and_save(job_id)
    if not model_id:
        return  # Exit if the fine-tuning job fails or is interrupted
    
    # Step 7: Test the fine-tuned model
    test_fine_tuned_model(model_id)
    
if __name__ == "__main__":
    main()
