"""
Utility functions and LLM client
"""
import os
import re
import string
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfbase.pdfmetrics import stringWidth
from config import Config


# ============================================================================
# LLM CLIENT
# ============================================================================

class LLMClient:
    """Universal LLM client - supports OpenAI and Ollama"""

    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        self.ollama_url = Config.OLLAMA_URL
        self.ollama_model = Config.OLLAMA_MODEL
        self.openai_key = Config.OPENAI_API_KEY

        if self.provider == 'openai' and self.openai_key:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.openai_key)

    def generate(self, prompt, system_prompt=None):
        """Generate text using configured LLM"""
        if self.provider == 'openai':
            return self._generate_openai(prompt, system_prompt)
        else:
            return self._generate_ollama(prompt, system_prompt)

    def _generate_openai(self, prompt, system_prompt=None):
        """Generate using OpenAI API (new v1.0+ syntax)"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.openai_client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                temperature=Config.LLM_TEMPERATURE,
                max_tokens=Config.LLM_MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None

    def _generate_ollama(self, prompt, system_prompt=None):
        """Generate using Ollama"""
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=120
            )

            if response.status_code == 200:
                return response.json()['response']
            else:
                print(f"Ollama error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None


# Global LLM instance
llm = LLMClient()


# ============================================================================
# VALIDATION
# ============================================================================

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search("[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search("[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search("[0-9]", password):
        return "Password must contain at least one number."
    if not re.search("[!@#$%^&*]", password):
        return "Password must contain at least one special character (!@#$%^&*)."
    return None


# ============================================================================
# FILE UTILITIES
# ============================================================================

def sanitize_filename(text):
    """Sanitize a string to be used as a filename"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in text if c in valid_chars)
    return sanitized[:255]


# ============================================================================
# TEXT UTILITIES
# ============================================================================

def wrap_text(text, max_width, font_name, font_size):
    """Wrap text to fit within a given width"""
    wrapped_text = []
    words = text.split()

    while words:
        line = ''
        while words and stringWidth(line + words[0], font_name, font_size) <= max_width:
            line += (words.pop(0) + ' ')
        wrapped_text.append(line)

    return wrapped_text


def split_content_into_chunks(content, max_chars=400):
    """Split content into chunks for slides"""
    content_chunks = []
    current_chunk = ''

    for line in content.split('\n'):
        if len(current_chunk) + len(line) <= max_chars:
            current_chunk += line + '\n'
        else:
            content_chunks.append(current_chunk)
            current_chunk = line + '\n'

    if current_chunk:
        content_chunks.append(current_chunk)

    return content_chunks


# ============================================================================
# LATEX UTILITIES
# ============================================================================

def is_latex(text):
    """Check if a string contains LaTeX content"""
    return bool(re.search(r"\$.*\$", text))


def render_latex(formula, fontsize=12, dpi=150):
    """Render a LaTeX formula to an image"""
    plt.rcParams['text.usetex'] = True
    fig = plt.figure()
    fig.patch.set_alpha(0)
    ax = fig.add_subplot(111)
    ax.axis('off')
    ax.patch.set_alpha(0)
    ax.text(0, 0, f"\\begin{{equation}}{formula}\\end{{equation}}", fontsize=fontsize)
    buffer = BytesIO()
    fig.savefig(buffer, dpi=dpi, transparent=True, format='png')
    plt.close(fig)
    buffer.seek(0)
    return buffer


# ============================================================================
# DIFFICULTY MAPPING
# ============================================================================

DIFFICULTY_MAP = {
    1: "Grade 1 - Introduction to fundamental concepts",
    2: "Grade 2 - Building on basic skills and knowledge",
    3: "Grade 3 - Expanding core understanding",
    4: "Grade 4 - Deepening comprehension of key topics",
    5: "Grade 5 - Preparing for intermediate challenges",
    6: "Grade 6 - Transitioning to more complex subjects",
    7: "Grade 7 - Enhancing critical thinking and application",
    8: "Grade 8 - Solidifying foundational knowledge",
    9: "Grade 9 - High school introductory concepts",
    10: "Grade 10 - Sophomore explorations and depth",
    11: "Grade 11 - Junior year, college prep, and advanced topics",
    12: "Grade 12 - Senior year, culmination, and readiness for next steps"
}


def get_difficulty_text(difficulty):
    """Get difficulty description"""
    return DIFFICULTY_MAP.get(difficulty, DIFFICULTY_MAP[1])