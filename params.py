# This module defines configuration parameters for the Speech enabled AI Assistant application.

# Application title
app_title = "Speech enabled AI Assistant"

# File containing system prompts
sys_prompt_file = "metaprompt-1.txt"

# Azure Cognitive Services Speech Service configuration
speech_key = ""  # Speech service subscription key
service_region = "westeurope"  # Azure service region for the Speech service
neural_voice_name = "en-US-AvaMultilingualNeural"  # Name of the neural voice to use

# Azure OpenAI Service configuration
aoai_base_url = "https://xxxxxxxx.openai.azure.com/"  # Base URL for the Azure OpenAI Service
aoai_key = ""  # Subscription key for the Azure OpenAI Service
aoai_version = "2024-05-01-preview"  # API version to use for the Azure OpenAI Service
deployment_name = "gpt-4o"  # Name of the deployment for the Azure OpenAI Service

# Azure Cognitive Search configuration
ai_search_url = "https://xxxxxx.search.windows.net"  # Base URL for the Azure Cognitive Search service
ai_search_key = ""  # Subscription key for the Azure Cognitive Search service

# Configuration for the Car Loan SOP (Standard Operating Procedure) Index
car_loan_index_name = "car-loan-sop-abcbank-index"  # Name of the index for car loan SOP
car_loan_ai_semantic_config = "car-loans-abcbank-config"  # Semantic configuration for car loan SOP
car_loan_query_type = "semantic"  # Query type for car loan SOP
car_loan_prompt_assist_file_name = "car_loan_assist.txt"  # File containing prompts for car loan SOP assistance

# Configuration for the SOW (Statement of Work) Data Index
sow_index_name = "ites-sow-vector-index"  # Name of the index for SOW data
sow_ai_semantic_config = "ites-sow-vector-index-semantic-configuration"  # Semantic configuration for SOW data
sow_query_type = "semantic"  # Query type for SOW data
sow_prompt_file_name = "sow_helper.txt"  # File containing prompts for SOW assistance

# Configuration for the Edu Docs (Educational Documents) Assistant Index
edu_index_name = "vector-edu-docs-idx"  # Name of the index for educational documents
edu_ai_semantic_config = "vector-edu-docs-idx-semantic-configuration"  # Semantic configuration for educational documents
edu_query_type = "semantic"  # Query type for educational documents
edu_prompt_file_name = "edu_assist.txt"  # File containing prompts for educational documents assistance
