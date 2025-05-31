#!/usr/bin/env python3

"""
Quick demo of the most important filter tests
Runs a subset of tests to showcase functionality without taking too long
"""

from test_all_filters import run_test

def quick_demo():
    """Run key tests to demonstrate functionality"""
    print("🏒 NHL PROSPECTS QUICK TEST DEMO 🏒")
    print("Running key filter tests...")
    
    # Key tests to demonstrate
    demo_tests = [
        ("Help Menu", "-H", "Display help information"),
        ("All Goalies", "-POS G", "Position filter for goalies"),
        ("All Centers", "-POS C", "Position filter for centers"),
        ("USA Players", "-CODES \"USA\"", "Country filter for USA"),
        ("Left-handed Players", "-HAND \"L\"", "Hand/shoots filter"),
        ("Young Players", "-AGE \"20\"", "Age filter (20 and under)"),
        ("Tall Players", "+HEIGHT \"6'4\"", "Height filter (6'4\" and over)"),
        ("USA Goalies", "-POS G -CODES \"USA\"", "Combined filters"),
        ("Specific Player", "-ID \"8479361\"", "Individual player lookup"),
        ("Draft Eligible", "-ELIG", "Draft eligibility filter"),
    ]
    
    results = []
    
    for name, query, description in demo_tests:
        print(f"\n{'='*50}")
        print(f"🔍 {name}: {description}")
        success, count = run_test(name, query)
        results.append((name, success, count))
        
        # Add small delay to be nice to the API
        import time
        time.sleep(0.5)
    
    # Summary
    print(f"\n\n{'='*60}")
    print("📊 QUICK DEMO SUMMARY")
    print(f"{'='*60}")
    
    passed = failed = 0
    for name, success, count in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {name}: {count} players")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n🎯 Quick Demo Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All key filters are working correctly!")
    else:
        print("⚠️  Some filters may need attention")

if __name__ == "__main__":
    quick_demo() 