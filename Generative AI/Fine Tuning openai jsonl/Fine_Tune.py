import openai, csv, os
import time, json
from dotenv import load_dotenv, find_dotenv

# Load environment variables for OpenAI API
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to convert JSON to JSONL format
def json_to_jsonl(input_json_path, output_jsonl_path):
    """
    Converts a JSON file to JSONL format by writing each object in the JSON array to a new line in the output JSONL file.
    """
    try:
        # Open and load the JSON file
        with open(input_json_path, 'r') as json_file:
            data = json.load(json_file)

        # Write the data to the jsonl file, each item on a new line
        with open(output_jsonl_path, 'w') as jsonl_file:
            for item in data:
                jsonl_file.write(json.dumps(item) + '\n')
        
        print(f"Conversion successful! {input_json_path} has been converted to {output_jsonl_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")

# Example usage of the conversion function
input_json_path = "data.json"  # Path to your input JSON file
output_jsonl_path = "data_prepared.jsonl"  # Path to save the output JSONL file
json_to_jsonl(input_json_path, output_jsonl_path)

# Function to upload the training file to OpenAI
def upload_file(file_path):
    """
    Uploads the training file to OpenAI's server for fine-tuning.
    Returns the file ID if the upload is successful, else returns None.
    """
    try:
        response = openai.files.create(file=open(file_path, "rb"), purpose="fine-tune")
        print(f"File uploaded: {response.id}")
        return response.id
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

# Function to start the fine-tuning job
def start_fine_tuning(training_file_id, model="gpt-3.5-turbo-1106"):
    """
    Starts a fine-tuning job with the specified training file ID and model.
    Returns the job ID if the job starts successfully, else returns None.
    """
    try:
        response = openai.fine_tuning.jobs.create(
            training_file=training_file_id,
            model=model,
            suffix="Vaishnavi Model"  # Adding the suffix directly in the fine-tuning job
        )
        print(f"Fine-tuning job started: {response.id}")
        return response.id
    except Exception as e:
        print(f"Error starting fine-tuning: {e}")
        return None

# Function to monitor the fine-tuning job and save metrics to a CSV file
def monitor_and_save(job_id, output_csv):
    """
    Monitors the fine-tuning job's status. Once the job is completed, 
    it saves the metrics (like loss and accuracy) to a CSV file.
    """
    try:
        while True:
            job_status = openai.fine_tuning.jobs.retrieve(job_id)
            # Check the job's status
            if job_status.status == 'succeeded':
                print("Fine-tuning completed successfully!")
                events = openai.fine_tuning.jobs.list_events(job_id)
                save_metrics_to_csv(events, output_csv)  # Save metrics to CSV
                break
            elif job_status.status == 'failed':
                print("Fine-tuning failed!")
                break
            else:
                print(f"Fine-tuning in progress... (status: {job_status.status})")
                time.sleep(60)  # Wait for 60 seconds before checking again
    except Exception as e:
        print(f"Error monitoring job: {e}")

# Function to save metrics to a CSV file
def save_metrics_to_csv(events, output_csv):
    """
    Saves the fine-tuning job's metrics (like training loss, sequence accuracy, token accuracy) to a CSV file.
    """
    try:
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write CSV header
            writer.writerow(["step", "train_loss", "total_steps", "train_mean_token_accuracy"])
            
            # Iterate through the events and extract metrics
            for event in events:
                if event.type == 'metrics':  # Only process metric events
                    metrics = event.data  # Extract metric data
                    writer.writerow([
                        metrics.get('step', 'N/A'),
                        metrics.get('train_loss', 'N/A'),
                        metrics.get('total_steps', 'N/A'),
                        metrics.get('train_mean_token_accuracy', 'N/A')
                    ])
        print(f"Metrics successfully saved to {output_csv}")
    except Exception as e:
        print(f"Error saving metrics to CSV: {e}")

# Main function to drive the fine-tuning process
def main():
    file_path = "data_prepared.jsonl"  # Path to your dataset (converted to JSONL format)
    output_csv = "fine_tuning_metrics.csv"  # Output CSV file for metrics
    
    # Step 1: Upload the training file
    training_file_id = upload_file(file_path)
    if not training_file_id:
        return  # Exit if the file upload fails
    
    # Step 2: Start the fine-tuning job
    job_id = start_fine_tuning(training_file_id)
    if not job_id:
        return  # Exit if the fine-tuning job fails to start
    
    # Step 3: Monitor the fine-tuning job and save metrics to CSV
    monitor_and_save(job_id, output_csv)

# Execute the main function
if __name__ == "__main__":
    main()