#!/usr/bin/env python3
"""
Cerebras Cloud inference client - fast LLM workhorse.
"""

import argparse
import asyncio
import json
import os
import sys
from typing import AsyncIterator, Optional

try:
    import aiohttp
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp", "-q"])
    import aiohttp

# Configuration
def get_config():
    """Load config from env or file."""
    config = {
        "api_key": os.getenv("CEREBRAS_API_KEY"),
        "model": os.getenv("CEREBRAS_MODEL", "zai-glm-4.7"),
        "base_url": "https://api.cerebras.ai/v1",
    }
    
    # Try config file
    config_path = os.path.expanduser("~/.config/cerebras/config")
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip().lower()
                    value = value.strip().strip('"\'')
                    if key == "cerebras_api_key" and not config["api_key"]:
                        config["api_key"] = value
                    elif key == "cerebras_model":
                        config["model"] = value
    
    return config


class CerebrasClient:
    """Async client for Cerebras Cloud inference."""
    
    MODELS = {
        "zai-glm-4.7": "zai-glm-4.7",  # Coding specialist (default)
        "llama-3.3-70b": "llama-3.3-70b",
        "llama3.1-8b": "llama3.1-8b",
        "qwen-3-32b": "qwen-3-32b",
        "gpt-oss-120b": "gpt-oss-120b",  # OpenAI's open model
    }
    
    def __init__(self, api_key: str = None, model: str = None):
        config = get_config()
        self.api_key = api_key or config["api_key"]
        self.model = model or config["model"]
        self.base_url = config["base_url"]
        
        if not self.api_key:
            raise ValueError("CEREBRAS_API_KEY not set. Export it or add to ~/.config/cerebras/config")
    
    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    async def complete(
        self,
        prompt: str,
        system: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Simple completion."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        return await self.chat(messages, max_tokens, temperature)
    
    async def chat(
        self,
        messages: list[dict],
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Chat completion."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }
            ) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    raise Exception(f"Cerebras API error {resp.status}: {error}")
                
                data = await resp.json()
                return data["choices"][0]["message"]["content"]
    
    async def stream(
        self,
        prompt: str,
        system: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        """Streaming completion."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "stream": True,
                }
            ) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    raise Exception(f"Cerebras API error {resp.status}: {error}")
                
                async for line in resp.content:
                    line = line.decode().strip()
                    if line.startswith("data: ") and line != "data: [DONE]":
                        try:
                            data = json.loads(line[6:])
                            delta = data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                        except json.JSONDecodeError:
                            continue
    
    async def code(
        self,
        task: str,
        context: str = None,
        language: str = "python",
    ) -> str:
        """Code generation with coding-optimized prompt."""
        system = f"""You are an expert {language} programmer. 
Output only code, no explanations unless asked.
Follow best practices and include error handling."""
        
        prompt = task
        if context:
            prompt = f"Context:\n```\n{context}\n```\n\nTask: {task}"
        
        return await self.complete(prompt, system=system, temperature=0.3)


# Preset prompts for common tasks
PRESETS = {
    "refactor": "Refactor this code to be cleaner and more maintainable:",
    "test": "Write comprehensive pytest tests for this code:",
    "docs": "Write docstrings and comments for this code:",
    "types": "Add type hints to this Python code:",
    "translate": "Translate this code to {target_lang}:",
    "explain": "Explain what this code does step by step:",
}


async def main():
    parser = argparse.ArgumentParser(description="Cerebras inference client")
    parser.add_argument("--model", default=None, help="Model to use")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Complete
    comp = subparsers.add_parser("complete", help="Simple completion")
    comp.add_argument("prompt", help="Prompt text")
    comp.add_argument("--system", help="System prompt")
    comp.add_argument("--stream", action="store_true", help="Stream output")
    
    # Code
    code = subparsers.add_parser("code", help="Code generation")
    code.add_argument("task", help="Task description")
    code.add_argument("--context", help="Code context")
    code.add_argument("--language", default="python")
    
    # Chat
    chat = subparsers.add_parser("chat", help="Chat mode")
    chat.add_argument("message", help="User message")
    chat.add_argument("--context", help="Additional context")
    chat.add_argument("--system", help="System prompt")
    
    # Preset
    preset = subparsers.add_parser("preset", help="Use a preset task")
    preset.add_argument("name", choices=list(PRESETS.keys()))
    preset.add_argument("--context", required=True, help="Code to process")
    preset.add_argument("--target-lang", help="Target language (for translate)")
    
    args = parser.parse_args()
    
    try:
        client = CerebrasClient(model=args.model)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    if args.command == "complete":
        if args.stream:
            async for chunk in client.stream(args.prompt, system=args.system):
                print(chunk, end="", flush=True)
            print()
        else:
            result = await client.complete(args.prompt, system=args.system)
            print(result)
    
    elif args.command == "code":
        result = await client.code(args.task, context=args.context, language=args.language)
        print(result)
    
    elif args.command == "chat":
        prompt = args.message
        if args.context:
            prompt = f"Context:\n{args.context}\n\n{args.message}"
        result = await client.complete(prompt, system=args.system)
        print(result)
    
    elif args.command == "preset":
        preset_prompt = PRESETS[args.name]
        if "{target_lang}" in preset_prompt:
            preset_prompt = preset_prompt.format(target_lang=args.target_lang or "TypeScript")
        
        prompt = f"{preset_prompt}\n\n```\n{args.context}\n```"
        result = await client.complete(prompt, temperature=0.3)
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
