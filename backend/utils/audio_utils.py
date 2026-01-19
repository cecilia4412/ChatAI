"""
音频处理工具函数
"""

import numpy as np
from typing import Tuple


def bytes_to_numpy(audio_bytes: bytes, dtype=np.int16) -> np.ndarray:
    """
    将字节数据转换为 numpy 数组
    
    Args:
        audio_bytes: 音频字节数据
        dtype: 数据类型
        
    Returns:
        numpy 数组
    """
    return np.frombuffer(audio_bytes, dtype=dtype)


def numpy_to_bytes(audio_array: np.ndarray) -> bytes:
    """
    将 numpy 数组转换为字节数据
    
    Args:
        audio_array: numpy 数组
        
    Returns:
        字节数据
    """
    return audio_array.tobytes()


def resample_audio(
    audio_data: np.ndarray, 
    orig_sr: int, 
    target_sr: int
) -> np.ndarray:
    """
    重采样音频
    
    Args:
        audio_data: 原始音频数据
        orig_sr: 原始采样率
        target_sr: 目标采样率
        
    Returns:
        重采样后的音频数据
    """
    # TODO: 实现重采样逻辑
    # 可以使用 librosa.resample 或 scipy.signal.resample
    return audio_data


def normalize_audio(audio_data: np.ndarray) -> np.ndarray:
    """
    归一化音频
    
    Args:
        audio_data: 音频数据
        
    Returns:
        归一化后的音频数据
    """
    max_val = np.abs(audio_data).max()
    if max_val > 0:
        return audio_data / max_val
    return audio_data


def calculate_rms(audio_data: np.ndarray) -> float:
    """
    计算音频的 RMS (均方根) 值
    
    Args:
        audio_data: 音频数据
        
    Returns:
        RMS 值
    """
    return np.sqrt(np.mean(audio_data ** 2))
