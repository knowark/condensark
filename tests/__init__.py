import os

# Fix environment variables while testing
os.environ['INTEGRARK_DEFINITIONS_DIRECTORY'] = 'schema/definitions'
os.environ['INTEGRARK_INTEGRATIONS_DIRECTORY'] = 'schema/integrations'
