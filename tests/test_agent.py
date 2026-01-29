#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LUCIA Agent Integration Test & Scenario Runner

This script performs an integration test for the `root_agent` by simulating a 
multi-turn conversation with a specific user persona. It validates the agent's 
ability to handle context, empathy, and medical reasoning.

Scenario:
    The test simulates a female patient describing symptoms indicative of an 
    autoimmune condition (stiff joints, fatigue) who has faced potential 
    medical gaslighting (symptoms dismissed as perimenopause/anxiety).

Key Features:
    - **Session Management**: Uses `InMemorySessionService` to maintain 
      conversational state across multiple queries.
    - **ADK Runner**: Utilizes the Google ADK `Runner` to execute the 
      `root_agent` asynchronously.
    - **Response Handling**: Captures and prints both intermediate events 
      and the final response for verification.

Usage:
    Run this script from the project root:
    $ python -m tests.test_agent

Dependencies:
    - google.adk
    - google.genai
    - main_agent.agent

Original Author: inna campo
Created: Mon Nov 17 2025
"""
import asyncio
import uuid
from dotenv import load_dotenv
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from main_agent.agent import root_agent
from google.genai import types as genai_types
import warnings
warnings.filterwarnings("ignore")
APP_NAME = "LUCIA"  # Application

async def main():
    session_id = str(uuid.uuid4())
    """Runs the agent with a sample query."""
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="agents", user_id="test_user", session_id=session_id
    )
    print (session_id)
    runner = Runner(
        agent=root_agent, app_name="agents", session_service=session_service
    )
    
    queries = [
        "I've been waking up with stiff, swollen joints in my hands and feet for three months. The fatigue is so bad I have to nap in my car at lunch.",
        "I saw a new doctor today. I tried to show him the swelling, but he barely looked. He told me that at 48, this is just classic perimenopause and 'empty nest syndrome' making me depressed.",
        "He didn't order any blood work. He just told me to lose 10 pounds and try meditation to calm my 'nerves' because women get so anxious at this stage of life."   
        ]

    for index, query in enumerate(queries):
        print(f"\nUser, query #{index} > {query}")
        
        # 1. Create a variable to hold the final report
        final_report = None

        # 2. Loop through events to find and store the final response
        async for event in runner.run_async(
            user_id="test_user",
            session_id=session_id,
            new_message=genai_types.Content(
                role="user", 
                parts=[genai_types.Part.from_text(text=query)]
            ),
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print(f"{APP_NAME}, query #{index} > ", event.content.parts[0].text)
                final_report = event.content.parts[0].text

        # 3. Print the stored report only once, after the agent is done
    if final_report:
        print("\n\n Final Report \n\n")
        print(f"{APP_NAME} > ", final_report)
            
if __name__ == "__main__":
    asyncio.run(main())
