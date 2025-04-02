#!/usr/bin/env python3

import sys
import json
import datetime
import pytz
from typing import Dict, Any, List, Optional

# MCP protocol implementation
class MCPServer:
    def __init__(self):
        self.supported_commands = ["get_current_time", "convert_time"]
        
    def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming MCP request"""
        if "command" not in input_data:
            return self._error_response("Missing command field")
            
        command = input_data.get("command")
        
        if command not in self.supported_commands:
            return self._error_response(f"Unsupported command: {command}")
            
        try:
            if command == "get_current_time":
                return self._handle_get_current_time(input_data)
            elif command == "convert_time":
                return self._handle_convert_time(input_data)
        except Exception as e:
            return self._error_response(f"Error processing command: {str(e)}")
    
    def _handle_get_current_time(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_current_time command"""
        try:
            timezone = input_data.get("args", {}).get("timezone", "UTC")
            tz = pytz.timezone(timezone)
            now = datetime.datetime.now(tz)
            
            return {
                "status": "success",
                "result": {
                    "timezone": timezone,
                    "datetime": now.isoformat(),
                    "is_dst": now.dst() != datetime.timedelta(0)
                }
            }
        except pytz.exceptions.UnknownTimeZoneError:
            return self._error_response(f"Unknown timezone: {timezone}")
    
    def _handle_convert_time(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle convert_time command"""
        try:
            args = input_data.get("args", {})
            source_timezone = args.get("source_timezone", "UTC")
            target_timezone = args.get("target_timezone", "UTC")
            time_str = args.get("time", "")
            
            if not time_str:
                return self._error_response("Missing time parameter")
                
            # Parse time string (expected format: HH:MM)
            try:
                hour, minute = map(int, time_str.split(':'))
                if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                    return self._error_response("Invalid time format. Use HH:MM in 24-hour format")
            except ValueError:
                return self._error_response("Invalid time format. Use HH:MM in 24-hour format")
                
            # Get current date in source timezone
            source_tz = pytz.timezone(source_timezone)
            now = datetime.datetime.now(source_tz)
            
            # Create datetime with provided time
            dt = datetime.datetime(now.year, now.month, now.day, hour, minute, 0, 0, tzinfo=source_tz)
            
            # Convert to target timezone
            target_tz = pytz.timezone(target_timezone)
            converted_dt = dt.astimezone(target_tz)
            
            # Calculate time difference
            source_offset = source_tz.utcoffset(now).total_seconds() / 3600
            target_offset = target_tz.utcoffset(now).total_seconds() / 3600
            difference = f"{'+' if target_offset > source_offset else ''}{target_offset - source_offset:.1f}h"
            
            return {
                "status": "success",
                "result": {
                    "source": {
                        "timezone": source_timezone,
                        "datetime": dt.isoformat(),
                        "is_dst": dt.dst() != datetime.timedelta(0)
                    },
                    "target": {
                        "timezone": target_timezone,
                        "datetime": converted_dt.isoformat(),
                        "is_dst": converted_dt.dst() != datetime.timedelta(0)
                    },
                    "time_difference": difference
                }
            }
        except pytz.exceptions.UnknownTimeZoneError as e:
            return self._error_response(f"Unknown timezone: {str(e)}")
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "status": "error",
            "error": {
                "message": message
            }
        }

def main():
    """Main function to run the MCP server"""
    server = MCPServer()
    
    # Process JSON input line by line
    for line in sys.stdin:
        try:
            input_data = json.loads(line)
            response = server.process_input(input_data)
            print(json.dumps(response))
            sys.stdout.flush()
        except json.JSONDecodeError:
            error_response = {"status": "error", "error": {"message": "Invalid JSON input"}}
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main()