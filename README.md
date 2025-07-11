# Intel Unnati Healthcare Kiosk – README

## Table of Contents
1. Project Overview  
2. Core Features  
3. System Architecture  
4. Hardware Reference Design  
5. Software Stack  
6. Getting Started  
7. Repository Structure  
8. Roadmap  
9. Contributing  
10. License  

## 1. Project Overview
The Intel Unnati Healthcare Kiosk project delivers an **AI-enabled, self-service point of care** that can operate in rural or urban clinics, corporate campuses, and community centers.  
Key objectives:

* Bring basic diagnostics to underserved areas.  
* Integrate seamlessly with India’s Ayushman Bharat Digital Mission (ABDM).  
* Preserve patient privacy through on-device federated learning.  
* Support 22 + Indian languages for inclusive digital health access.

## 2. Core Features
| Module | Purpose | Highlights |
|--------|---------|-----------|
| **FedHealth-AI** | Privacy-preserving federated learning | No raw data leaves the kiosk; models are aggregated securely on the edge cloud. |
| **BharatHealth-GPT** | Multilingual virtual assistant | Real-time symptom triage in 22+ languages, offline fall-back, text-to-speech support. |
| **Vitals CV** | Contact-free vital-sign capture | Heart-rate and respiratory-rate estimation via camera; integrates with standard peripherals for SpO₂, BP, etc. |
| **ABDM Connector** | National health stack compliance | ABHA ID verification, encrypted EHR push/pull, DigiLocker and e-Sign integration. |

## 3. System Architecture
```
┌───────────┐   Local Inference   ┌──────────────┐
│  Kiosk    │────────────────────▶│  Edge Model  │
│  (12th Gen│   Gradient Updates  │  Aggregator  │
│   Intel)  │◀────────────────────│ (Federated)  │
└───────────┘                    └──────────────┘
       │                                   │
       │ Secure APIs                       │
       ▼                                   ▼
┌──────────────┐                   ┌────────────────┐
│ ABDM Gateway │◀──────────────────│  Cloud Portal  │
└──────────────┘   Encrypted EHR   └────────────────┘
```
*Front-end*: React web app on kiosk touchscreen  
*Back-end*: FastAPI micro-services, gRPC between services  
*Model Ops*: TensorFlow Federated + OpenVINO runtime  

## 4. Hardware Reference Design
* Intel Core i5-12400, 16 GB RAM, 512 GB NVMe SSD  
* 21.5-inch FHD capacitive touchscreen, IP65 front panel  
* 4 K RGB-IR camera, fingerprint reader, thermal printer, barcode scanner  
* Connectivity: 5G/4G modem, Wi-Fi 6, Bluetooth 5.2, Gigabit LAN  
* Power: 65 W TDP, 4-hour UPS, optional solar kit  

## 5. Software Stack
| Layer / Purpose | Technologies |
|-----------------|--------------|
| OS / Container  | Ubuntu 22.04, Docker, *optional* Kubernetes |
| AI / ML         | TensorFlow 2.x, PyTorch 2.x, OpenVINO, TensorFlow Federated |
| NLP             | AI4Bharat IndicBERT, Hugging Face Transformers |
| CV              | OpenCV-Python |
| Data            | MongoDB, Redis (cache), InfluxDB (time-series) |
| API             | FastAPI (REST), GraphQL |
| Security        | AES-256 at rest, TLS 1.3 in transit, FIDO2 / WebAuthn |

## 6. Getting Started

### 6.1 Prerequisites
* Python 3.9+  
* Git, Docker (optional for container build)  
* VS Code or any Python IDE  

### 6.2 Clone and Set Up
```bash
git clone https://github.com/your-org/intel-unnati-health-kiosk.git
cd intel-unnati-health-kiosk
python -m venv venv
venv\Scripts\activate      # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

### 6.3 Running a Local Demo
```bash
# Start FastAPI server
python src/backend/main.py

# Launch kiosk UI (React)
cd src/frontend
npm install
npm start
```

### 6.4 Testing Multilingual AI
```python
from src.models.bharathealth_gpt import BharatHealthGPT
bot = BharatHealthGPT()
print(bot.process_query("Mujhe bukhar hai", language="hi"))
```

## 7. Repository Structure
<pre>
```
.
├── docs/                 # Design docs, architecture diagrams
├── hardware/             # BOM, enclosure CAD, PCB schematics
├── src/
│   ├── backend/          # FastAPI services, DB models
│   ├── frontend/         # React kiosk UI
│   └── models/           # AI/ML code, training scripts
├── tests/                # Unit and integration tests
├── requirements.txt
└── README.md             # This file
```
</pre>


## 8. Contributing
1. Fork the repo and create your branch (`git checkout -b feature/name`).  
2. Commit your changes (`git commit -m "Add feature"`).  
3. Push to the branch (`git push origin feature/name`).  
4. Open a pull request describing your changes.

Please run `pre-commit run --all-files` before submitting PRs.

## 9. License
This project is released under the **MIT License**. See `LICENSE` for details.

_© 2025 Intel Unnati Healthcare Kiosk Project_