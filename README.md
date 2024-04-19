# Financial News Sentiment Analysis

## Introduction
This project focuses on sentiment analysis for financial news using a pre-trained language model. It involves downloading a dataset from Kaggle, setting up the dataset, fine-tuning a language model, and using it for sentiment analysis. This README provides step-by-step instructions to set up and run the project.

## Steps to Setup and Run the Project

1. **Download Dataset from Kaggle**
   - Download the dataset from [Kaggle](https://www.kaggle.com/datasets/ankurzing/sentiment-analysis-for-financial-news).

2. **Unzip Dataset and Copy Data Files**
   - Unzip the downloaded dataset file.
   - Copy all_data file from the unzipped folder.

3. **Create Dataset Folder**
   - Create a new folder named `dataset` in the project directory.

4. **Paste Data Files**
   - Paste the copied data file into the `dataset` folder.

5. **Run Fine-tuning Notebook**
   - Open and run the `fine-tuning-sentiment.ipynb` file.
   - This notebook will fine-tune the language model using the financial news dataset.
   - After execution, it will create the necessary files in the `models` folder.

6. **Run `main.py`**
   - After fine-tuning the language model, you can run the `main.py` file.
   - This script utilizes the fine-tuned model to perform sentiment analysis on financial news.
   - Ensure that the `models` folder contains the required files generated during fine-tuning.

7. **Review Results**
   - After running `main.py`, review the sentiment analysis results produced by the model.

## Additional Notes
- Make sure you have all the required libraries installed, as specified in the `requirements.txt` file.
- Ensure you have sufficient computing resources to run the fine-tuning process, as it may be resource-intensive.
- Feel free to customize the project according to your needs, such as adjusting hyperparameters or using different language models.

By following these steps, you'll be able to set up and run the financial news sentiment analysis project successfully. If you encounter any issues or have questions, refer to the documentation or reach out for assistance. Happy analyzing!
