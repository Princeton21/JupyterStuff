from mrjob.job import MRJob
import re

class LogAnalysis(MRJob):
    
    def mapper(self, _, line):
        # Extract timestamp and log level from each log entry
        match = re.search(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+): (.+)$', line)
        if match:
            timestamp = match.group(1)
            log_level = match.group(2)
            yield log_level, (timestamp, 1)
    
    def reducer(self, log_level, values):
        total_count = 0
        min_timestamp = None
        max_timestamp = None
        
        for timestamp, count in values:
            total_count += count
            if min_timestamp is None or timestamp < min_timestamp:
                min_timestamp = timestamp
            if max_timestamp is None or timestamp > max_timestamp:
                max_timestamp = timestamp
        
        yield log_level, {
            'count': total_count,
            'min_timestamp': min_timestamp,
            'max_timestamp': max_timestamp
        }

if _name_ == '_main_':
    LogAnalysis.run()