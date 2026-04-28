import os
import re

agent_dir = r'c:\Users\AlexJ\Documents\Coding\Repos\openfang-repos\openfang\agents'
for root, dirs, files in os.walk(agent_dir):
    for file in files:
        if file == 'agent.toml':
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find [model] and [[fallback_models]] sections
            sections = re.split(r'(?=\[model\]|\[\[fallback_models\]\]|\[resources\]|\[capabilities\]|\[autonomous\])', content)
            
            new_content = ''
            for sec in sections:
                if sec.startswith('[model]') or sec.startswith('[[fallback_models]]'):
                    # Check if provider = "openrouter"
                    if 'provider = "openrouter"' in sec:
                        # Replace api_key_env if it exists
                        if 'api_key_env' in sec:
                            sec = re.sub(r'api_key_env\s*=\s*".*?"', 'api_key_env = "OPENROUTER_API_KEY"', sec)
                        else:
                            # Insert api_key_env after model
                            sec = re.sub(r'(model\s*=\s*".*?")', r'\1\napi_key_env = "OPENROUTER_API_KEY"', sec)
                new_content += sec
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Fixed {path}')
