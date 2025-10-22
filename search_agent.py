import search_tools
from pydantic_ai import Agent
from tracing import tracer


SYSTEM_PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions about documentation from the following GitHub repositories:
{repo_links}

Use the search tool to find relevant information from the course materials before answering questions.  

If you can find specific information through search, use it to provide accurate answers.

Always include references by citing the filename of the source material you used.
When creating the link, use the full path to the GitHub repository.
For example, if the filename is "path/to/file.md" from the repository "owner/repo", the link should be:
[path/to/file.md](https://github.com/owner/repo/blob/main/path/to/file.md)

If the search doesn't return relevant results, let the user know and provide general guidance.
"""

def init_agent(index, repositories):
    repo_links = "\n".join([f"- https://github.com/{owner}/{name}" for owner, name in repositories])
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(repo_links=repo_links)

    search_tool = search_tools.SearchTool(index=index)
    
    # Wrap the search tool with OpenInference tracing
    traced_search = tracer.tool(
        name="search_faq",
        description="Search the FAQ documentation index"
    )(search_tool.search)

    agent = Agent(
        name="gh_agent",
        instructions=system_prompt,
        tools=[traced_search],
        model='gpt-4o-mini'
    )

    return agent
