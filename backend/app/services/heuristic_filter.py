"""Fast-path heuristic keyword & regex filter (<20ms execution time).
Identifies preliminary coercion vectors and suspicious tokens before deep MoE reasoning.
"""

import re
import time
from typing import Dict, List, Optional, Tuple


# Pre-compiled high-priority pattern matrices for Indic/English telephony fraud
FRAUD_PATTERNS = {
    "DIGITAL_ARREST": [
        r"\b(cbi|cyber\s*cell|crime\s*branch|police|customs|narcotics)\b",
        r"\b(arrest\s*warrant|warrant|fir|jail|illegal\s*parcel|drugs)\b",
        r"\b(aadhaar\s*misuse|money\s*laundering|terror\s*funding)\b",
        r"\b(digital\s*arrest|video\s*call\s*pe\s*aao|skype|camera\s*on)\b",
        r"\b(court\s*order|supreme\s*court|dcp|inspector)\b",
        r"\b(verification\s*fee|security\s*deposit|clearance\s*fee)\b",
        r"\b(police\s*ghar\s*aayegi|arrest\s*chestaru|jail\s*lo\s*pedataru)\b"
    ],
    "UTILITY_CUT": [
        r"\b(electricity|bijli|power\s*cut|current\s*bill|line\s*cut)\b",
        r"\b(meter\s*disconnection|power\s*department|tsspdcl|bescom)\b",
        r"\b(bill\s*pending|unpaid\s*bill|officer\s*sharma|lineman)\b",
        r"\b(urgent\s*ga\s*payment|turant\s*pay|link\s*meeda\s*payment)\b",
        r"\b(within\s*1\s*hour|aaj\s*raat\s*9\s*baje|power\s*off)\b"
    ],
    "KYC_EXPIRY": [
        r"\b(kyc\s*expiry|kyc\s*update|account\s*block|account\s*freeze)\b",
        r"\b(pan\s*card\s*link|sbi|hdfc|icici|axis\s*bank)\b",
        r"\b(apk\s*install|download\s*app|anydesk|teamviewer|rustdesk)\b",
        r"\b(otp\s*batao|share\s*otp|otp\s*pampandi|cvv)\b",
        r"\b(atm\s*block|debit\s*card\s*deactivate)\b"
    ],
    "LOTTERY_REWARD": [
        r"\b(lottery|cashback|kbc|kaun\s*banega|won\s*prize|reward)\b",
        r"\b(processing\s*charge|tax\s*amount|claim\s*amount)\b"
    ]
}

URGENCY_KEYWORDS = [
    "turant", "urgent", "ventane", "immediately", "right now", "warna",
    "police ghar aayegi", "arrest chestaru", "jail", "within 1 hour",
    "aaj raat", "final notice", "strictly confidential", "phone mat kaatna"
]

BENIGN_INDICATORS = [
    r"\b(namaskaram|bagunara|babu|amma|tinnava|pandaga|weekend|dinner|lunch)\b",
    r"\b(grandpa|dadaji|nana|illu|home|health|tablet|hospital|doctor\s*appointment)\b"
]


class FastHeuristicFilter:
    """Ultra-fast regex filter that triggers in <20ms."""

    def __init__(self):
        self.compiled_patterns = {
            scheme: [re.compile(p, re.IGNORECASE) for p in patterns]
            for scheme, patterns in FRAUD_PATTERNS.items()
        }
        self.compiled_urgency = [re.compile(re.escape(k), re.IGNORECASE) for k in URGENCY_KEYWORDS]
        self.compiled_benign = [re.compile(p, re.IGNORECASE) for p in BENIGN_INDICATORS]

    def scan_transcript(self, text: str) -> Dict:
        start_time = time.perf_counter()
        clean_text = text.lower().strip()

        matched_schemes: Dict[str, int] = {}
        detected_clues: List[str] = []

        # Check fraud patterns
        for scheme, patterns in self.compiled_patterns.items():
            scheme_matches = 0
            for pat in patterns:
                matches = pat.findall(clean_text)
                if matches:
                    scheme_matches += len(matches)
                    for m in matches:
                        match_str = m if isinstance(m, str) else m[0]
                        if match_str and match_str not in detected_clues:
                            detected_clues.append(match_str)
            if scheme_matches > 0:
                matched_schemes[scheme] = scheme_matches

        # Check urgency
        urgency_matches = 0
        for pat in self.compiled_urgency:
            matches = pat.findall(clean_text)
            if matches:
                urgency_matches += len(matches)
                for m in matches:
                    if m not in detected_clues:
                        detected_clues.append(m)

        # Check benign indicators
        benign_matches = 0
        for pat in self.compiled_benign:
            matches = pat.findall(clean_text)
            if matches:
                benign_matches += len(matches)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # Preliminary scoring calculation
        if not matched_schemes and benign_matches > 0:
            return {
                "flagged": False,
                "preliminary_score": max(0, 10 - benign_matches * 5),
                "top_scheme": "BENIGN",
                "detected_clues": [],
                "urgency_matches": 0,
                "latency_ms": elapsed_ms
            }

        if matched_schemes:
            top_scheme = max(matched_schemes.items(), key=lambda x: x[1])[0]
            total_matches = sum(matched_schemes.values())
            # Heuristic preliminary score base
            score = min(95, 45 + (total_matches * 15) + (urgency_matches * 10))
            return {
                "flagged": score >= 50,
                "preliminary_score": score,
                "top_scheme": top_scheme,
                "detected_clues": detected_clues[:6],
                "urgency_matches": urgency_matches,
                "latency_ms": elapsed_ms
            }

        return {
            "flagged": False,
            "preliminary_score": 5,
            "top_scheme": "BENIGN",
            "detected_clues": [],
            "urgency_matches": 0,
            "latency_ms": elapsed_ms
        }


heuristic_filter = FastHeuristicFilter()
