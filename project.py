import os

# Updated root project folder name
ROOT_FOLDER = "EDA_Assistant"

structure = {
    ROOT_FOLDER: [
        "app.py",
        "requirements.txt",
        "README.md",
        {
            "src": [
                "__init__.py",
                {
                    "pipeline": [
                        "__init__.py",
                        "profiler.py",
                        "cleaner.py",
                        "report_builder.py"
                    ]
                },
                {
                    "agents": [
                        "__init__.py",
                        "langgraph_workflow.py",
                        "chat_memory.py",
                        "nlp_intent_parser.py",
                        "response_generator.py"
                    ]
                },
                {
                    "tools": [
                        "__init__.py",
                        "chart_generator.py",
                        "pdf_generator.py",
                        "utils.py"
                    ]
                },
                {
                    "ui": [
                        "__init__.py",
                        "layout.py",
                        "styles.css"
                    ]
                },
                {
                    "data": [
                        "sample_dataset.csv",
                        {
                            "temp": []
                        }
                    ]
                }
            ]
        },
        {
            "checkpoints": []
        },
        {
            "exports": [
                {
                    "reports": []
                },
                {
                    "cleaned": []
                }
            ]
        }
    ]
}

def create_structure(base_path, struct):
    for folder, items in struct.items():
        root = os.path.join(base_path, folder)
        os.makedirs(root, exist_ok=True)

        for item in items:
            if isinstance(item, str):
                file_path = os.path.join(root, item)
                open(file_path, 'w').close()
            elif isinstance(item, dict):
                create_structure(root, item)

if __name__ == "__main__":
    base_dir = os.getcwd()
    create_structure(base_dir, structure)
    print(f"📁 Project '{ROOT_FOLDER}' structure created successfully!")
