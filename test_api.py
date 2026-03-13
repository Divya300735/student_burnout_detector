#!/usr/bin/env python3
"""Test script to verify the API endpoints are working."""

import requests
import json
import time
import sys

# Give server time to start
time.sleep(2)

BASE_URL = "http://localhost:5000"

def test_api():
    """Test all API endpoints."""
    tests_passed = 0
    tests_failed = 0
    
    print("=" * 60)
    print("Testing Academic Burnout Detection API")
    print("=" * 60)
    
    # Test 1: Dataset Summary
    print("\n[1] Testing /api/dataset_summary...")
    try:
        response = requests.get(f"{BASE_URL}/api/dataset_summary")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("    ✓ Dataset summary retrieved successfully")
                print(f"      Total students: {data['data']['total_students']}")
                tests_passed += 1
            else:
                print("    ✗ Failed to retrieve dataset summary")
                tests_failed += 1
        else:
            print(f"    ✗ HTTP {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"    ✗ Error: {e}")
        tests_failed += 1
    
    # Test 2: Statistics
    print("\n[2] Testing /api/statistics...")
    try:
        response = requests.get(f"{BASE_URL}/api/statistics")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("    ✓ Statistics retrieved successfully")
                stats = data['data']
                print(f"      Variables analyzed: {len(stats)}")
                tests_passed += 1
            else:
                print("    ✗ Failed to retrieve statistics")
                tests_failed += 1
        else:
            print(f"    ✗ HTTP {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"    ✗ Error: {e}")
        tests_failed += 1
    
    # Test 3: Correlation
    print("\n[3] Testing /api/correlation...")
    try:
        response = requests.get(f"{BASE_URL}/api/correlation")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("    ✓ Correlation matrix retrieved successfully")
                indicators = data['data'].get('burnout_indicators', {})
                print(f"      Burnout indicators identified: {len(indicators)}")
                tests_passed += 1
            else:
                print("    ✗ Failed to retrieve correlation data")
                tests_failed += 1
        else:
            print(f"    ✗ HTTP {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"    ✗ Error: {e}")
        tests_failed += 1
    
    # Test 4: Regression
    print("\n[4] Testing /api/regression...")
    try:
        response = requests.get(f"{BASE_URL}/api/regression")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("    ✓ Regression model retrieved successfully")
                print(f"      R² value: {data['data']['r_squared']:.4f}")
                tests_passed += 1
            else:
                print("    ✗ Failed to retrieve regression data")
                tests_failed += 1
        else:
            print(f"    ✗ HTTP {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"    ✗ Error: {e}")
        tests_failed += 1
    
    # Test 5: Graphs
    print("\n[5] Testing /api/graphs...")
    try:
        response = requests.get(f"{BASE_URL}/api/graphs")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("    ✓ Graph list retrieved successfully")
                total_graphs = sum(len(v) for v in data['data'].values())
                print(f"      Total graphs generated: {total_graphs}")
                tests_passed += 1
            else:
                print("    ✗ Failed to retrieve graph list")
                tests_failed += 1
        else:
            print(f"    ✗ HTTP {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"    ✗ Error: {e}")
        tests_failed += 1

    # Test 5a: Dataset Graphs including risk analysis
    print("\n[5a] Testing /api/dataset_graphs for risk_analysis...")
    try:
        response = requests.get(f"{BASE_URL}/api/dataset_graphs")
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'risk_analysis' in data['data']:
                print("    ✓ Risk analysis graphs listed")
                risk_list = data['data']['risk_analysis']
                print(f"      Risk graphs count: {len(risk_list)}")
                tests_passed += 1
            else:
                print("    ✗ Risk analysis section missing in dataset graphs")
                tests_failed += 1
        else:
            print(f"    ✗ HTTP {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"    ✗ Error: {e}")
        tests_failed += 1
    
    # Test 6: Burnout Prediction
    print("\n[6] Testing /api/burnout_predict...")
    try:
        payload = {
            "sleep_hours": 6.5,
            "study_hours": 5.5,
            "screen_time": 7.0,
            "stress_level": 5.5,
            "physical_activity": 4.0,
            "assignment_load": 5.0
        }
        response = requests.post(f"{BASE_URL}/api/burnout_predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("    ✓ Burnout prediction successful")
                result = data['data']
                print(f"      Burnout Score: {result['burnout_score']}/10")
                print(f"      Risk Category: {result['risk_category']}")
                print(f"      Probability: {result['burnout_probability']}%")
                tests_passed += 1
            else:
                print("    ✗ Failed to predict burnout")
                tests_failed += 1
        else:
            print(f"    ✗ HTTP {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"    ✗ Error: {e}")
        tests_failed += 1
    
    # Test 7: Report
    print("\n[7] Testing /api/report...")
    try:
        response = requests.get(f"{BASE_URL}/api/report")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                report = data['data']
                # look for the project title as a simple sanity check
        if "Early Statistical Detection" in report:
                    print("    ✓ Report retrieved successfully")
                    print(f"      Report size: {len(report)} characters")
                    tests_passed += 1
                else:
                    print("    ✗ Report format invalid")
                    tests_failed += 1
            else:
                print("    ✗ Failed to retrieve report")
                tests_failed += 1
        else:
            print(f"    ✗ HTTP {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"    ✗ Error: {e}")
        tests_failed += 1
    
    # Test 8: Home page
    print("\n[8] Testing home page (/)...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            if "Academic Burnout Detection" in response.text:
                print("    ✓ Home page loaded successfully")
                tests_passed += 1
            else:
                print("    ✗ Home page content invalid")
                tests_failed += 1
        else:
            print(f"    ✗ HTTP {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"    ✗ Error: {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print(f"Total Tests:  {tests_passed + tests_failed}")
    print("=" * 60)
    
    if tests_failed == 0:
        print("\n✓ All tests passed! The application is working correctly.")
        return True
    else:
        print(f"\n✗ {tests_failed} test(s) failed.")
        return False

if __name__ == "__main__":
    try:
        success = test_api()
        sys.exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Cannot connect to server at {BASE_URL}")
        print("Make sure the Flask app is running on localhost:5000")
        sys.exit(1)
