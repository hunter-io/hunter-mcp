import unittest
import json
from unittest.mock import AsyncMock, patch

import main


class ToolCompatibilityTests(unittest.IsolatedAsyncioTestCase):
    async def test_registered_tools_return_hunter_json(self):
        cases = (
            ("domain_search", {"domain": "example.com"}, "get", "domain-search"),
            ("email_verifier", {"email": "a@example.com"}, "get", "email-verifier"),
            ("email_finder", {"domain": "example.com", "full_name": "A B"}, "get", "email-finder"),
            ("enrich_email", {"email": "a@example.com"}, "get", "people/find"),
            ("enrich_company", {"domain": "example.com"}, "get", "companies/find"),
            ("create_lead", {"email": "a@example.com"}, "post", "leads"),
        )

        self.assertEqual({case[0] for case in cases}, {tool.name for tool in main.mcp._tool_manager.list_tools()})
        for name, arguments, method, endpoint in cases:
            with self.subTest(name=name):
                client = AsyncMock()
                client.__aenter__.return_value = client
                getattr(client, method).return_value = {"data": {"ok": True}}
                with patch.object(main, "HunterAPIClient", return_value=client):
                    result = await main.mcp.call_tool(name, arguments)
                content, structured = result
                self.assertEqual(structured, {"data": {"ok": True}})
                self.assertEqual(json.loads(content[0].text), structured)
                getattr(client, method).assert_awaited_once_with(endpoint, arguments)
