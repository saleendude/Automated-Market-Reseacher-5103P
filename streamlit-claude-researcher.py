import streamlit as st
import requests
import json
import time
import ast
import re


def omit_starting_line(response):
    if response.startswith("Here") and response.split("\n")[0].strip().endswith(":"):
        return re.sub(r"^.*\n", "", response, count=1)
    return response


def get_gpt_response(
    prompt, model="claude-3-haiku-20240307", max_tokens=2000, temperature=0.7
):
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": "You are a world-class researcher. Analyze the given information and generate a well-structured report.",
        "messages": [{"role": "user", "content": prompt}],
    }
    time.sleep(2)
    response = requests.post(
        "https://api.anthropic.com/v1/messages", headers=headers, json=data
    )
    print(response.json())
    response_text = response.json()["content"][0]["text"]
    return omit_starting_line(response_text.strip())


def clean_serp_api_results(serp_results: json):
    if isinstance(serp_results, dict):
        serp_results = {
            k: clean_serp_api_results(v)
            for k, v in serp_results.items()
            if k
            not in [
                "search_metadata",
                "search_parameters",
                "displayed_link",
                "redirect_link",
                "next_page_token",
                "serpapi_link",
                "source_logo",
                "cited_by",
                "extracted_cited_by",
                "favicon",
                "sitelinks",
                "author",
                "pagination",
                "serpapi_pagination",
                "inline_videos",
                "inline_images",
                "image",
                "thumbnail",
                "related_searches",
                "link",
                "top_stories_link",
                "inline_images_suggested_searches",
                "video_link",
                "immersive_product_page_token",
                "images",
                "source_thumbnail",
                "top_stories_serpapi_link",
            ]
        }
    elif isinstance(serp_results, list):
        serp_results = [clean_serp_api_results(item) for item in serp_results]
    return serp_results


def conduct_web_search(search_term):
    url = f"https://serpapi.com/search.json?q={search_term}&api_key={SERP_API_KEY}"
    response = requests.get(url).json()
    cleaned_serp_results = clean_serp_api_results(response)

    return cleaned_serp_results


