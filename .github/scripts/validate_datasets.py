#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13,<3.14"
# ///

import argparse
import sys
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Any, Callable, List

# ==========================================
# 📐 DATA MODELS & REGISTRY
# ==========================================

@dataclass
class RuleReturn:
    status: bool
    name: str # What rule is being checked (used for error reporting)
    help: Optional[str] = None
    data: Any = None # Reserved for future serialization of complex errors

    def to_dict(self):
        return {
            "name": self.name,
            "help": self.help,
            "data": self.data
        }

# This list will automatically collect all our decorated rule functions
VALIDATION_RULES: List[Callable[[Path], RuleReturn]] = []

def rule(func: Callable[[Path], RuleReturn]) -> Callable[[Path], RuleReturn]:
    """Decorator to automatically register a validation rule."""
    VALIDATION_RULES.append(func)
    return func


# ==========================================
# 🛠️ DATASET VALIDATION RULES
# ==========================================

@rule
def check_media_dir(dataset_path: Path) -> RuleReturn:
    return RuleReturn(
        status=(dataset_path / "media").is_dir(),
        name="Directory: media",
        help="Folder containing all images, potentially organized into subdirectories."
    )

@rule
def check_raw_labels_dir(dataset_path: Path) -> RuleReturn:
    return RuleReturn(
        status=(dataset_path / "raw_labels").is_dir(),
        name="Directory: raw_labels",
        help="The original annotations in their source format (JSON, CSV, TXT, etc.)."
    )

@rule
def check_code_dir(dataset_path: Path) -> RuleReturn:
    return RuleReturn(
        status=(dataset_path / "code").is_dir(),
        name="Directory: code",
        help="Folder containing the conversion scripts (Jupyter, R, etc.) used to convert the raw data."
    )

@rule
def check_readme(dataset_path: Path) -> RuleReturn:
    return RuleReturn(
        status=(dataset_path / "README.md").is_file(),
        name="File: README.md",
        help="A readme file describing the dataset, its source, and details about the conversion."
    )

@rule
def check_deployments_csv(dataset_path: Path) -> RuleReturn:
    # Future expansion: You could open the CSV here and validate contents!
    return RuleReturn(
        status=(dataset_path / "deployments.csv").is_file(),
        name="File: deployments.csv",
        help="Generated records of camera/sensor deployments. Required for Camtrap DP."
    )

@rule
def check_media_csv(dataset_path: Path) -> RuleReturn:
    return RuleReturn(
        status=(dataset_path / "media.csv").is_file(),
        name="File: media.csv",
        help="Generated metadata for all media files. Required for Camtrap DP."
    )

@rule
def check_observations_csv(dataset_path: Path) -> RuleReturn:
    return RuleReturn(
        status=(dataset_path / "observations.csv").is_file(),
        name="File: observations.csv",
        help="Generated taxonomic or individual observations. Required for Camtrap DP."
    )

@rule
def check_datapackage_json(dataset_path: Path) -> RuleReturn:
    return RuleReturn(
        status=(dataset_path / "datapackage.json").is_file(),
        name="File: datapackage.json",
        help="The generated metadata descriptor for the data package. (See: https://tdwg.github.io/camtrap-dp/)"
    )


# ==========================================
# 🚀 CORE EXECUTION LOGIC   
# ==========================================

def get_violations(datasets_dir: str):
    base_path = Path(datasets_dir)
    if not base_path.exists() or not base_path.is_dir():
        return None, []

    violations = {}
    dataset_names = []
    
    for dataset_path in base_path.iterdir():
        if not dataset_path.is_dir():
            continue 
        
        name = dataset_path.name
        dataset_names.append(name)
        missing_items = []

        # Run every registered rule against this dataset
        for run_rule in VALIDATION_RULES:
            result = run_rule(dataset_path)
            if not result.status:
                missing_items.append(result.to_dict())

        violations[name] = missing_items
            
    return violations, dataset_names

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="datasets")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    violations, all_datasets = get_violations(args.dir)
    
    if violations is None:
        print(f"⚠️  Warning: Directory '{args.dir}' not found.", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        # Output JSON payload
        print(json.dumps({"violations": violations, "all_datasets": all_datasets}))
    else:
        for ds, issues in violations.items():
            if not issues:
                print(
                    f"✅ Dataset: {ds}\n"
                    f"   All {len(all_datasets)} datasets passed {len(VALIDATION_RULES)} validation rules.\n"
                )
                continue
            print(f"\n❌ Dataset: {ds}")
            for issue in issues:
                print(f"   - Failed: {issue['name']}")
                if issue.get("help"):
                    print(f"     💡 {issue['help']}")
            print()
    
    sys.exit(1 if any(violations.values()) else 0)

if __name__ == "__main__":
    main()