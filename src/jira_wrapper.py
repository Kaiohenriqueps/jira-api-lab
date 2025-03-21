import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict
from requests.auth import HTTPBasicAuth

load_dotenv()


class JiraWrapper:
    def __init__(self, jira_url):
        self.jira_url = jira_url
        self.jira_email = os.environ["JIRA_EMAIL"]
        self.jira_token = os.environ["JIRA_TOKEN"]

    def request_jira(self, url="", params={}):
        auth = HTTPBasicAuth(self.jira_email, self.jira_token)
        headers = {"Accept": "application/json"}
        response = requests.request(
            "GET", url, headers=headers, params=params, auth=auth
        )
        return response

    def search_issues(self, project: str, status: str):
        search_url = f"{self.jira_url}/rest/api/2/search"
        query = {
            "fields": "*all",
            "jql": f"project = '{project}' AND status = '{status}'",
        }

        result = json.loads(self.request_jira(search_url, query).text)
        return result["issues"]

    def get_attachments(self, issues: List[Dict]):
        attachments = []
        for issue in issues:
            for attachment in issue["fields"]["attachment"]:
                attachments.append(attachment)
        return attachments

    def download_content(self, attachment: Dict, attachment_data: List):
        attachment_url = attachment["content"]
        attachment_name = attachment["filename"]

        # Download attachment
        response = self.request_jira(attachment_url, {})
        if response.status_code == 200:
            attachment_data.append(
                {
                    "filename": attachment_name,
                    "content": response.content,
                }
            )
        return attachment_data

    def get_content_from_attachments(self, issues: List[Dict]):
        attachments = self.get_attachments(issues)

        attachment_data = []
        for attachment in attachments:
            self.download_content(attachment, attachment_data)

        return attachment_data
