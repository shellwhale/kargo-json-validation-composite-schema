import json
import requests

# Mapping of schema URLs to their expected "kind" values.
schema_mapping = {
    "https://raw.githubusercontent.com/akuity/kargo/refs/heads/main/ui/src/gen/schema/clusterpromotiontasks.kargo.akuity.io_v1alpha1.json": "ClusterPromotionTask",
    "https://raw.githubusercontent.com/akuity/kargo/refs/heads/main/ui/src/gen/schema/freights.kargo.akuity.io_v1alpha1.json": "Freight",
    "https://raw.githubusercontent.com/akuity/kargo/refs/heads/main/ui/src/gen/schema/projects.kargo.akuity.io_v1alpha1.json": "Project",
    "https://raw.githubusercontent.com/akuity/kargo/refs/heads/main/ui/src/gen/schema/promotions.kargo.akuity.io_v1alpha1.json": "Promotion",
    "https://raw.githubusercontent.com/akuity/kargo/refs/heads/main/ui/src/gen/schema/promotiontasks.kargo.akuity.io_v1alpha1.json": "PromotionTask",
    "https://raw.githubusercontent.com/akuity/kargo/refs/heads/main/ui/src/gen/schema/stages.kargo.akuity.io_v1alpha1.json": "Stage",
    "https://raw.githubusercontent.com/akuity/kargo/refs/heads/main/ui/src/gen/schema/warehouses.kargo.akuity.io_v1alpha1.json": "Warehouse"
}

wrapped_schemas = []

for url, kind in schema_mapping.items():
    print(f"Fetching schema from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        schema = response.json()
        # Remove the top-level $schema property if present.
        schema.pop("$schema", None)
        # Wrap the schema with an if/then/else block.
        wrapped = {
            "if": {
                "properties": {
                    "kind": {"const": kind}
                },
                "required": ["kind"]
            },
            "then": schema,
            "else": { "not": {} }  # Fails validation if the if condition is not met.
        }
        wrapped_schemas.append(wrapped)
    else:
        print(f"Failed to fetch schema from {url}")

# Create the composite schema that uses oneOf to validate against any of the wrapped schemas.
composite_schema = {
    "oneOf": wrapped_schemas
}

# Output the composite schema to a file.
with open("composite-schema.json", "w") as f:
    json.dump(composite_schema, f, indent=2)

print("Composite schema created as composite-schema.json")
