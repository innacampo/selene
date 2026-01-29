# SELENE Integration Tests

This directory contains integration scenarios to validate the `root_agent` orchestration logic, specifically testing the interaction between the **Symptom Mapper**, **Bias Analyzer**, and **Advocacy Generator**.

## The Test Scenario: "The Perimenopause Dismissal"

The `test_agent.py` script runs a multi-turn simulation designed to stress-test the agent's ability to detect "Diagnostic Shadowing."

**The Persona:**
* **User:** 48-year-old female.
* **Symptoms:** Joint swelling, stiffness, extreme fatigue (Autoimmune indicators).
* **Provider Interaction:** Dismissed as "perimenopause" and "empty nest syndrome"; symptoms attributed to anxiety ("nerves").

**What this test validates:**
1.  **Symptom Mapping:** Does Agent 1 capture "joint swelling" while ignoring the doctor's "anxiety" label?
2.  **Bias Detection:** Does Agent 2 flag "Ageism" and "Gender Bias" using the AXIOM tool?
3.  **Statefulness:** Does the agent maintain context across 3 distinct user messages?

## How to Run

Execute the test module from the **project root** directory:

```bash
python -m tests.test_agent
```

## **Expected Output**

The script will stream the agent's thought process to the console. You should look for:

1. **User Queries:** Three sequential inputs simulating the narrative.  
2. **Intermediate Steps:** Logs showing the tool calls to `get_bias_implications`.  
3. **Final Report:** A structured text block titled **"Patient Advocacy & Consultation Aid"**.

## **Troubleshooting**

If the test fails immediately, ensure your environment variables are set:

1. Check that your `.env` file exists in the root directory.  
2. Ensure `GOOGLE_API_KEY` is valid.
