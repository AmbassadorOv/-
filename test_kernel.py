from kernel import OntologicalKernel

def test_ontological_kernel():
    kernel = OntologicalKernel()

    # Test valid sequence
    valid_seq = [1, 2, 3, 22, 1]
    is_valid, msg = kernel.validate_logic(valid_seq)
    print(f"Testing valid sequence {valid_seq}: {is_valid}, {msg}")
    assert is_valid is True

    # Test invalid sequence (self-loop)
    invalid_seq_self = [1, 1]
    is_valid, msg = kernel.validate_logic(invalid_seq_self)
    print(f"Testing invalid sequence (self-loop) {invalid_seq_self}: {is_valid}, {msg}")
    assert is_valid is False

    # Test invalid sequence (out of range)
    invalid_seq_range = [1, 23]
    is_valid, msg = kernel.validate_logic(invalid_seq_range)
    print(f"Testing invalid sequence (out of range) {invalid_seq_range}: {is_valid}, {msg}")
    assert is_valid is False

    # Test sync point
    sync_msg = kernel.sync_to_github_brain("some data")
    print(f"Testing sync point: {sync_msg}")
    assert "✅ Sync Point Created" in sync_msg

if __name__ == "__main__":
    try:
        test_ontological_kernel()
        print("✅ All tests passed!")
    except AssertionError as e:
        print("❌ Test failed!")
        exit(1)
