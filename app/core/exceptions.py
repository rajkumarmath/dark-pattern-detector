# app/core/exceptions.py
class DarkPatternDetectorError(Exception):
    """Base exception for dark pattern detector"""
    pass

class ModelLoadError(DarkPatternDetectorError):
    """Raised when model fails to load"""
    pass

class InvalidInputError(DarkPatternDetectorError):
    """Raised when input is invalid"""
    pass