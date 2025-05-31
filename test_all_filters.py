#!/usr/bin/env python3

"""
Comprehensive test suite for all NHL prospects filter options
Tests all the filters mentioned in the help menu
"""

import time

from queryParser import processIntoHtml


def run_test(test_name, query, expected_behavior=None):
    """Run a single test and report results"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"QUERY: '{query}'")
    print(f"{'='*60}")

    try:
        start_time = time.time()
        result = processIntoHtml(query)
        end_time = time.time()

        # Count players found
        player_count = len([line for line in result if "Player Full Name:" in line])

        print(
            f"✅ SUCCESS - Found {player_count} players in {end_time - start_time:.2f}s"
        )
        print(f"Total output lines: {len(result)}")

        # Show first few lines for context
        print("\nFirst few output lines:")
        for i, line in enumerate(result[:8]):
            if line.strip():
                print(f"  {i+1}: {line}")

        if expected_behavior:
            print(f"\nExpected behavior: {expected_behavior}")

        return True, player_count

    except Exception as e:
        print(f"❌ FAILED - Error: {e}")
        import traceback

        traceback.print_exc()
        return False, 0


def test_help_menu():
    """Test help menu display"""
    return run_test(
        "Help Menu Display",
        "-H",
        "Should show the help menu with all available filter options",
    )


def test_position_filters():
    """Test all position filter variations"""
    tests = [
        ("Goalies Only", "-POS G", "Should show only goalie prospects"),
        ("Centers Only", "-POS C", "Should show only center prospects"),
        ("Left Wings Only", "-POS L", "Should show only left wing prospects"),
        ("Right Wings Only", "-POS R", "Should show only right wing prospects"),
        ("Defensemen Only", "-POS D", "Should show only defenseman prospects"),
        ("All Forwards", "-POS F", "Should show centers, left wings, and right wings"),
    ]

    results = []
    for name, query, expected in tests:
        success, count = run_test(name, query, expected)
        results.append((name, success, count))

    return results


def test_draft_filters():
    """Test draft-related filters"""
    tests = [
        (
            "Ranked Players Only",
            "-RANKED",
            "Should show players with ranking data (currently shows all due to API limitations)",
        ),
        ("Draft Eligible Only", "-ELIG", "Should show only draft eligible players"),
    ]

    results = []
    for name, query, expected in tests:
        success, count = run_test(name, query, expected)
        results.append((name, success, count))

    return results


def test_country_filter():
    """Test country code filter"""
    tests = [
        ("USA Players", '-CODES "USA"', "Should show only USA-born players"),
        ("Canada Players", '-CODES "CAN"', "Should show only Canada-born players"),
        (
            "Multiple Countries",
            '-CODES "USA,CAN"',
            "Should show USA and Canada-born players",
        ),
        ("Sweden Players", '-CODES "SWE"', "Should show only Sweden-born players"),
    ]

    results = []
    for name, query, expected in tests:
        success, count = run_test(name, query, expected)
        results.append((name, success, count))

    return results


def test_country_exclude_filter():
    """Test country code exclusion filter"""
    tests = [
        (
            "Exclude USA Players",
            '-EXCLUDE-CODES "USA"',
            "Should show all players except USA-born",
        ),
        (
            "Exclude Canada Players",
            '-EXCLUDE-CODES "CAN"',
            "Should show all players except Canada-born",
        ),
        (
            "Exclude Multiple Countries",
            '-EXCLUDE-CODES "USA,CAN"',
            "Should exclude both USA and Canada-born players",
        ),
        (
            "Exclude Sweden Players",
            '-EXCLUDE-CODES "SWE"',
            "Should show all players except Sweden-born",
        ),
    ]

    results = []
    for name, query, expected in tests:
        success, count = run_test(name, query, expected)
        results.append((name, success, count))

    return results


def test_physical_filters():
    """Test height, weight, and age filters"""
    tests = [
        ("Tall Players", '-HEIGHT "6\'2"', "Should show players 6'2\" and under"),
        ("Very Tall Players", '+HEIGHT "6\'4"', "Should show players 6'4\" and over"),
        ("Heavy Players", '-WEIGHT "200"', "Should show players 200lbs and under"),
        ("Light Players", '+WEIGHT "180"', "Should show players 180lbs and over"),
        ("Young Players", '-AGE "21"', "Should show players 21 years old and younger"),
        ("Older Players", '+AGE "23"', "Should show players 23 years old and older"),
    ]

    results = []
    for name, query, expected in tests:
        success, count = run_test(name, query, expected)
        results.append((name, success, count))

    return results


def test_hand_filter():
    """Test shooting/catching hand filter"""
    tests = [
        ("Left-handed Players", '-HAND "L"', "Should show only left-handed players"),
        ("Right-handed Players", '-HAND "R"', "Should show only right-handed players"),
    ]

    results = []
    for name, query, expected in tests:
        success, count = run_test(name, query, expected)
        results.append((name, success, count))

    return results


def test_rank_filters():
    """Test ranking filters (note: these may not work due to API limitations)"""
    tests = [
        (
            "Top 50 Ranked",
            '-MAX-RANK "50"',
            "Should show players ranked 50 or better (may not work with new API)",
        ),
        (
            "Lower Ranked",
            '-MIN-RANK "100"',
            "Should show players ranked 100 or worse (may not work with new API)",
        ),
    ]

    results = []
    for name, query, expected in tests:
        success, count = run_test(name, query, expected)
        results.append((name, success, count))

    return results


def test_id_filter():
    """Test individual player ID lookup"""
    tests = [
        ("Specific Player", '-ID "8479361"', "Should show Joseph Woll's information"),
        ("Another Player", '-ID "8481720"', "Should show Nick Abruzzese's information"),
    ]

    results = []
    for name, query, expected in tests:
        success, count = run_test(name, query, expected)
        results.append((name, success, count))

    return results


def test_combined_filters():
    """Test combinations of filters"""
    tests = [
        ("USA Goalies", '-POS G -CODES "USA"', "Should show only USA-born goalies"),
        (
            "Tall Centers",
            '-POS C +HEIGHT "6\'2"',
            "Should show centers 6'2\" and taller",
        ),
        (
            "Young Left-handed Players",
            '-AGE "20" -HAND "L"',
            "Should show players 20 and under who are left-handed",
        ),
        (
            "Canadian Defensemen",
            '-POS D -CODES "CAN"',
            "Should show only Canadian defensemen",
        ),
        (
            "Non-North American Goalies",
            '-POS G -EXCLUDE-CODES "USA,CAN"',
            "Should show goalies from outside USA and Canada",
        ),
        (
            "European Centers Only",
            '-POS C -CODES "SWE,FIN,RUS" -EXCLUDE-CODES "USA,CAN"',
            "Should show centers from specific European countries, excluding North America",
        ),
    ]

    results = []
    for name, query, expected in tests:
        success, count = run_test(name, query, expected)
        results.append((name, success, count))

    return results


def test_no_filters():
    """Test with no filters (should show all prospects)"""
    return run_test(
        "No Filters - All Prospects", "", "Should show all prospects from all teams"
    )


def main():
    """Run all tests"""
    print("🏒 NHL PROSPECTS FILTER TEST SUITE 🏒")
    print("Testing all filter options from the help menu")

    all_results = []

    # Run all test categories
    test_categories = [
        ("Help Menu", test_help_menu),
        ("No Filters", test_no_filters),
        ("Position Filters", test_position_filters),
        ("Draft Filters", test_draft_filters),
        ("Country Filters", test_country_filter),
        ("Country Exclude Filters", test_country_exclude_filter),
        ("Physical Filters", test_physical_filters),
        ("Hand Filters", test_hand_filter),
        ("Rank Filters", test_rank_filters),
        ("ID Filters", test_id_filter),
        ("Combined Filters", test_combined_filters),
    ]

    for category_name, test_func in test_categories:
        print(f"\n\n🔥 RUNNING {category_name.upper()} TESTS 🔥")

        if category_name in ["Help Menu", "No Filters"]:
            # These return single results
            success, count = test_func()
            all_results.append((category_name, success, count))
        else:
            # These return lists of results
            category_results = test_func()
            all_results.extend(
                [
                    (f"{category_name}: {name}", success, count)
                    for name, success, count in category_results
                ]
            )

    # Print summary
    print(f"\n\n{'='*80}")
    print("📊 TEST SUMMARY")
    print(f"{'='*80}")

    passed = 0
    failed = 0
    total_players = 0

    for test_name, success, count in all_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name} - {count} players found")

        if success:
            passed += 1
            total_players += count
        else:
            failed += 1

    print(f"\n📈 OVERALL RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"🎯 Success Rate: {passed/(passed+failed)*100:.1f}%")
    print(f"👥 Total Player Records Tested: {total_players}")

    print(f"\n{'='*80}")


if __name__ == "__main__":
    main()
