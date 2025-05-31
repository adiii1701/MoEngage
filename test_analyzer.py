#!/usr/bin/env python3
"""
Test script for the Documentation Analyzer Agent.
Includes mock analysis for testing without API calls.
"""

import json
from datetime import datetime
from doc_analyzer import DocumentationAnalyzer

class MockDocumentationAnalyzer(DocumentationAnalyzer):
    """Mock analyzer for testing without API calls."""
    
    def __init__(self):
        # Don't initialize the API client for mock
        pass
    
    def fetch_content(self, url):
        """Mock content fetching."""
        return {
            'url': url,
            'title': 'Setting Up Push Notifications - MoEngage',
            'full_text': 'This guide will help you set up push notifications in your mobile application using MoEngage SDK. First, you need to integrate the SDK into your project. The SDK provides comprehensive APIs for managing push notifications. You can customize the notification appearance and behavior. Make sure to test your implementation thoroughly before going live.',
            'headings': [
                {'level': 1, 'text': 'Setting Up Push Notifications'},
                {'level': 2, 'text': 'Prerequisites'},
                {'level': 2, 'text': 'SDK Integration'},
                {'level': 3, 'text': 'Android Setup'},
                {'level': 3, 'text': 'iOS Setup'},
                {'level': 2, 'text': 'Configuration'},
                {'level': 2, 'text': 'Testing'}
            ],
            'paragraphs': [
                'This guide will help you set up push notifications in your mobile application using MoEngage SDK.',
                'First, you need to integrate the SDK into your project.',
                'The SDK provides comprehensive APIs for managing push notifications.',
                'You can customize the notification appearance and behavior.',
                'Make sure to test your implementation thoroughly before going live.'
            ],
            'lists': [
                {'type': 'ul', 'items': ['Android SDK', 'iOS SDK', 'Web SDK']},
                {'type': 'ol', 'items': ['Download SDK', 'Add to project', 'Configure', 'Test']}
            ],
            'code_blocks': ['implementation "com.moengage:moe-android-sdk:12.0.0"', 'MoEngage.initialize(this, "YOUR_APP_ID")'],
            'word_count': 250,
            'paragraph_count': 5
        }
    
    def analyze_readability(self, content):
        """Mock readability analysis."""
        return {
            'flesch_kincaid_grade': 8.5,
            'gunning_fog_score': 11.2,
            'assessment': 'The content is moderately readable for marketers. Technical terms like "SDK" and "APIs" may need explanation. The writing style is clear but could be more conversational.',
            'suggestions': [
                'Define technical acronyms like "SDK" and "API" on first use',
                'Consider replacing "comprehensive APIs" with "complete set of tools"',
                'Add a brief explanation of what push notifications accomplish for marketing goals',
                'Use more active voice: "The SDK provides" → "Use the SDK to access"'
            ]
        }
    
    def analyze_structure(self, content):
        """Mock structure analysis."""
        return {
            'heading_count': 7,
            'paragraph_count': 5,
            'list_count': 2,
            'avg_paragraph_length': 15.6,
            'hierarchy_issues': [],
            'assessment': 'The article has good heading structure with logical flow from prerequisites to implementation to testing. The use of lists helps break down information.',
            'suggestions': [
                'Add a "Quick Start" section at the beginning for experienced developers',
                'Consider adding a troubleshooting section after the main content',
                'Include estimated time for each major section',
                'Add cross-references between related sections'
            ]
        }
    
    def analyze_completeness(self, content):
        """Mock completeness analysis."""
        return {
            'word_count': 250,
            'code_examples_count': 2,
            'sections_count': 7,
            'assessment': 'The article covers basic setup but lacks detailed implementation examples and error handling guidance. More practical examples would be beneficial.',
            'suggestions': [
                'Add complete code examples for both Android and iOS implementations',
                'Include common error scenarios and solutions',
                'Add screenshots of the notification setup process',
                'Provide sample notification payload examples',
                'Include performance optimization tips'
            ]
        }
    
    def analyze_style_guidelines(self, content):
        """Mock style guidelines analysis."""
        return {
            'assessment': 'The content follows basic style guidelines but could be more action-oriented and customer-focused. Some sentences use passive voice.',
            'suggestions': [
                'Replace "you need to integrate" with "integrate the SDK by following these steps"',
                'Change "Make sure to test" to "Test your implementation using these methods"',
                'Add benefit statements: explain why each step matters for the user',
                'Use more imperative mood for instructions: "Download the SDK" instead of "You should download"'
            ]
        }

def run_mock_test():
    """Run a test analysis using mock data."""
    print("Running Mock Analysis Test")
    print("=" * 30)
    
    mock_analyzer = MockDocumentationAnalyzer()
    
    test_url = "https://help.moengage.com/hc/en-us/articles/test-push-notifications"
    
    try:
        # Simulate the analysis process
        print(f"Analyzing: {test_url}")
        
        content = mock_analyzer.fetch_content(test_url)
        print(f"✓ Content fetched: {content['word_count']} words")
        
        readability = mock_analyzer.analyze_readability(content)
        print(f"✓ Readability analyzed: Grade {readability['flesch_kincaid_grade']}")
        
        structure = mock_analyzer.analyze_structure(content)
        print(f"✓ Structure analyzed: {structure['heading_count']} headings")
        
        completeness = mock_analyzer.analyze_completeness(content)
        print(f"✓ Completeness analyzed: {completeness['code_examples_count']} code examples")
        
        style = mock_analyzer.analyze_style_guidelines(content)
        print(f"✓ Style analyzed: {len(style['suggestions'])} suggestions")
        
        # Build complete result
        result = {
            'url': test_url,
            'title': content['title'],
            'analysis_timestamp': datetime.now().isoformat(),
            'readability': readability,
            'structure': structure,
            'completeness': completeness,
            'style_guidelines': style,
            'metadata': {
                'word_count': content['word_count'],
                'paragraph_count': content['paragraph_count'],
                'heading_count': len(content['headings']),
                'code_blocks_count': len(content['code_blocks'])
            }
        }
        
        print("\nTest completed successfully!")
        print("\nSample Output:")
        print("-" * 20)
        print(json.dumps(result, indent=2)[:1000] + "...")
        
        # Save test result
        with open('test_analysis_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        print("\nFull test result saved to: test_analysis_result.json")
        
    except Exception as e:
        print(f"Test failed: {str(e)}")

def validate_real_analyzer():
    """Validate that the real analyzer can be instantiated."""
    try:
        import os
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if api_key:
            analyzer = DocumentationAnalyzer(api_key)
            print(" Real analyzer can be instantiated with API key")
        else:
            print(" ANTHROPIC_API_KEY not set - real analyzer not tested")
            
    except Exception as e:
        print(f"✗ Real analyzer validation failed: {str(e)}")

if __name__ == "__main__":
    print("Documentation Analyzer - Test Suite")
    print("=" * 40)
    
    # Run mock test
    run_mock_test()
    
    print("\n" + "=" * 40)
    
    # Validate real analyzer
    validate_real_analyzer()
    
    print("\nTest suite completed!")
    print("\nTo run with real API:")
    print("1. Set ANTHROPIC_API_KEY environment variable")
    print("2. Run: python doc_analyzer.py 'https://help.moengage.com/hc/en-us/articles/your-url'")
