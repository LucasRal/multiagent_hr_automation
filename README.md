# Multi-Agent HR Automation System

A simple (yet quite sophisticated use case) HR automation system that leverages multiple AI agents orchestrated through LangGraph to automate and enhance the recruitment process.

## 🌟 Features

- **Profile Analysis**: Automated CV/resume matching with job descriptions
- **Interview Planning**: Dynamic generation of interview questions and evaluation criteria
- **Interview Feedback**: Simulated or real interview feedback processing
- **Final Synthesis**: Comprehensive candidate evaluation and recommendations
- **Multi-Agent Orchestration**: Seamless coordination between specialized agents
- **State Management**: Robust workflow state tracking and persistence

## 🛠️ System Architecture

The system consists of three main agents working in coordination:

1. **ProfileAnalyzerAgent**
   - Analyzes CV/resume match with job descriptions
   - Calculates matching scores
   - Identifies key skills and gaps

2. **InterviewerAgent**
   - Generates tailored interview questions
   - Creates evaluation criteria
   - Prepares technical and behavioral assessments

3. **HRCoordinatorAgent**
   - Synthesizes all recruitment information
   - Provides final recommendations
   - Suggests next steps

## 🔧 Technical Stack

- **Language**: Python 3.7+
- **Main Libraries**:
  - LangGraph: Agent orchestration
  - LangChain: LLM interactions
  - OpenAI: Language model integration
  - Pydantic: Data validation
  - Python-dotenv: Environment management

## 📋 Prerequisites

```bash
python 3.7+
pip (Python package manager)
```

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/multiagent_hr_automation.git
cd multiagent_hr_automation
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## 🚀 Usage

Basic usage example:

```python
from main import process_candidate

# Define job requirements
job_description = """
Senior Software Engineer
Requirements:
- 5+ years Python experience
- Experience with AI/ML
- Strong communication skills
"""

# Provide candidate information
cv_content = """
John Doe
Software Engineer with 6 years experience
Skills: Python, TensorFlow, Communication
"""

# Process the candidate
result = process_candidate(
    job_description=job_description,
    cv_content=cv_content,
    simulate_interview=True
)
```

## 📁 Project Structure

```
hr_multiagent/
│
├── agents/
│   ├── __init__.py
│   ├── profile_analyzer.py
│   ├── interviewer.py
│   └── hr_coordinator.py
│
├── core/
│   ├── __init__.py
│   ├── state.py
│   └── config.py
│
├── workflow/
│   ├── __init__.py
│   ├── nodes.py
│   └── graph.py
│
├── utils/
│   ├── __init__.py
│   └── json_helpers.py
│
├── main.py
└── requirements.txt
```

## 📊 Output Examples

The system generates detailed reports in JSON format:

```json
{
  "profile_analysis": {
    "matching_score": 85,
    "key_skills": ["Python", "AI/ML", "Leadership"],
    "gaps": ["Cloud Architecture"],
    "strengths": ["Technical Experience", "Team Leadership"]
  },
  "interview_plan": {
    "technical_questions": [...],
    "behavioral_questions": [...],
    "evaluation_criteria": [...]
  },
  "final_recommendation": {
    "decision": "GO",
    "next_steps": ["Technical Assignment", "Team Meeting"]
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [LangChain](https://github.com/langchain-ai/langchain)
- Inspired by modern HR automation needs

## 📞 Contact

Aina Lucas RALAMBO - [@LinkedIn](https://www.linkedin.com/in/lucas-ralambo/)

Project Link: [https://github.com/LucasRal/multiagent_hr_automation](https://github.com/LucasRal/multiagent_hr_automation)
