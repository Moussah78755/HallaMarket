# MarketMinder AI 🌾🛒

**Empowering Bamenda’s Traders and Farmers through AI-Driven Supply Chain Resilience.**

MarketMinder AI is an intelligent coordination platform designed to rescue the disrupted agricultural supply chains of the North West Region of Cameroon. Due to unpredictable ghost towns, curfews, and sudden lockdowns, vital food supplies (like Irish potatoes from Santa and maize from Balikumbat) frequently rot in transit, leaving women traders ("Bayamsellams") and local farmers absorbing devastating financial losses. 

This project makes this invisible crisis visible. By pairing advanced AI capabilities with low-tech accessibility channels (WhatsApp and SMS/USSD), MarketMinder AI provides real-time market safety predictions, coordinates supply-demand matching, and digitizes inventory management.

---

## ✨ Key Features

* **🎙️ Pidgin Voice-to-Inventory AI (Accessibility First):** Rural farmers and market women can send WhatsApp voice notes in local Pidgin English detailing their harvests (e.g., *"I get 5 bags of potato for Santa"*). The system uses an LLM-powered backend to parse the audio and automatically structure it into digital inventory data.
* **🔮 Predictive Market Status & Safety Alerts:** An AI agent aggregates public digital channels, local community reports, and news text to predict market access levels for major hubs like the **Bamenda Main Market** and **Mile 6 Market**, giving farmers a reliable "Go/No-Go" safety signal before they travel.
* **📊 Intelligent Supply-Demand Matching:** Predicts localized food gluts and shortages, automatically matching stranded farmers with alternative bulk buyers, storage facilities, or safer neighborhood markets.
* **🗺️ Analytical Logistics Dashboard:** A central dashboard for agricultural cooperatives and local management to visually track regional supply blockages, food waste hotspots, and trade volume metrics.

---

## 🛠️ Tech Stack

* **AI/LLM Core:** Google Gemini API (for structuring unstructured Pidgin voice/text inputs and processing sentiment analysis for market safety).
* **Backend:** Python, FastAPI / Node.js
* **Database:** PostgreSQL / Firebase (to track real-time inventory, user locations, and market metrics)
* **Frontend Channels:** * *User-facing:* Twilio API (for WhatsApp Business Automation / SMS Gateway integration)
    * *Admin-facing:* React.js / Tailwind CSS (for the analytical mapping dashboard)

---

## 🚀 How It Works

1. **Inventory Logging:** A farmer in Santa sends a WhatsApp voice note stating what they have ready. 
2. **AI Processing:** Gemini processes the text/audio, extracts the crop, quantity, and location, and updates the central database.
3. **Safety & Match Verification:** The AI checks current safety signals for the target market. If safe, a dispatch note is created. If blocked, the system alerts the farmer and suggests an alternative local cooperative or buyer.
4. **Data Visualization:** The local dashboard maps out active supply lines and flags high-risk or high-waste areas.

---

## 💻 Getting Started

### Prerequisites
* Python 3.10+ or Node.js v18+
* Google Gemini API Key
* Twilio Account (for WhatsApp/SMS integration)

### Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Moussah78755/HallaMarket.git
   cd HallaMarket
   ```
