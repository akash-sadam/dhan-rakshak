"""Pre-recorded and scripted Indian telephony fraud scenarios for Dhan-Rakshak demonstration.
Includes realistic code-mixed Tenglish and Hinglish dialogue turns.
"""

from typing import List
from backend.app.schemas.fraud_schema import CallScenario, ScenarioDialogueTurn


SCENARIOS_DATA: List[CallScenario] = [
    CallScenario(
        id="digital_arrest",
        name="🚨 Digital Arrest / Police Extortion",
        description="Impersonation of Maharashtra Police & CBI claiming narcotics parcel in elder's name.",
        scheme="DIGITAL_ARREST",
        target_score=98,
        audio_sample_url="/samples/scenario_digital_arrest.wav",
        dialogue=[
            ScenarioDialogueTurn(
                time_offset=1.5,
                speaker="caller",
                text="Sunye, main Maharashtra Police Cyber Cell se Inspector Shinde bol raha hoon. Aapke Aadhaar card pe Mumbai airport par illegal narcotics parcel pakda gaya hai.",
                language="hi-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=5.0,
                speaker="senior",
                text="Entandi? Police aa? Nenu eppudu Mumbai vellaledu babu, naaku em sambandham ledu...",
                language="te-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=8.5,
                speaker="caller",
                text="Aapke naam pe Supreme Court se arrest warrant issue hua hai. Turant Skype video call pe aaiye aur ₹50,000 security clearance fee jama kijiye, warna police ghar aayegi!",
                language="hi-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=12.5,
                speaker="senior",
                text="Ayyo babu! Naa daggara antha dabbu lede... arrest chestarani bayam esthundi!",
                language="te-IN"
            )
        ]
    ),
    CallScenario(
        id="power_cut",
        name="⚡ Electricity Disconnection Fraud",
        description="Fake TSSPDCL power officer threatening immediate electricity cut within 1 hour.",
        scheme="UTILITY_CUT",
        target_score=94,
        audio_sample_url="/samples/scenario_power_cut.wav",
        dialogue=[
            ScenarioDialogueTurn(
                time_offset=1.5,
                speaker="caller",
                text="Dear consumer, aapka TSSPDCL current bill update nahi hua hai. Aaj raat 9:30 baje aapka meter connection permanently cut ho jayega.",
                language="hi-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=4.8,
                speaker="senior",
                text="Nenu poyina vaaram bill kattesaane babu, Mee office lo check cheyandi!",
                language="te-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=8.0,
                speaker="caller",
                text="Server update nahi hua. Lineman nikal chuka hai! Turant main jo SMS link bhej raha hoon, usme ₹1,450 online pay kijiye warna line disconnect hogi.",
                language="hi-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=11.5,
                speaker="senior",
                text="Ee link meeda payment ela cheyali babu? Naaku online cheyatam radhe...",
                language="te-IN"
            )
        ]
    ),
    CallScenario(
        id="kyc_expiry",
        name="🏦 Urgent Bank KYC & APK Fraud",
        description="Fake SBI fraud alert threatening account freeze unless senior installs remote APK.",
        scheme="KYC_EXPIRY",
        target_score=91,
        audio_sample_url="/samples/scenario_kyc_expiry.wav",
        dialogue=[
            ScenarioDialogueTurn(
                time_offset=1.5,
                speaker="caller",
                text="Attention! SBI customer care se bol rahe hain. Aapka pension account KYC update expire ho gaya hai, 2 ghante mein account freeze ho jayega.",
                language="hi-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=5.2,
                speaker="senior",
                text="Account freeze aa? Naa monthly pension dabbu andulo ne vundi babu, em cheyali?",
                language="te-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=8.8,
                speaker="caller",
                text="Branch jaane ki zaroorat nahi. Main ek verification APK bhej raha hoon, turant install kijiye aur phone pe aaya 6-digit OTP bataiye.",
                language="hi-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=12.2,
                speaker="senior",
                text="OTP naaku SMS lo vachindi babu... meeku cheppala?",
                language="te-IN"
            )
        ]
    ),
    CallScenario(
        id="benign_family",
        name="🟢 Benign Family Conversation",
        description="Granddaughter calling grandfather to check on health and weekend visit plans (0% Threat Test).",
        scheme="BENIGN",
        target_score=4,
        audio_sample_url="/samples/scenario_benign_family.wav",
        dialogue=[
            ScenarioDialogueTurn(
                time_offset=1.5,
                speaker="caller",
                text="Namaskaram Thatha garu! Ela vunnaru? Blood pressure tablets tinnara?",
                language="te-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=4.5,
                speaker="senior",
                text="Namaskaram Divya thalli! Bagunnanamma, ippude tablet vesa. Weekend pandaga ki intiki vasthunnava?",
                language="te-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=7.8,
                speaker="caller",
                text="Avunu Thatha, Saturday morning train ki vasthunna. Mee kosam sugar-free sweets thestha!",
                language="te-IN"
            ),
            ScenarioDialogueTurn(
                time_offset=10.5,
                speaker="senior",
                text="Manchidi thalli, jagratha ga ra. Amma nanna ki cheppu.",
                language="te-IN"
            )
        ]
    )
]


def get_scenario_by_id(scenario_id: str) -> CallScenario:
    for s in SCENARIOS_DATA:
        if s.id == scenario_id:
            return s
    return SCENARIOS_DATA[0]