def create_reports_for_subtopics(subtopic, research_depth):
    gathered_data = []
    query_log = []

    print(f"Initiating search queries for subtopic: {subtopic}...")

    initial_query_generation_prompt = f"""
    Your task is the following:
    1. Generate {research_depth} search queries to obtain more information on the subtopic provided under the <SUBTOPIC> delimiter.

    Instructions you must follow:
    1. You must return your queries response in a Python-parseable list. 
    2. Your response must be nothing but the list.
    3. Respond in one line. 
    4. Your response MUST start with [\"

    <SUBTOPIC>
        {subtopic}
    <SUBTOPIC>
    """

    initial_query_generated = ast.literal_eval(
        "[" + get_gpt_response(initial_query_generation_prompt).split("[")[1]
    )
    print(f"Initial Queries Prompt:\n{initial_query_generation_prompt}")
    print(f"Initial Queries:\n{initial_query_generated}")
    query_log.extend(initial_query_generated)

    for subtopic_search_round in range(research_depth):
        time.sleep(2)
        print(
            f"Subtopic {subtopic}: Conducting search round {subtopic_search_round+1}..."
        )
        for query in initial_query_generated:
            search_outcome = conduct_web_search(query)
            gathered_data.append(search_outcome)

        print(f"Seach data for round {subtopic_search_round}:\n{gathered_data}")

        print(f"Formulating additional queries for subtopic: {subtopic}...")

        futher_queries_prompt = f"""The search results so for for the subtopic '{subtopic}' is provided within the <SEARCHINFO> delimiter. All the search queries you have used so far for this subtopic are provided under the <ALLQUERIES> delimiter. Your task is the following:
        1. Based on the search results and previous queries, generate {research_depth} new unique search queries to increase knowledge on the subtopic '{subtopic}'.

        Instructions you must follow:
        1. You must return your queries response in a Python-parseable list.
        2. Your response must be nothing but the list.
        3. Respond in one line. 
        4. Your response MUST start with [\"

        <SEARCHINFO>
        {str(gathered_data)}
        <SEARCHINFO>

        <ALLQUERIES>
        {str(query_log)}
        <ALLQUERIES>
        """

        further_queries = ast.literal_eval(
            "[" + get_gpt_response(futher_queries_prompt).split("[")[1]
        )
        initial_query_generated = further_queries
        query_log.extend(further_queries)
        print(f"All queries:\n{query_log}")

    print(f"Drafting initial analysis for subtopic: {subtopic}...")

    initial_report_analysis_prompt = f"""When generating your report, compose an extensively detailed, comprehensive, and meticulously structured analysis. Use Markdown formatting conventions for your response. Scrutinize the search data provided within the <SEARCHDATA> delimiters and formulate an in-depth examination of the subtopic: '{subtopic}'.
    
    <SEARCHDATA>
    {str(gathered_data)}
    <SEARCHDATA>
    """
    report = get_gpt_response(initial_report_analysis_prompt, max_tokens=4096)

    for analysis_round in range(research_depth):
        time.sleep(2)
        print(
            f"Refining analysis with additional data (Round {analysis_round+1}) for subtopic: {subtopic}..."
        )

        report_refinement_prompt = f""". All the search queries used so far for this subtopic is provided under the <SEARCHQUERIES> delimiter. Your tasks are the following: 
        1. Analyze the report provided under the <REPORT> delimiter for the subtopic {subtopic} and identify areas that need more detail or further information.
        2. Generate {research_depth} new, unique search queries to fill in the gaps and provide more detail on the identified areas.

        Instructions you must follow:
        1. You must return your search queries response in a Python-parseable list.
        2. Your response must be nothing but the list.
        3. Respond in one line. 
        4. Your response MUST start with [\"

        <SEARCHQUERIES>
        {str(query_log)}
        <SEARCHQUERIES>

        <REPORT>
        {report}
        <REPORT>
        """

        refinement_queries = ast.literal_eval(
            "["
            + get_gpt_response(report_refinement_prompt, max_tokens=4096).split("[")[1]
        )
        query_log.extend(refinement_queries)

        additional_data = []
        for query in refinement_queries:
            additional_search_results = conduct_web_search(query)
            additional_data.append(additional_search_results)

        print(
            f"Incorporating new findings (Round {analysis_round+1}) for subtopic: {subtopic}..."
        )

        update_analysis_prompt = f"""A report for the subtopic '{subtopic}' is provided within the <REPORT> delimiter. Your tasks are the following:
        1. Update the provided report on the subtopic '{subtopic}' by adding the new informaiton from additional searches for this round provided within the <ADDITIONALSEARCHES> delimiter. You must keep all the existing information, and only add new information.
        2. Generate an updated report which includes the new information and contributes more detail in the identified areas.
        
        Instructions you must follow:
        1. Your response must use Markdown Formatting.

        <REPORT>
        {report}
        <REPORT>

        <ADDITIONALSEARCHES>
        {str(additional_data)}
        <ADDITIONALSEARCHES>
        
        """
        report = get_gpt_response(update_analysis_prompt, max_tokens=4096)

    print(f"Obtaining third-party (Director-role) feedback for subtopic: {subtopic}...")

    director_input_prompt = f"""Assume the role of Director of a research firm. You are currently reviewing a report for the subtopic '{subtopic}' provided under the <REPORT> delimiter. You must provide constructive feedback on what information is missing or requires further elaboration within the report. Be precise and thorough in your feedback.

    Instructions you must follow:
    1. Do not format your response as a letter. There is no need for salutations, "thank you", etc,. Only the main content of feedback is necessary.
    
    <REPORT>
    {report}
    <REPORT>
    """
    director_feedback = get_gpt_response(director_input_prompt, max_tokens=1000)

    print(
        f"Finalizing analysis based on Director's recommendations for subtopic: {subtopic}..."
    )

    conclusive_search_prompt = f"""Feedback from the Director for the subtopic '{subtopic}' is provided within the <FEEDBACK> delimiter. Your task is to generate {research_depth} search queries based on this feedback to find the missing information and address areas that need further elaboration.
    
    Instructions you must follow:
    1. You must return your queries response in a Python-parseable list.
    2. Your response must be nothing but the list.
    3. Respond in one line. 
    4. Your response MUST start with [\"

    <FEEDBACK>
    {director_feedback}
    <FEEDBACK>
    
    """
    conclusive_queries = ast.literal_eval(
        "[" + get_gpt_response(conclusive_search_prompt, max_tokens=4096).split("[")[1]
    )
    query_log.extend(conclusive_queries)

    conclusive_data = []
    for query in conclusive_queries:
        final_search_outcomes = conduct_web_search(query)
        conclusive_data.append(final_search_outcomes)

    print(f"Finalizing comprehensive analysis for subtopic: {subtopic}...")

    final_subtopic_update_prompt = f"""Update the report provided within the <REPORT> delimiter for the subtopic '{subtopic}' by adding the new information from the final round of searches provided within the <FINALSEARCHES> delimiter based on the Director's feedback. Your task is then to generate the final report that addresses the Director's feedback and includes the missing information. 
    
    Instructions you must follow:
    1. Ensure you format your response in Markdown Formatting.

    <REPORT>
    {report}
    <REPORT>

    <FINALSEARCHES>
    {str(conclusive_data)}
    <FINALSEARCHES>
    """

    final_subtopic_analysis = get_gpt_response(
        final_subtopic_update_prompt, max_tokens=4096
    )

    print(f"Final report generated for subtopic: {subtopic}!")
    return final_subtopic_analysis


