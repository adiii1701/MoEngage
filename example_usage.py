#!/usr/bin/env python3
"""
Example usage script for the Documentation Analyzer Agent.
This script demonstrates how to use the analyzer programmatically.
"""

import json
import os
from doc_analyzer import DocumentationAnalyzer

def run_example_analysis():
    """Run example analysis on sample MoEngage documentation URLs."""
    
    # Get API key from environment
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if __name__ == "__main__":
    print("Documentation Analyzer - Example Usage")
    print("=" * 40)
    
    choice = input("\nChoose an option:\n1. Run example analysis on multiple URLs\n2. Demonstrate single detailed analysis\n3. Custom URL analysis\n\nEnter choice (1-3): ")
    
    if choice == '1':
        run_example_analysis()
    elif choice == '2':
        demonstrate_single_analysis()
    elif choice == '3':
        custom_url = input("Enter MoEngage documentation URL: ")
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("Error: Please set ANTHROPIC_API_KEY environment variable")
        else:
            try:
                analyzer = DocumentationAnalyzer(api_key)
                result = analyzer.analyze_document(custom_url)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Error: {str(e)}")
    else:
        print("Invalid choice. Please run again and select 1, 2, or 3.") not api_key:
        print("Error: Please set ANTHROPIC_API_KEY environment variable")
        return
    
    # Initialize analyzer
    analyzer = DocumentationAnalyzer(api_key)
    
    # Example URLs (replace with actual MoEngage documentation URLs)
    example_urls = [
        "https://help.moengage.com/hc/en-us/articles/229488268-Push-Notifications-Android",
        "https://help.moengage.com/hc/en-us/articles/229399928-Email-Campaigns"
    ]
    
    results = []
    
    for url in example_urls:
        try:
            print(f"\nAnalyzing: {url}")
            print("-" * 50)
            
            # Perform analysis
            result = analyzer.analyze_document(url)
            results.append(result)
            
            # Print summary
            print(f"Title: {result['title']}")
            print(f"Word count: {result['metadata']['word_count']}")
            print(f"Readability grade: {result['readability']['flesch_kincaid_grade']:.1f}")
            print(f"Total suggestions: {len(result['readability']['suggestions']) + len(result['structure']['suggestions']) + len(result['completeness']['suggestions']) + len(result['style_guidelines']['suggestions'])}")
            
            # Print top suggestions from each category
            print("\nTop Suggestions:")
            for category in ['readability', 'structure', 'completeness', 'style_guidelines']:
                if result[category]['suggestions']:
                    print(f"  {category.title()}: {result[category]['suggestions'][0]}")
            
        except Exception as e:
            print(f"Error analyzing {url}: {str(e)}")
    
    # Save all results
    output_file = "example_analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nComplete results saved to: {output_file}")

def demonstrate_single_analysis():
    """Demonstrate detailed analysis of a single document."""
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: Please set ANTHROPIC_API_KEY environment variable")
        return
    
    analyzer = DocumentationAnalyzer(api_key)
    
    # Replace with actual URL
    url = "https://help.moengage.com/hc/en-us/articles/your-article-here"
    
    try:
        result = analyzer.analyze_document(url)
        
        print("DETAILED ANALYSIS REPORT")
        print("=" * 60)
        print(f"URL: {result['url']}")
        print(f"Title: {result['title']}")
        print(f"Analysis Date: {result['analysis_timestamp']}")
        print()
        
        # Readability Analysis
        print("READABILITY ANALYSIS")
        print("-" * 30)
        print(f"Flesch-Kincaid Grade: {result['readability']['flesch_kincaid_grade']:.1f}")
        print(f"Gunning Fog Score: {result['readability']['gunning_fog_score']:.1f}")
        print("\nSuggestions:")
        for i, suggestion in enumerate(result['readability']['suggestions'][:5], 1):
            print(f"  {i}. {suggestion}")
        print()
        
        # Structure Analysis
        print("STRUCTURE ANALYSIS")
        print("-" * 30)
        print(f"Headings: {result['structure']['heading_count']}")
        print(f"Paragraphs: {result['structure']['paragraph_count']}")
        print(f"Lists: {result['structure']['list_count']}")
        print(f"Avg Paragraph Length: {result['structure']['avg_paragraph_length']:.1f} words")
        print("\nSuggestions:")
        for i, suggestion in enumerate(result['structure']['suggestions'][:5], 1):
            print(f"  {i}. {suggestion}")
        print()
        
        # Completeness Analysis
        print("COMPLETENESS ANALYSIS")
        print("-" * 30)
        print(f"Word Count: {result['completeness']['word_count']}")
        print(f"Code Examples: {result['completeness']['code_examples_count']}")
        print(f"Sections: {result['completeness']['sections_count']}")
        print("\nSuggestions:")
        for i, suggestion in enumerate(result['completeness']['suggestions'][:5], 1):
            print(f"  {i}. {suggestion}")
        print()
        
        # Style Guidelines Analysis
        print("STYLE GUIDELINES ANALYSIS")
        print("-" * 30)
        print("Suggestions:")
        for i, suggestion in enumerate(result['style_guidelines']['suggestions'][:5], 1):
            print(f"  {i}. {suggestion}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if