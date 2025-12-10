import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStreamableHttp


load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DEFAULT_MODEL = "gpt-4o-mini"

INSTRUCTIONS = """
You are a customer support assistant for a company that sells computer products:
monitors, printers, and accessories.

You can:
- Answer general questions about monitors, printers, and common troubleshooting.
- Use tools to look up real data from the company's systems.
- Create support tickets when issues can't be resolved in chat.

Available MCP Tools (call them when needed):

1. **search_products** - Search by keyword
   MCP_CALL: {"action": "search_products", "query": "4K monitor"}

2. **list_products** - List all products
   MCP_CALL: {"action": "list_products"}

3. **get_product** - Get product by SKU
   MCP_CALL: {"action": "get_product", "sku": "MON-0054"}

4. **verify_customer_pin** - Verify customer identity
   MCP_CALL: {"action": "verify_customer_pin", "email": "customer@email.com", "pin": "1234"}

5. **list_orders** - List customer orders (need customer_id from verification)
   MCP_CALL: {"action": "list_orders", "customer_id": "uuid-here"}

6. **get_order** - Get specific order
   MCP_CALL: {"action": "get_order", "order_id": "uuid-here"}

When you need real data, you MUST call the appropriate tool.
If data is missing, ask the user to provide it first.
Be concise, friendly, and guide the user step by step.
"""


async def company_support_agent(user_query: str, client_session_timeout_seconds: int = 60):
   if "OPENAI_API_KEY" not in os.environ:
      raise RuntimeError("OPENAI_API_KEY must be set in the environment to run the Agent SDK")

   mcp_params = {
      "url": "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp",
      "headers": {
         "Content-Type": "application/json",
         "Accept": "application/json",
      }
   }

   async with MCPServerStreamableHttp(params=mcp_params, client_session_timeout_seconds=client_session_timeout_seconds, max_retry_attempts=3) as mcp_server:
      with trace("customer_support_assistant"):
         agent = Agent(
            name="customer_support_assistant",
            instructions=INSTRUCTIONS,
            model=DEFAULT_MODEL,
            mcp_servers=[mcp_server],
         )
         result = await Runner.run(agent, user_query)
         return result.final_output



def call_mcp(action_dict, timeout=60):
   """
   Synchronous wrapper for company_support_agent for use in test scripts.
   action_dict: dict to send as the user_query (will be stringified)
   """
   import json
   user_query = json.dumps(action_dict)
   try:
      return asyncio.run(company_support_agent(user_query, client_session_timeout_seconds=timeout))
   except RuntimeError as e:
      # If already in an event loop (e.g., in Jupyter), use alternative
      try:
         import nest_asyncio
         nest_asyncio.apply()
         loop = asyncio.get_event_loop()
         return loop.run_until_complete(company_support_agent(user_query, client_session_timeout_seconds=timeout))
      except Exception as exc:
         return f"Error running async function: {exc}"
