# Graph Report - C:\Users\Omola\PulseAI  (2026-04-23)

## Corpus Check
- 12 files · ~33,278 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 47 nodes · 48 edges · 11 communities detected
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]

## God Nodes (most connected - your core abstractions)
1. `get_ai_response()` - 8 edges
2. `load_state()` - 5 edges
3. `save_state()` - 5 edges
4. `approve_messages()` - 5 edges
5. `get_state_path()` - 4 edges
6. `send_whatsapp_message()` - 4 edges
7. `process_buffered_message()` - 4 edges
8. `WhatsAppWebhookHandler` - 4 edges
9. `OAuthHandler` - 3 edges
10. `create_payment_link()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `load_state()` --calls--> `approve_messages()`  [INFERRED]
  C:\Users\Omola\PulseAI\core\ai_brain.py → C:\Users\Omola\PulseAI\core\owner_assist.py
- `save_state()` --calls--> `approve_messages()`  [INFERRED]
  C:\Users\Omola\PulseAI\core\ai_brain.py → C:\Users\Omola\PulseAI\core\owner_assist.py
- `get_ai_response()` --calls--> `load_business_data()`  [INFERRED]
  C:\Users\Omola\PulseAI\core\ai_brain.py → C:\Users\Omola\PulseAI\core\persona_engine.py
- `get_ai_response()` --calls--> `get_business_prompt_context()`  [INFERRED]
  C:\Users\Omola\PulseAI\core\ai_brain.py → C:\Users\Omola\PulseAI\core\persona_engine.py
- `get_ai_response()` --calls--> `create_payment_link()`  [INFERRED]
  C:\Users\Omola\PulseAI\core\ai_brain.py → C:\Users\Omola\PulseAI\core\payment.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.33
Nodes (8): get_ai_response(), get_state_path(), load_state(), Returns the path to the state file for a sender., Loads the conversation state for a sender, ensuring all keys exist., Saves the conversation state for a sender., Pulse AI Master Brain (The Master Closer v2.2).     Focuses on: Natural Variety, save_state()

### Community 1 - "Community 1"
Cohesion: 0.25
Nodes (6): approve_messages(), CLI tool for the owner to approve or edit pending AI messages., process_buffered_message(), Sends a message via the Meta WhatsApp Cloud API., Wait period over. Actually call the AI brain and reply., send_whatsapp_message()

### Community 2 - "Community 2"
Cohesion: 0.25
Nodes (3): OAuthHandler, BaseHTTPRequestHandler, WhatsAppWebhookHandler

### Community 3 - "Community 3"
Cohesion: 0.4
Nodes (4): get_business_prompt_context(), load_business_data(), Formats business data into a context string for the AI., Loads business data from a JSON file.

### Community 4 - "Community 4"
Cohesion: 0.5
Nodes (2): FileSystemEventHandler, PulseHandler

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (2): create_payment_link(), Creates a Paystack payment page link.     Amount should be in Naira (converted

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (0): 

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (0): 

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (0): 

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (0): 

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **10 isolated node(s):** `Returns the path to the state file for a sender.`, `Loads the conversation state for a sender, ensuring all keys exist.`, `Saves the conversation state for a sender.`, `Pulse AI Master Brain (The Master Closer v2.2).     Focuses on: Natural Variety`, `CLI tool for the owner to approve or edit pending AI messages.` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 6`** (2 nodes): `list_models.py`, `list_compatible_models()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (2 nodes): `whatsapp_pulse.py`, `send_whatsapp()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (2 nodes): `pitch_generator.py`, `generate_pitch()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (2 nodes): `researcher.py`, `find_prospects()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (1 nodes): `eye.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_ai_response()` connect `Community 0` to `Community 1`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.289) - this node is a cross-community bridge._
- **Why does `process_buffered_message()` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.188) - this node is a cross-community bridge._
- **Why does `WhatsAppWebhookHandler` connect `Community 2` to `Community 1`?**
  _High betweenness centrality (0.186) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `get_ai_response()` (e.g. with `load_business_data()` and `get_business_prompt_context()`) actually correct?**
  _`get_ai_response()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `approve_messages()` (e.g. with `load_state()` and `send_whatsapp_message()`) actually correct?**
  _`approve_messages()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Returns the path to the state file for a sender.`, `Loads the conversation state for a sender, ensuring all keys exist.`, `Saves the conversation state for a sender.` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._