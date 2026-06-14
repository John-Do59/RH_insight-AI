import pytest
import sys
import subprocess

def run_tests():
    print("========================================")
    print("RH Insight AI - Matching Engine Test Suite")
    print("========================================\n")
    
    # 1. Seed the database
    print("[1/4] Seeding the mock database...")
    result = subprocess.run([sys.executable, "backend/tests/utils/seed_database.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Error seeding database:")
        print(result.stderr)
        sys.exit(1)
    print("✔ Database seeded successfully.")

    # 2. Run pytest
    print("\n[2/4] Running E2E Test Suite...")
    pytest_args = [
        "-v",
        "backend/tests/e2e/test_mock_data_factory.py",
        "backend/tests/e2e/test_matching_pipeline.py",
        "backend/tests/e2e/test_cache_behavior.py",
        "backend/tests/e2e/test_matching_consistency.py"
    ]
    
    # Run pytest inline
    exit_code = pytest.main(pytest_args)
    
    print("\n========================================")
    if exit_code == 0:
        print("✔ Matching pipeline OK")
        print("✔ Cache behavior OK")
        print("✔ Consistency OK")
        print("✔ No critical failures")
        print("\nSUCCESS RATE: 100%")
        print("\nRH Insight AI Matching Engine\n")
        print("Status: STABLE")
        print("Tests: PASSED")
        print("Pipeline: OPERATIONAL")
        print("Cache: ACTIVE")
    else:
        print("❌ Tests failed. Please check the logs above.")
        sys.exit(exit_code)

if __name__ == "__main__":
    run_tests()
