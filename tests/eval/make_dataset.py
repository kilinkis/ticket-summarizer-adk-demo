"""Builds datasets/tickets-dataset.json. All data is invented (test card/IBAN numbers, .test emails, 555 phones).

Each case's `reference` holds the key-fact keywords: ';' separates required facts,
'|' separates acceptable synonyms for one fact.
"""
import json
from pathlib import Path

TICKETS = [
    ("card_double_charge",
     "Hello, my card 4111 1111 1111 1111 was charged twice for the same order on 2026-10-28, EUR 89.90 each time. "
     "Please refund the duplicate charge as soon as possible, I am short on money this week.",
     "twice|double|duplicate;refund"),
    ("iban_wrong_payout",
     "Our weekly payout of EUR 4,310.00 went to the wrong account. The IBAN on file should end 0130 00 but "
     "the money was sent to DE89 3704 0044 0532 0130 00 instead. We need the payout re-sent to the right IBAN GB29 NWBK 6016 1331 9268 19. "
     "This is blocking our payroll on Friday.",
     "payout;wrong|incorrect;payroll|friday"),
    ("name_phone_callback",
     "Hi, my name is Jonas Testmann. I cannot log in to the merchant dashboard since the password reset. "
     "Please call me back on +44 20 7946 0958 today.\nRegards,\nJonas Testmann",
     "log in|login|dashboard;password;call"),
    ("very_short",
     "Refund pending 3 weeks, still nothing!!",
     "refund;3 weeks|three weeks|pending"),
    ("email_chargeback",
     "I received a chargeback notification for a transaction I never made. Reply to maria.fake@example.test. "
     "The disputed amount is USD 640.00 and the deadline to respond is 2026-11-05. Please tell me how to submit evidence.",
     "chargeback|dispute;evidence;11-05|nov"),
    ("fx_fee_question",
     "Ms. Olivia Notreal here. Why was I charged a 3.5% foreign exchange fee on my GBP to EUR transfer of 2,000 pounds? "
     "The pricing page says 1.5%. No rush, just want an explanation and a correction if it is a mistake.",
     "fee|fx|exchange;1.5|correct|explanation"),
    ("terminal_down_urgent",
     "URGENT: all 4 card terminals in our shop stopped accepting payments at 09:00 this morning, error code E-4021. "
     "We are losing sales every minute. Contact: 0612345678 or ops@shop-example.test. Mr Pieter Fakeman, store manager.",
     "terminal;e-4021|4021|not accepting|stopped;urgent|high"),
]

cases = []
for cid, text, keys in TICKETS:
    cases.append({
        "eval_case_id": cid,
        "prompt": {"role": "user", "parts": [{"text": text}]},
        "reference": {"response": {"role": "model", "parts": [{"text": keys}]}},
    })

out = Path(__file__).parent / "datasets" / "tickets-dataset.json"
out.write_text(json.dumps({"eval_cases": cases}, indent=2) + "\n")
print(f"wrote {len(cases)} cases to {out}")
