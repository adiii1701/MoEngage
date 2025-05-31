import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import anthropic
from textstat import flesch_kincaid_grade, gunning_fog
import argparse
import os
from typing import Dict, List, Any
import time

class DocumentationAnalyzer:
    def __init__(self, anthropic_api_key: str):
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})

    def fetch_content(self, url: str) -> Dict[str, Any]:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        article_content = soup.find('article') or soup.find('div', class_='article-body') or soup.find('main')
        if not article_content:
            article_content = soup.find('div', {'class': re.compile(r'content|article|body')})
        if not article_content:
            raise ValueError("Could not locate main article content")
        title = (soup.find('h1') or soup.find('title')).get_text(strip=True) if soup.find('h1') or soup.find('title') else "No title"
        headings = [{'level': int(h.name[1]), 'text': h.get_text(strip=True)} for h in article_content.find_all(['h1','h2','h3','h4','h5','h6'])]
        paragraphs = [p.get_text(strip=True) for p in article_content.find_all('p') if p.get_text(strip=True)]
        lists = [{'type': ul.name, 'items': [li.get_text(strip=True) for li in ul.find_all('li')]} for ul in article_content.find_all(['ul','ol'])]
        code_blocks = [c.get_text(strip=True) for c in article_content.find_all(['code','pre'])]
        full_text = article_content.get_text(separator=' ', strip=True)
        return {
            'url': url, 'title': title, 'full_text': full_text, 'headings': headings,
            'paragraphs': paragraphs, 'lists': lists, 'code_blocks': code_blocks,
            'word_count': len(full_text.split()), 'paragraph_count': len(paragraphs)
        }

    def _extract_feedback_suggestions(self, assessment: str) -> List[str]:
        lines = assessment.split('\n')
        return [line.strip() for line in lines if any(k in line.lower() for k in ['suggest','recommend','consider','improve','add','remove','change']) and len(line.strip()) > 20][:10]

    def analyze_readability(self, content: Dict[str, Any]) -> Dict[str, Any]:
        text = content['full_text']
        fk = flesch_kincaid_grade(text)
        fog = gunning_fog(text)
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1500,
                messages=[{"role": "user", "content": f"Analyze readability:\n{text[:2000]}"}]
            )
            llm = message.content[0].text
        except Exception as e:
            llm = f"LLM failed: {str(e)}"
        return {'flesch_kincaid_grade': fk, 'gunning_fog_score': fog, 'assessment': llm, 'suggestions': self._extract_feedback_suggestions(llm)}

    def analyze_structure(self, content: Dict[str, Any]) -> Dict[str, Any]:
        headings = content['headings']
        paragraphs = content['paragraphs']
        lists = content['lists']
        avg_par_len = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1500,
                messages=[{"role": "user", "content": f"Structure analysis for:\n{content['title']}"}]
            )
            assessment = message.content[0].text
        except Exception as e:
            assessment = f"Structure analysis failed: {str(e)}"
        return {
            'heading_count': len(headings), 'paragraph_count': len(paragraphs), 'list_count': len(lists),
            'avg_paragraph_length': avg_par_len, 'hierarchy_issues': [],
            'assessment': assessment, 'suggestions': self._extract_feedback_suggestions(assessment)
        }

    def analyze_completeness(self, content: Dict[str, Any]) -> Dict[str, Any]:
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1500,
                messages=[{"role": "user", "content": f"Evaluate completeness:\n{content['full_text'][:2500]}"}]
            )
            assessment = message.content[0].text
        except Exception as e:
            assessment = f"Completeness analysis failed: {str(e)}"
        return {
            'word_count': content['word_count'],
            'code_examples_count': len(content['code_blocks']),
            'sections_count': len(content['headings']),
            'assessment': assessment,
            'suggestions': self._extract_feedback_suggestions(assessment)
        }

    def analyze_style_guidelines(self, content: Dict[str, Any]) -> Dict[str, Any]:
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1500,
                messages=[{"role": "user", "content": f"Style guide compliance:\n{content['full_text'][:2500]}"}]
            )
            assessment = message.content[0].text
        except Exception as e:
            assessment = f"Style analysis failed: {str(e)}"
        return {
            'assessment': assessment,
            'suggestions': self._extract_feedback_suggestions(assessment)
        }

    def analyze_document(self, url: str) -> Dict[str, Any]:
        content = self.fetch_content(url)
        time.sleep(1)
        readability = self.analyze_readability(content)
        time.sleep(1)
        structure = self.analyze_structure(content)
        time.sleep(1)
        completeness = self.analyze_completeness(content)
        time.sleep(1)
        style = self.analyze_style_guidelines(content)
        return {
            'url': url,
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL to analyze')
    parser.add_argument('--api-key', help='Anthropic API key')
    parser.add_argument('--output', '-o', help='Output file path')
    args = parser.parse_args()
    api_key = args.api_key or os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("API key required.")
        return 1
    analyzer = DocumentationAnalyzer(api_key)
    result = analyzer.analyze_document(args.url)
    output_json = json.dumps(result, indent=2)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
    else:
        print(output_json)
    return 0

if __name__ == "__main__":
    exit(main())
