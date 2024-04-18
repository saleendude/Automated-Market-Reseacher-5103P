# Automated-Market-Reseacher-5103P
This project is built to demonstrate using Chain-Of-Thought Prompting and Google Search APIs to automate the process of market research.

## Requirements:
- [AnthropicAI Claude3-Haiku API Key](https://www.anthropic.com/api) for LLM components
- [SERP API Key](https://serpapi.com/) for automated Google Seach components


## Versions Available
- Standalone Backend Python Script: claude-researcher.py
- Backend with Streamlit Frontend: streamlit-claude-researcher.py
- Deployed Streamlit app already online: https://automated-market-researcher-5103p-2navqb7n4papp4bfznj6tah.streamlit.app/
- Google Colab Notebook: https://colab.research.google.com/drive/13HKqObLolM-EorkZIeyAskgRg2mBgt9L?usp=sharing

## Pre-requisites
It is recommended to create a new virtual environment and install all the packages provided within the requirements.txt file. Follow the steps below to create, activate and install these packages in the virtual environment.
1. Clone this repo:
```git clone git@github.com:saleendude/Automated-Market-Researcher-5103P.git```
2. Enter the repo folder:
```cd Automated-Market-Researcher/```
3. Create a new Python Virtual Environment:
```python -m venv venv```
4. Activate the new Python Virtual Environment:
If you're on Windows: ```venv\Scripts\activate```
If you're on Linux: ```. venv\bin\activate```
5. Install all the package requirements after activating the environment:
```pip install -r requirements.txt```

You are now ready to run one of the versions of this program.

## Running the standalone version:
1. In a terminal window, navigate to the directory where the ```claude-researcher.py``` file exists.
2. Open the file and enter your AnthropicAI and SERP API keys at the start of the file in the ```ANTHROPIC_API_KEY``` and ```SERP_API_KEY``` variables. Save and close the file.
3. Run the file using ```python claude-researcher.py```
4. Enter your research topic, number of subtopics required and intended research depth. Hit enter after each paramter is entered.
5. The program should start generating your report for you as long as the API keys are not rate limited and have credits in your account.
6. The reports are exported into .txt and .md files within the same directory after the program is successfully run.

## Running the Streamlit version (recommended):
1. In a terminal window, navigate to the directory where the ```streamlit-claude-researcher.py``` file exists.
2. Run ```streamlit run streamlit-claude-researcher.py```. The Streamlit server should start running on port 8501.
3. On your browser, navigate to http://localhost:8501/ to access the Streamlit frontend.
4. Enter your AnthropicAI and SERP API keys in the sidebar.
5. Enable/Disable the txt and markdown options depending on your need.
6. Enter your research topic, number of subtopics required and intended research depth. Press the Generate Report button and a loading bar should pop up showing the current subtopic being analyzed.
7. Once the program finishes execution, the final report will be visible on the same screen.
8. Depending on your export options, a report will be extracted into .txt and .md files as well.

## Running the already [deployed Streamlit app](https://automated-market-researcher-5103p-2navqb7n4papp4bfznj6tah.streamlit.app/):
1. Enter your AnthropicAI and SERP API keys in the sidebar.
2. Enable/Disable the txt and markdown options depending on your need.
3. Enter your research topic, number of subtopics required and intended research depth. Press the Generate Report button and a loading bar should pop up showing the current subtopic being analyzed.
4. Once the program finishes execution, the final report will be visible on the same screen.
5. Depending on your export options, a report will be extracted into .txt and .md files as well.

## Running the [Google Colab Notebook](https://colab.research.google.com/drive/13HKqObLolM-EorkZIeyAskgRg2mBgt9L?usp=sharing):
1. Enter your AnthropicAI and SERP API keys in the sidebar as new secret variables ANTHROPIC_API_KEY and SERP_API_KEY. Enable them before moving onto the next step.
2. Run all the cells one after the other, the necessary package installs and imports will be done automatically.
3. When prompted after running the last cell, enter your research topic, number of subtopics required, and intended research depth. 
4. Once the program finishes execution, the final report will be visible on the same screen.
5. Depending on your export options, a report will be extracted into .txt and .md files as well.

## Screenshots and videos:
![Main Page](https://github.com/saleendude/Automated-Market-Researcher-5103P/assets/35657745/99fe2b9f-aa64-4298-8aea-38e81806766f)
![Loading Report..](https://github.com/saleendude/Automated-Market-Researcher-5103P/assets/35657745/8f22f3d6-877c-49b1-80a0-4ed7ebc30d17)
![Report Generated](https://github.com/saleendude/Automated-Market-Researcher-5103P/assets/35657745/9fe2e64d-3955-453d-bfec-a5d86cae3c13)

https://github.com/saleendude/Automated-Market-Researcher-5103P/assets/35657745/ff5785ef-0b36-4097-be05-26a8e5b36fa2

