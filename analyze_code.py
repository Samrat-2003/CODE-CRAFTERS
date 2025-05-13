import json
import re
from collections import defaultdict
from datetime import datetime

class CodeAnalyzer:
    def __init__(self):
        self.metrics = defaultdict(dict)
        
    def analyze_code(self, submission_id, code, execution_time, timestamp):
        """Analyze code and calculate metrics."""
        metrics = {
            'length': len(code),
            'complexity': self._calculate_complexity(code),
            'execution_time': float(execution_time),
            'timestamp': datetime.fromisoformat(timestamp),
        }
        self.metrics[submission_id] = metrics
        
    def _calculate_complexity(self, code):
        """Calculate code complexity based on various factors."""
        # Count control structures
        control_structures = len(re.findall(r'\b(if|for|while|switch)\b', code))
        # Count function declarations
        functions = len(re.findall(r'\bfunction\b', code))
        # Count nested structures (rough estimate)
        nesting = len(re.findall(r'{[^{}]*{', code))
        
        return control_structures + functions + nesting
        
    def calculate_rank(self):
        """Calculate rankings based on metrics."""
        if not self.metrics:
            return []
            
        # Calculate scores
        scores = []
        for submission_id, metrics in self.metrics.items():
            # Lower is better for all metrics
            score = (
                metrics['execution_time'] * 0.4 +  # 40% weight for execution time
                metrics['complexity'] * 0.3 +      # 30% weight for complexity
                metrics['length'] * 0.2 +          # 20% weight for code length
                metrics['timestamp'].timestamp() * 0.1  # 10% weight for submission time
            )
            scores.append((submission_id, score))
        
        # Sort by score (lower is better)
        ranked_submissions = sorted(scores, key=lambda x: x[1])
        
        # Create ranking list
        rankings = []
        for rank, (submission_id, score) in enumerate(ranked_submissions, 1):
            rankings.append({
                'rank': rank,
                'submission_id': submission_id,
                'score': round(score, 2),
                'metrics': self.metrics[submission_id]
            })
            
        return rankings

    def save_rankings(self, filename='rankings.json'):
        """Save rankings to a JSON file."""
        rankings = self.calculate_rank()
        with open(filename, 'w') as f:
            json.dump(rankings, f, indent=2, default=str)

# Example usage
if __name__ == '__main__':
    analyzer = CodeAnalyzer()
    
    # Example submissions
    submissions = [
        {
            'id': 'sub1',
            'code': 'function sum(a,b) { return a + b; }',
            'execution_time': '0.15',
            'timestamp': '2024-03-14T10:00:00'
        },
        {
            'id': 'sub2',
            'code': '''
                function complexSum(arr) {
                    let sum = 0;
                    for (let i = 0; i < arr.length; i++) {
                        if (arr[i] > 0) {
                            sum += arr[i];
                        }
                    }
                    return sum;
                }
            ''',
            'execution_time': '0.25',
            'timestamp': '2024-03-14T10:05:00'
        }
    ]
    
    # Analyze submissions
    for sub in submissions:
        analyzer.analyze_code(
            sub['id'],
            sub['code'],
            sub['execution_time'],
            sub['timestamp']
        )
    
    # Calculate and save rankings
    analyzer.save_rankings()
    
    # Print rankings
    rankings = analyzer.calculate_rank()
    print("\nCode Submission Rankings:")
    print("-" * 50)
    for entry in rankings:
        print(f"Rank {entry['rank']}: Submission {entry['submission_id']}")
        print(f"Score: {entry['score']}")
        print(f"Execution Time: {entry['metrics']['execution_time']}s")
        print(f"Complexity: {entry['metrics']['complexity']}")
        print(f"Code Length: {entry['metrics']['length']} characters")
        print("-" * 50)