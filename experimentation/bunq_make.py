from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq import ApiEnvironmentType

# Create an API context for production
api_context = ApiContext.create(
    ApiEnvironmentType.SANDBOX, # SANDBOX for testing
    "sandbox_06919d2727fb28b55df04e1b75709223783805f1aa526f2254f7299c",
    "Rohit_Laptop"
)

# Save the API context to a file for future use
api_context.save("bunq_api_context.conf")

# Load the API context into the SDK
BunqContext.load_api_context(api_context)