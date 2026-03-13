#!/usr/bin/env python3
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app

print("\n" + "="*60)
print("CHECKING REPORT GENERATION")
print("="*60)

# Check file exists in both possible locations
for base in ['backend', '.']:
    report_path = os.path.join(base, 'reports', 'analysis_report.txt')
    if os.path.exists(report_path):
        size = os.path.getsize(report_path)
        print(f"\n✓ Report file exists: {report_path}")
        print(f"  File size: {size} bytes")
        with open(report_path, 'r') as f:
            content = f.read()
            print(f"  Content length: {len(content)} characters")
            print(f"  Has 'BURNOUT RISK ANALYSIS': {'BURNOUT RISK ANALYSIS' in content}")
    else:
        print(f"\n✗ Report file NOT found: {report_path}")

# Check API endpoint
print("\n" + "-"*60)
print("Testing /api/report endpoint...")
print("-"*60)

try:
    with app.test_client() as c:
        resp = c.get('/api/report')
        data = resp.json
        
        if data.get('success'):
            report_text = data.get('data', '')
            print(f"\n✓ API endpoint works!")
            print(f"  Response success: {data.get('success')}")
            print(f"  Report content length: {len(report_text)} chars")
            print(f"  Has sections: {sum(1 for i in range(1,8) if f'{i}.' in report_text)}")
        else:
            print(f"\n✗ API returned error: {data.get('error')}")
except Exception as e:
    print(f"\n✗ Error testing API: {e}")

print("\n" + "="*60 + "\n")
