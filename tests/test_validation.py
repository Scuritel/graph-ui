"""
Unit tests for validation module.
"""

from src.validation import ValidationResult, validate_all_parameters, validate_parameter


class TestValidationResult:
    """Test cases for ValidationResult dataclass."""

    def test_success_result(self) -> None:
        """Test creating a successful validation result."""
        result = ValidationResult.success(42.0)
        assert result.is_valid is True
        assert result.value == 42.0
        assert result.error_message is None

    def test_error_result(self) -> None:
        """Test creating a failed validation result."""
        result = ValidationResult.error("Invalid input")
        assert result.is_valid is False
        assert result.value is None
        assert result.error_message == "Invalid input"


class TestValidateParameter:
    """Test cases for validate_parameter function."""

    def test_valid_positive_number(self) -> None:
        """Test validation of a valid positive number."""
        result = validate_parameter("42.5", "a")
        assert result.is_valid is True
        assert result.value == 42.5
        assert result.error_message is None

    def test_valid_negative_number(self) -> None:
        """Test validation of a valid negative number."""
        result = validate_parameter("-3.14", "b", allow_zero=False)
        assert result.is_valid is True
        assert result.value == -3.14

    def test_valid_zero_when_allowed(self) -> None:
        """Test that zero is valid when allow_zero=True."""
        result = validate_parameter("0", "a", allow_zero=True)
        assert result.is_valid is True
        assert result.value == 0.0

    def test_invalid_zero_when_not_allowed(self) -> None:
        """Test that zero is invalid when allow_zero=False."""
        result = validate_parameter("0", "b", allow_zero=False)
        assert result.is_valid is False
        assert "cannot be zero" in result.error_message

    def test_empty_string(self) -> None:
        """Test validation of empty string."""
        result = validate_parameter("", "a")
        assert result.is_valid is False
        assert "cannot be empty" in result.error_message

    def test_whitespace_only(self) -> None:
        """Test validation of whitespace-only string."""
        result = validate_parameter("   ", "a")
        assert result.is_valid is False
        assert "cannot be empty" in result.error_message

    def test_non_numeric_string(self) -> None:
        """Test validation of non-numeric string."""
        result = validate_parameter("not a number", "a")
        assert result.is_valid is False
        assert "must be a valid number" in result.error_message

    def test_scientific_notation(self) -> None:
        """Test validation of scientific notation."""
        result = validate_parameter("1.5e-3", "a")
        assert result.is_valid is True
        assert result.value == 0.0015

    def test_whitespace_stripped(self) -> None:
        """Test that leading/trailing whitespace is stripped."""
        result = validate_parameter("  42.0  ", "a")
        assert result.is_valid is True
        assert result.value == 42.0


class TestValidateAllParameters:
    """Test cases for validate_all_parameters function."""

    def test_all_valid_parameters(self) -> None:
        """Test validation when all parameters are valid."""
        all_valid, errors = validate_all_parameters("1.0", "2.0", "3.0", "4.0")
        assert all_valid is True
        assert all(error is None for error in errors.values())

    def test_invalid_a_parameter(self) -> None:
        """Test validation when parameter 'a' is invalid."""
        all_valid, errors = validate_all_parameters("invalid", "2.0", "3.0", "4.0")
        assert all_valid is False
        assert errors["a"] is not None
        assert errors["b"] is None
        assert errors["c"] is None
        assert errors["d"] is None

    def test_b_can_be_zero_with_nonzero_d(self) -> None:
        """Test validation when parameter 'b' is zero but d is not (allowed)."""
        all_valid, errors = validate_all_parameters("1.0", "0", "1.0", "1.0")
        assert all_valid is True
        assert errors["b"] is None

    def test_both_b_and_d_zero_invalid(self) -> None:
        """Test validation when both 'b' and 'd' are zero (not allowed)."""
        all_valid, errors = validate_all_parameters("1.0", "0", "0", "0")
        assert all_valid is False
        assert errors["b"] is not None
        assert errors["d"] is not None
        assert "At least one of b or d must be non-zero" in errors["b"]

    def test_both_a_and_d_zero_invalid(self) -> None:
        """Test validation when both 'a' and 'd' are zero (constant zero)."""
        all_valid, errors = validate_all_parameters("0", "1.0", "0", "0")
        assert all_valid is False
        assert errors["a"] is not None
        assert errors["d"] is not None
        assert "At least one of a or d must be non-zero" in errors["a"]

    def test_d_can_be_zero(self) -> None:
        """Test validation when parameter 'd' is zero (allowed for pure sine with a≠0)."""
        all_valid, errors = validate_all_parameters("1.0", "2.0", "3.0", "0")
        assert all_valid is True
        assert errors["d"] is None

    def test_a_can_be_zero(self) -> None:
        """Test validation when parameter 'a' is zero (allowed for pure tangent)."""
        all_valid, errors = validate_all_parameters("0", "2.0", "3.0", "1.0")
        assert all_valid is True
        assert errors["a"] is None

    def test_multiple_invalid_parameters(self) -> None:
        """Test validation when multiple parameters are invalid."""
        all_valid, errors = validate_all_parameters("invalid", "abc", "", "xyz")
        assert all_valid is False
        assert errors["a"] is not None
        assert errors["b"] is not None
        assert errors["c"] is not None
        assert errors["d"] is not None

    def test_c_can_be_zero(self) -> None:
        """Test that parameter 'c' can be zero."""
        all_valid, errors = validate_all_parameters("1.0", "2.0", "0", "4.0")
        assert all_valid is True
        assert errors["c"] is None
