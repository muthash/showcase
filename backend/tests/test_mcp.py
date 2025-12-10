from backend.agent.mcp_client import call_mcp

print("--- Test 1: List all products ---")
result2 = call_mcp({"action": "list_products"})
print(f"Result: {result2}\n")
print("-"*80)

print("--- Test 2: Search for mouse ---")
result1 = call_mcp({"action": "search_products", "query": "mouse"})
print(f"Result: {result1}\n")
print("-"*80)

print("--- Test 3: Verify customer PIN ---")
result3 = call_mcp({
	"action": "verify_customer_pin",
	"email": "donaldgarcia@example.net",
	"pin": "7912"
})
print(f"Result: {result3}\n")
print("-"*80)

print("--- Test 4: Invalid SKU ---")
result4 = call_mcp({"action": "get_product", "sku": "INVALID-SKU"})
print(f"Result: {result4}\n")
print("-"*80)

print("--- Test 5: Wrong PIN ---")
result5 = call_mcp({
	"action": "verify_customer_pin",
	"email": "donaldgarcia@example.net",
	"pin": "0000"
})
print(f"Result: {result5}\n")
print("-"*80)

print("--- Test 6: General question ---")
result6 = call_mcp("What is the warranty on monitors?")
print(f"Result: {result6}\n")
print("-"*80)