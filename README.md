#### Introduction
The Research Report Generation System is a cutting-edge tool designed to assist users in generating comprehensive research reports based on various data sources. The system integrates large language models (LLMs), web search engines, and advanced frameworks such as LangChain and Langraph to automate the process of information gathering, synthesis, and report generation.

The system operates on a three-node agent framework that consists of:

- LLM Query Node: Interacts with large language models to gather responses based on a user’s query.

- Web Search Node (Tavily): Uses the Tavily search tool to fetch the most up-to-date and relevant information from the web.

- Combiner Node: Combines the LLM-generated content with the results from the web search, delivering a cohesive and informative report.

This report delves into the architecture and detailed working of the system, focusing on the integration of LangChain and Langraph frameworks to streamline data processing and ensure high-quality output.

#### System Workflow
The workflow of the Research Report Generation System can be summarized as follows:

- User Query Input: The user enters a query or research topic they need information on. The query is sent to both the LLM Query Node and Tavily Web Search Node in parallel.

- LLM Response: The LLM processes the query and returns an initial response based on its pre-trained knowledge.

- Web Search (Tavily): Simultaneously, Tavily searches the web for relevant, up-to-date information and returns the most relevant results.

- Data Integration: The Combiner Node receives both the LLM response and the Tavily search results. It synthesizes the information and generates a comprehensive report that addresses the user’s query in full.

- Final Report Generation: The system outputs a detailed research report that combines the LLM’s knowledge with the most current information from the web, offering the user a well-rounded, informative response.


#### Instructions to use.

- Python 3.12 or higher
- API keys for:
  - OpenAI, Anthropic, Google AI 
  - Tavily (Mandatory)
- clone the github repo.

- Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
TAVILY_API_KEY=your_tavily_key (madantory)
```
(Note: Currently this project uses lamma2 so it does not require any key)

- Run the agent.ipynb notebook to test for different queries.
