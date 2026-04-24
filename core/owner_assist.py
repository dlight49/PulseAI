import os
import json
import sys
from core.whatsapp_webhook import send_whatsapp_message
from core.ai_brain import load_state, save_state

def approve_messages():
    """CLI tool for the owner to approve or edit pending AI messages."""
    base_path = r"C:\Users\Omola\PulseAI\data\states"
    if not os.path.exists(base_path):
        print("No pending messages found.")
        return

    while True:
        pending_files = [f for f in os.listdir(base_path) if f.endswith('.json')]
        active_pending = []
        
        for file in pending_files:
            sender = file.replace('.json', '')
            state = load_state(sender)
            if state.get('pending_approval'):
                active_pending.append((sender, state))

        if not active_pending:
            print("\n☕ No more pending messages. All caught up!")
            break

        print(f"\n--- 📢 {len(active_pending)} Pending Message(s) ---")
        for i, (sender, state) in enumerate(active_pending):
            print(f"[{i}] From: {sender} | Last Msg: {state['history'][-1]['content'][:50]}...")

        choice = input("\nSelect [index] to review, or 'q' to quit: ")
        if choice.lower() == 'q':
            break
        
        try:
            idx = int(choice)
            sender, state = active_pending[idx]
            suggestion = state['pending_approval']
            
            print(f"\n--------------------------------------------------")
            print(f"MASTER CLOSER SUGGESTION for {sender}:")
            print(f"--------------------------------------------------")
            print(suggestion)
            print(f"--------------------------------------------------")
            
            action = input("\n[a] Approve | [e] Edit | [d] Discard: ").lower()
            
            if action == 'a':
                # Send the message
                if send_whatsapp_message(sender, suggestion):
                    state['history'].append({"role": "assistant", "content": suggestion})
                    state['pending_approval'] = None
                    save_state(sender, state)
                    print("✅ Approved and Sent!")
            
            elif action == 'e':
                new_msg = input("Type your new message: ")
                if send_whatsapp_message(sender, new_msg):
                    state['history'].append({"role": "assistant", "content": new_msg})
                    state['pending_approval'] = None
                    save_state(sender, state)
                    print("✅ Edited and Sent!")
            
            elif action == 'd':
                state['pending_approval'] = None
                save_state(sender, state)
                print("🗑️ Discarded.")
                
        except (ValueError, IndexError):
            print("Invalid selection.")

if __name__ == "__main__":
    approve_messages()
