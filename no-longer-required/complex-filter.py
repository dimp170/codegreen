import os
import radon.complexity as cc
from radon.visitors import ComplexityVisitor

DATASET_DIR = "../cleaned_python_dataset"
TOP_COMPLEX_FILES = 10  # Keep the 10 most complex files
OUTPUT_DIR = "../mostest_complex_python"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_cyclomatic_complexity(file_path):
    """Calculate Cyclomatic Complexity of a Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            visitor = ComplexityVisitor.from_code(code)
            return sum(block.complexity for block in visitor.functions + visitor.classes)
    except Exception as e:
        print(f"⚠️ Error analyzing {file_path}: {e}")
        return 0


# ✅ Analyze complexity of all Python files
file_complexity = []
for file_name in os.listdir(DATASET_DIR):
    file_path = os.path.join(DATASET_DIR, file_name)

    # Get complexity score
    complexity_score = get_cyclomatic_complexity(file_path)

    if complexity_score > 0:
        file_complexity.append((file_name, complexity_score))

# ✅ Sort files by complexity (highest first)
file_complexity.sort(key=lambda x: x[1], reverse=True)

# ✅ Keep only the top 10 most complex files
top_complex_files = file_complexity[:TOP_COMPLEX_FILES]

# ✅ Move selected files to a new folder
for file_name, complexity in top_complex_files:
    old_path = os.path.join(DATASET_DIR, file_name)
    new_path = os.path.join(OUTPUT_DIR, file_name)
    os.rename(old_path, new_path)
    print(f"✅ Kept: {file_name} (Complexity: {complexity})")

print(f"✅ Top {TOP_COMPLEX_FILES} complex Python scripts saved in '{OUTPUT_DIR}'.")



