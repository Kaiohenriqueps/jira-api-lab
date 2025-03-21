from src.jira_wrapper import JiraWrapper


JIRA_URL = "https://kaiohenriqueps.atlassian.net"

wrapper = JiraWrapper(JIRA_URL)
issues = wrapper.search_issues(project="Projetos Pessoais", status="Pendente")
print(f"Found {len(issues)} issue(s)...")
attachments = wrapper.get_content_from_attachments(issues)
print(f"""Found {len(attachments)} attachment(s)...""")
print(attachments)
