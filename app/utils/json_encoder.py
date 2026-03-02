# app/utils/json_encoder.py
import numpy as np
from fastapi.encoders import jsonable_encoder
from typing import Any

def convert_numpy_types(obj: Any) -> Any:
    """
    Convert NumPy types to native Python types for JSON serialization
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.str_):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    return obj

class NumpySafeJSONEncoder:
    """Custom JSON encoder that handles NumPy types"""
    
    @staticmethod
    def encode(data: Any) -> Any:
        """Recursively convert NumPy types in data"""
        return convert_numpy_types(data)
