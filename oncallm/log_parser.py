import json
import logging
import re
from datetime import datetime
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class LogParser:
    """Utility class for parsing and analyzing Kubernetes logs."""

    @staticmethod
    def extract_error_messages(log_text: str) -> list[str]:
        """
        Extract error messages from log text.
        
        Args:
            log_text: Raw log text
            
        Returns:
            List of error messages
        """
        error_patterns = [
            r'Error: (.*)',
            r'ERROR: (.*)',
            r'Exception: (.*)',
            r'Failed: (.*)',
            r'\[error\] (.*)',
            r'\[ERROR\] (.*)',
            r'fatal: (.*)'
        ]

        errors = []
        for pattern in error_patterns:
            matches = re.finditer(pattern, log_text, re.MULTILINE)
            for match in matches:
                errors.append(match.group(1).strip())

        return errors

    @staticmethod
    def extract_json_logs(log_text: str) -> list[dict[str, Any]]:
        """
        Extract JSON log entries from log text.
        
        Args:
            log_text: Raw log text
            
        Returns:
            List of parsed JSON log entries
        """
        json_logs = []
        for line in log_text.splitlines():
            line = line.strip()
            if not line:
                continue

            # Try to find JSON objects in the line.
            try:
                # Find potential JSON by looking for curly braces.
                json_start = line.find('{')
                json_end = line.rfind('}')

                if 0 <= json_start < json_end:
                    json_str = line[json_start:json_end + 1]
                    log_entry = json.loads(json_str)
                    json_logs.append(log_entry)
            except json.JSONDecodeError:
                # Not a valid JSON object, skip.
                continue

        return json_logs

    @staticmethod
    def extract_timestamps(log_text: str) -> list[tuple[str, datetime]]:
        """
        Extract timestamps from log text.
        
        Args:
            log_text: Raw log text
            
        Returns:
            List of tuples with (log_line, timestamp)
        """
        # Common timestamp patterns
        timestamp_patterns = [
            # ISO format: 2023-01-23T12:34:56.789Z
            (r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z)', '%Y-%m-%dT%H:%M:%S.%fZ'),

            # ISO format with timezone: 2023-01-23T12:34:56+00:00
            (r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})', '%Y-%m-%dT%H:%M:%S%z'),

            # Standard format: 2023-01-23 12:34:56
            (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', '%Y-%m-%d %H:%M:%S'),

            # Standard format with ms: 2023-01-23 12:34:56.789
            (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})', '%Y-%m-%d %H:%M:%S.%f'),
        ]

        timestamps = []
        for line in log_text.splitlines():
            line = line.strip()
            if not line:
                continue

            for pattern, date_format in timestamp_patterns:
                match = re.search(pattern, line)
                if match:
                    try:
                        timestamp_str = match.group(1)
                        # Handle timezone format differences
                        if '+' in timestamp_str or '-' in timestamp_str:
                            # Convert +00:00 format to +0000 for parsing
                            if ':' in timestamp_str[-6:]:
                                timestamp_str = timestamp_str[:-3] + timestamp_str[-2:]

                        timestamp = datetime.strptime(timestamp_str, date_format)
                        timestamps.append((line, timestamp))
                        break
                    except ValueError:
                        # Parsing error, try next pattern
                        continue

        return timestamps

    @staticmethod
    def find_common_patterns(log_text: str, min_occurrences: int = 3) -> list[tuple[str, int]]:
        """
        Find common patterns in logs.
        
        Args:
            log_text: Raw log text
            min_occurrences: Minimum number of occurrences to consider a pattern common
            
        Returns:
            List of tuples with (pattern, count)
        """
        lines = [line.strip() for line in log_text.splitlines() if line.strip()]

        # Count occurrences of each line
        line_counts = {}
        for line in lines:
            # Skip lines that are too short (likely not meaningful)
            if len(line) < 10:
                continue

            # Normalize the line to find patterns
            # Replace timestamps, IDs, etc. with placeholders
            normalized = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z', '<TIMESTAMP>', line)
            normalized = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}', '<TIMESTAMP>', normalized)
            normalized = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '<TIMESTAMP>', normalized)
            normalized = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}', '<TIMESTAMP>', normalized)
            normalized = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<UUID>', normalized)
            normalized = re.sub(r'\b([0-9a-f]{32}|[0-9a-f]{40}|[0-9a-f]{64})\b', '<HASH>', normalized)
            normalized = re.sub(r'\b\d+\.\d+\.\d+\.\d+\b', '<IP>', normalized)

            if normalized in line_counts:
                line_counts[normalized] += 1
            else:
                line_counts[normalized] = 1

        # Filter to common patterns
        common_patterns = [(pattern, count) for pattern, count in line_counts.items() if count >= min_occurrences]

        # Sort by frequency (most frequent first)
        return sorted(common_patterns, key=lambda x: x[1], reverse=True)

    @staticmethod
    def analyze_log_frequency(log_text: str, time_window_minutes: int = 5) -> dict[str, Any]:
        """
        Analyze log frequency within time windows.
        
        Args:
            log_text: Raw log text
            time_window_minutes: Size of time window in minutes
            
        Returns:
            Dictionary with frequency analysis
        """
        # Extract timestamps from logs
        timestamp_lines = LogParser.extract_timestamps(log_text)

        if not timestamp_lines:
            return {"error": "No timestamps found in logs"}

        # Sort by timestamp
        timestamp_lines.sort(key=lambda x: x[1])

        # Get start and end times
        start_time = timestamp_lines[0][1]
        end_time = timestamp_lines[-1][1]

        # Calculate duration
        duration = (end_time - start_time).total_seconds() / 60  # in minutes

        # If duration is too short, adjust the time window
        if duration < time_window_minutes:
            time_window_minutes = max(1, int(duration))

        # Create time windows
        time_windows = {}
        for line, timestamp in timestamp_lines:
            # Calculate which window this belongs to
            minutes_since_start = (timestamp - start_time).total_seconds() / 60
            window_index = int(minutes_since_start / time_window_minutes)
            window_start = start_time.replace(second=0, microsecond=0)

            window_key = f"window_{window_index}"
            if window_key not in time_windows:
                window_start_time = start_time + pd.Timedelta(minutes=window_index * time_window_minutes)
                time_windows[window_key] = {
                    "start_time": window_start_time,
                    "end_time": window_start_time + pd.Timedelta(minutes=time_window_minutes),
                    "count": 0,
                    "error_count": 0
                }

            time_windows[window_key]["count"] += 1

            # Check if it's an error line.
            if any(err_term in line.lower() for err_term in ["error", "exception", "failed", "fatal"]):
                time_windows[window_key]["error_count"] += 1

        # Find the window with the highest log frequency and error rate.
        max_frequency_window = max(time_windows.values(), key=lambda x: x["count"])
        max_error_rate_window = max(time_windows.values(), key=lambda x: x["error_count"] / max(x["count"], 1))

        return {
            "total_logs": len(timestamp_lines),
            "duration_minutes": duration,
            "time_window_minutes": time_window_minutes,
            "windows": time_windows,
            "max_frequency_window": max_frequency_window,
            "max_error_rate_window": max_error_rate_window
        }
