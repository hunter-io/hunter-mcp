from mcp.server.fastmcp import FastMCP

from hunter_mcp.client import HunterAPIClient


mcp = FastMCP("hunter-mcp")

@mcp.tool(description="Return the top 10 emails on a given domain.")
async def domain_search(domain: str) -> str:
    async with HunterAPIClient() as client:
        response = await client.get("domain-search", {"domain": domain})
        return response

@mcp.tool(description="Return the validity of a given email address.")
async def email_verifier(email: str) -> str:
    async with HunterAPIClient() as client:
        response = await client.get("email-verifier", {"email": email})
        return response

@mcp.tool(description="Return the most likely email address for a given domain and full name.")
async def email_finder(domain: str, full_name: str) -> str:
    async with HunterAPIClient() as client:
        response = await client.get("email-finder", {"domain": domain, "full_name": full_name})
        return response

@mcp.tool(description="Return all the information associated with an email address, such as a person's name, location and social handles.")
async def enrich_email(email: str) -> str:
    async with HunterAPIClient() as client:
        response = await client.get("people/find", {"email": email})
        return response

@mcp.tool(description="Return all the information associated with a domain, such as the industry, the description, or headquarters' location.")
async def enrich_company(domain: str) -> str:
    async with HunterAPIClient() as client:
        response = await client.get("companies/find", {"domain": domain})
        return response

@mcp.tool(description="Create a lead in user's account.")
async def create_lead(email: str) -> str:
    async with HunterAPIClient() as client:
        response = await client.post("leads", {"email": email})
        return response