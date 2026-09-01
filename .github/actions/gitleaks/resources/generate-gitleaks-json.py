#!/usr/bin/env python3

import json
import argparse
import sys
from pathlib import Path


def generate_gitleaks_json(sarif_file, output_file):
    """
    Convert Gitleaks SARIF findings to a simplified JSON format.
    
    Args:
        sarif_file: Path to the SARIF file
        output_file: Path to write the JSON output
    """
    try:
        with open(sarif_file, 'r') as f:
            sarif_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading SARIF file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Extract findings from SARIF
    findings = []
    
    if 'runs' in sarif_data:
        for run in sarif_data['runs']:
            if 'results' in run:
                for result in run['results']:
                    finding = {
                        'message': result.get('message', {}).get('text', 'N/A'),
                        'ruleId': result.get('ruleId', 'N/A'),
                        'level': result.get('level', 'unknown'),
                        'locations': result.get('locations', [])
                    }
                    findings.append(finding)
    
    # Create output JSON structure
    output_json = {
        'tool': 'gitleaks',
        'summary': {
            'total': len(findings),
            'by_level': {
                'error': sum(1 for f in findings if f['level'] == 'error'),
                'warning': sum(1 for f in findings if f['level'] == 'warning'),
                'note': sum(1 for f in findings if f['level'] == 'note'),
                'none': sum(1 for f in findings if f['level'] == 'none')
            }
        },
        'findings': findings
    }
    
    # Write output
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(output_json, f, indent=2)
        
        print(f"Gitleaks JSON report generated: {output_file}")
        print(f"Total findings: {len(findings)}")
        
    except Exception as e:
        print(f"Error writing JSON file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert Gitleaks SARIF findings to JSON format'
    )
    parser.add_argument(
        '--sarif',
        required=True,
        help='Path to the SARIF file'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Path to write the JSON output'
    )
    
    args = parser.parse_args()
    
    generate_gitleaks_json(args.sarif, args.output)


if __name__ == '__main__':
    main()