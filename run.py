import sys
import os
import subprocess

def run_script(script_path, extra_args=[]):
    # Set PYTHONPATH to root directory
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd() + os.pathsep + env.get("PYTHONPATH", "")
    
    python_bin = sys.executable
    if os.path.exists(".venv/bin/python"):
        python_bin = os.path.abspath(".venv/bin/python")

    cmd = [python_bin, script_path] + extra_args
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, env=env)

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py [setup|preprocess|train_ae|train_mamba|evaluate]")
        return

    task = sys.argv[1]
    scripts = {
        "setup": "scripts/setup_data.py",
        "preprocess": "scripts/preprocess_data.py",
        "train_ae": "scripts/train_ae.py",
        "train_lightgbm": "scripts/train_lightgbm.py",
        "evaluate": "scripts/evaluate.py",
        "explain": "scripts/explain_model.py",
        "importance": "scripts/extract_gene_importance.py",
        "gatk": "scripts/integrate_gatk_features.py"
    }

    if task in scripts:
        run_script(scripts[task], sys.argv[2:])
    else:
        print(f"Unknown task: {task}. Available: {', '.join(scripts.keys())}")

if __name__ == "__main__":
    main()
