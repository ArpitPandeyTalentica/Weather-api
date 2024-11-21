import os
import yaml

# Get the absolute path to the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the directory where the YAML files are located relative to the script's directory
directory_path = os.path.join(script_dir)

# Initialize the catalog info structure
catalog_info = {
    'apiVersion': 'backstage.io/v1alpha1',
    'kind': 'Catalog',
    'metadata': {
        'name': 'weather-api-catalog'
    },
    'spec': {
        'items': []
    }
}

# Loop through all the files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".yaml"):  # Only include .yaml files
        # Construct the relative path to the file
        file_path = os.path.relpath(os.path.join(directory_path, filename), script_dir)

        # Define a new API item for each file
        catalog_info['spec']['items'].append({
            'apiVersion': 'backstage.io/v1alpha1',
            'kind': 'API',  # or 'Component', depending on your needs
            'metadata': {
                'name': f"weather-api-{filename}",
                'annotations': {
                    'github.com/project-slug': 'ArpitPandeyTalentica/Weather-api'
                }
            },
            'spec': {
                'type': 'openapi',  # Or another type if needed
                'lifecycle': 'production',
                'owner': 'arpit.pandey@talentica.com',
                'path': f'./{file_path}'  # Relative path to the file
            }
        })

# Write the generated catalog-info.yaml to a file
with open('catalog-info.yaml', 'w') as f:
    yaml.dump(catalog_info, f, default_flow_style=False)

print("catalog-info.yaml has been generated successfully.")