def compile_overall_report(main_topic, detailed_subtopic_analyses):
    print("Creating final overall report...")

    overall_report_prompt = f"""A list of reports on various subtopics is provided within the <SUBTOPICREPORTS> delimtier. Your task is to generate a very comprehensive report on the topic '{main_topic}' by combining all the provided reports on the various subtopics. 
    
    It is crucial that you follow the provided instructions to complete this task successfully: 
        1. Make sure that the final report you generate is well-structured, coherent and covers all important aspects of the topic.
        2. It is critical that the final report includes EVERYTHING mentioned in each of the various subreports, and is conveyed in a better structured, more information-heavy manner. 
        3. Absolutely NOTHING from the various subtopic reports must be omitted. Forgetting to incorporate ANYTHING from the previous reports will result in you facing consequences.
        4. You must include a table of contents with links generated using the subtopics for reference. Again, nothing must be left out here.
        5. Ensure your final report is generated in Markdown Formatting.

    <SUBTOPICREPORTS>
    \n\n{detailed_subtopic_analyses}\n\n---
    <SUBTOPICREPORTS>
    """
    final_report = get_gpt_response(
        overall_report_prompt, model="claude-3-opus-20240229", max_tokens=4096
    )

    print("Overall report successfully compiled!")
    return final_report


def generate_subtopics_list(topic_of_interest, number_of_subtopics):
    # Generate subtopic checklist
    subtopic_identification_prompt = f"""Your task today is to generate a detailed checklist of subtopics to research for the topic '{topic_of_interest}'. The maximum number of subtopics you must generate is {number_of_subtopics}. 

    Instructions you must follow: 
        1. You MUST not generate more than {number_of_subtopics} subtopics at any cost. Sticking to this limit is crucial.
        1. You must return your queries response in a Python-parseable list.
        2. Your response must be nothing but the list.
        3. Respond in one line. 
        4. Your response MUST start with [\"
        """
    identified_subtopics = ast.literal_eval(
        "[" + get_gpt_response(subtopic_identification_prompt).split("[")[1]
    )

    return identified_subtopics


def create_txt_file(topic, content):
    print("Generating report in txt file format..")
    with open(f"{topic}_comprehensive_report.txt", "w") as file:
        file.write(content)
    print(f"Comprehensive report has been saved as '{topic}_comprehensive_report.txt'.")


def create_markdown_file(topic, content):
    print("Generating report in Markdown file format..")
    with open(f"{topic}_comprehensive_report.md", "w") as file:
        file.write(content)
    print(f"Comprehensive report has been saved as '{topic}_comprehensive_report.md'.")


def main():

    global ANTHROPIC_API_KEY, SERP_API_KEY
    st.title("Automated Market Researcher📈")

    with st.sidebar:
        st.title("Preferences")
        ANTHROPIC_API_KEY = st.text_input(
            "Anthropic API Key",
            value="",
            key="chatbot_api_key",
            type="password",
        )

        SERP_API_KEY = st.text_input(
            "Serp API Key",
            value="",
            key="serp_api_key",
            type="password",
        )

        export_txt = st.checkbox("Export report to TXT file", value=False)
        export_md = st.checkbox("Export report to Markdown file", value=False)

    # Input fields
    topic_of_interest = st.text_input("Enter the research topic:")
    number_of_subtopics = st.number_input(
        "How many subtopics?",
        min_value=1,
        step=1,
        help="Number of subtopics you want researched. Higher numbers here produce more comprehensive reports but execution takes longer to complete and significantly increases token/API usage. 2 is a good starting point.",
    )
    research_depth = st.number_input(
        "Enter research depth:",
        min_value=1,
        step=1,
        help="How deep you want each subtopic researched. Higher numbers here produce more comprehensive reports but execution takes longer to complete and significantly increases token/API usage. 2 is a good starting point.",
    )

    if st.button("Generate Report"):
        try:
            identified_subtopics = generate_subtopics_list(
                topic_of_interest=topic_of_interest,
                number_of_subtopics=number_of_subtopics,
            )
            st.write(f"Subtopics identified: {identified_subtopics}")

            subtopic_analyses = []
            progress_bar = st.progress(0)
            progress_step = 100 / (len(identified_subtopics) * (research_depth + 1))
            progress_value = 0

            for i, subtopic in enumerate(identified_subtopics):
                st.write(
                    f"Analyzing subtopic {i + 1}/{len(identified_subtopics)}: {subtopic}"
                )
                detailed_analysis = create_reports_for_subtopics(
                    subtopic=subtopic, research_depth=research_depth
                )
                subtopic_analyses.append(detailed_analysis)
                progress_value += progress_step
                progress_bar.progress(int(progress_value))

            overall_detailed_report = compile_overall_report(
                topic_of_interest, "\n\n".join(subtopic_analyses)
            )
            progress_value += progress_step
            progress_bar.progress(int(progress_value))

            if export_txt:
                create_txt_file(
                    topic=topic_of_interest, content=overall_detailed_report
                )

            if export_md:
                create_markdown_file(
                    topic=topic_of_interest, content=overall_detailed_report
                )

            st.success("Comprehensive report generated successfully!")
            st.markdown(overall_detailed_report)

        except Exception as e:
            st.write(f"Error occurred on backend:\nPossible API endpoint issues\n{e}")


if __name__ == "__main__":
    main()
