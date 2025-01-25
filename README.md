#🌌 Aurora Tracker
Automated Northern Lights visibility notification script using NOAA forecast data.

##🚀 Features
Real-time aurora forecast tracking
Kp index monitoring
Daily scheduled notifications
Logging support
🛠 Prerequisites
Python 3.x
requests library

##🔧 Installation

```bash
git clone https://github.com/yourusername/aurora-tracker.git
cd aurora-tracker
pip install requests
```

##⚙️ Configuration
Edit script constants:

KP_THRESHOLD: Kp index threshold (default: 5)
CHECK_TIME: Daily check time (default: "20:30")
Update recipient email in send_notification()

##🏃 Usage

python aurora_tracker.py

##📋 Logging
Comprehensive logging tracks script operations and data processing.

##⚠️ Limitations
Requires internet connection
Pseudo-email notification
Depends on NOAA data availability

##📄 License
[Your License Here]
