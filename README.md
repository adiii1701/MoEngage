# AI-Powered Documentation Improvement Agent

An intelligent agent that analyzes MoEngage documentation articles and provides actionable suggestions for improvement across multiple criteria including readability, structure, completeness, and style guidelines.

---

## 📑 Table of Contents

1. [Features](#features)  
2. [Setup Instructions](#setup-instructions)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)  
3. [Usage](#usage)  
   - [Basic Usage](#basic-usage)  
   - [With API Key Argument](#with-api-key-argument)  
   - [Save Output to File](#save-output-to-file)  
   - [Using as Python Module](#using-as-python-module)  
4. [Output Format](#output-format)  
5. [Design Choices & Approach](#design-choices--approach)  
   - [Architecture](#architecture)  
   - [LLM Integration](#llm-integration)  
   - [Web Scraping Strategy](#web-scraping-strategy)  
   - [Style Guidelines Implementation](#style-guidelines-implementation)  
6. [Assumptions Made](#assumptions-made)  
7. [Example Outputs](#example-outputs)  
   - [Example 1: Tutorial Article](#example-1-tutorial-article)  
   - [Example 2: Reference Documentation](#example-2-reference-documentation)  

---


## Features

- **Readability Analysis**: Evaluates content accessibility for non-technical marketers using both algorithmic scores (Flesch-Kincaid, Gunning Fog) and AI assessment
- **Structure & Flow Analysis**: Examines article organization, heading hierarchy, and navigation ease
- **Completeness Assessment**: Identifies gaps in information, examples, and implementation details
- **Style Guidelines Compliance**: Checks adherence to Microsoft Style Guide principles (voice, clarity, action-oriented language)
- **Structured Output**: Generates detailed JSON reports with specific, actionable improvement suggestions

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Anthropic API key (Claude)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/adiii1701/MoEngage/
cd documentation-analyzer
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up API key**:
```bash
# Option 1: Environment variable (recommended)
export ANTHROPIC_API_KEY="your-api-key-here"

# Option 2: Pass as command line argument
# (see usage section below)
```

## Usage

### Basic Usage
```bash
python doc_analyzer.py "https://help.moengage.com/hc/en-us/articles/your-article-url"
```

### With API Key Argument
```bash
python doc_analyzer.py "https://help.moengage.com/hc/en-us/articles/your-article-url" --api-key "your-api-key"
```

### Save Output to File
```bash
python doc_analyzer.py "https://help.moengage.com/hc/en-us/articles/your-article-url" --output analysis_report.json
```

### Using as Python Module
```python
from doc_analyzer import DocumentationAnalyzer

analyzer = DocumentationAnalyzer(api_key="your-api-key")
result = analyzer.analyze_document("https://help.moengage.com/hc/en-us/articles/...")
print(json.dumps(result, indent=2))
```

## Output Format

The analyzer generates a structured JSON report with the following format:

```json
{
  "url": "https://help.moengage.com/hc/en-us/articles/...",
  "title": "Article Title",
  "analysis_timestamp": "2025-05-31T...",
  "readability": {
    "flesch_kincaid_grade": 12.5,
    "gunning_fog_score": 14.2,
    "assessment": "Detailed AI assessment of readability for marketers...",
    "suggestions": [
      "Specific suggestion 1",
      "Specific suggestion 2"
    ]
  },
  "structure": {
    "heading_count": 8,
    "paragraph_count": 15,
    "list_count": 3,
    "avg_paragraph_length": 67.3,
    "hierarchy_issues": [],
    "assessment": "AI assessment of structure and flow...",
    "suggestions": [
      "Structure improvement suggestions..."
    ]
  },
  "completeness": {
    "word_count": 1250,
    "code_examples_count": 2,
    "sections_count": 8,
    "assessment": "AI assessment of content completeness...",
    "suggestions": [
      "Completeness improvement suggestions..."
    ]
  },
  "style_guidelines": {
    "assessment": "AI assessment of style guide adherence...",
    "suggestions": [
      "Style improvement suggestions..."
    ]
  },
  "metadata": {
    "word_count": 1250,
    "paragraph_count": 15,
    "heading_count": 8,
    "code_blocks_count": 2
  }
}
```

## Design Choices & Approach

### Architecture
- **Modular Design**: Separate analysis modules for each criterion (readability, structure, completeness, style)
- **Hybrid Analysis**: Combines algorithmic metrics with LLM insights for comprehensive evaluation
- **Error Handling**: Robust error handling for web scraping and API calls
- **Rate Limiting**: Built-in delays to respect API rate limits

### LLM Integration
- **Claude 3 Sonnet**: Chosen for its strong analytical capabilities and detailed feedback
- **Focused Prompts**: Tailored prompts for each analysis criterion
- **Context-Aware**: Considers marketer persona and documentation context

### Web Scraping Strategy
- **Flexible Content Extraction**: Multiple fallback selectors for different HTML structures
- **Structured Data Extraction**: Separates headings, paragraphs, lists, and code blocks
- **Metadata Collection**: Gathers comprehensive document statistics

### Style Guidelines Implementation
- **Microsoft Style Guide Focus**: Emphasizes voice/tone, clarity, and action-oriented language
- **Practical Application**: Focuses on 2-3 key aspects as specified in requirements
- **Specific Suggestions**: Provides concrete, actionable improvements rather than generic advice

## Assumptions Made

1. **Content Structure**: Assumes MoEngage documentation follows standard HTML article structure with identifiable content containers
2. **Marketer Persona**: Defines "non-technical marketer" as someone familiar with marketing concepts but not necessarily technical implementation details
3. **Suggestion Prioritization**: Limits to top 10 suggestions per category to maintain actionability
4. **Rate Limiting**: Implements 1-second delays between API calls to ensure stability
5. **Content Length**: Analyzes first 2000-2500 characters for LLM assessment to balance context and token efficiency



## Example Outputs

### Example 1: Tutorial Article
```json
{
  "url": "https://help.moengage.com/hc/en-us/articles/example-tutorial",
  "title": "Setting Up Push Notifications",
  "readability": {
    "flesch_kincaid_grade": 10.2,
    "suggestions": [
      "Replace 'SDK integration methodology' with 'how to integrate the SDK'",
      "Break down the 89-word paragraph in section 3 into smaller chunks"
    ]
  },
  "structure": {
    "suggestions": [
      "Add a 'Prerequisites' section before diving into implementation steps",
      "Consider adding a 'Troubleshooting' section at the end"
    ]
  }
}
```

### Example 2: Reference Documentation
```json
{
  "url": "https://help.moengage.com/hc/en-us/articles/example-reference",
  "title": "API Reference - Events",
  "completeness": {
    "suggestions": [
      "Missing code examples for error handling scenarios",
      "Add response format examples for each endpoint",
      "Include rate limiting information"
    ]
  },
  "style_guidelines": {
    "suggestions": [
      "Replace passive voice: 'Events can be tracked' → 'Track events'",
      "Add action-oriented headings: 'Event Tracking' → 'Track Your Events'"
    ]
  }
}
```
