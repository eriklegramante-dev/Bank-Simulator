# 🏦 Banco Nester - ATM Simulator

A professional ATM (Automated Teller Machine) simulator built with **Python** and the **Streamlit** framework. This project focuses on business logic implementation, session state management, and security auditing practices through logging.

## 🚀 Features

- **Secure Authentication**: Login system using card numbers and passwords.
- **Security Lockout**: Automatic card blocking after 3 consecutive failed login attempts.
- **Operations Dashboard**:
  - 💸 **Withdrawal**: Includes balance validation and password confirmation.
  - 📲 **Transfer**: Send funds between accounts registered in the system's engine.
  - 📄 **Statement (Extrato)**: Real-time transaction history extracted directly from system log files.
- **Security Auditing (Logs)**: All operations (success, failure, or lockout) are recorded in `.log` files with timestamps, following security monitoring best practices.

## 🛠️ Technologies Used

- [Python](https://www.python.org/) - Core language.
- [Streamlit](https://streamlit.io/) - Web interface framework.
- [Logging](https://docs.python.org/3/library/logging.html) - Event auditing and recording.
- [OS & Time](https://docs.python.org/3/library/os.html) - File manipulation and flow control.

## 📁 Project Structure

```text
.
├── main.py           # Streamlit interface and flow control
├── engine.py         # Business logic and "database" (ATM Engine)
├── logs/             # Directory where system events are recorded
│   └── atm.log
├── .gitignore        # Git configuration to ignore venv and logs
└── README.md         # Project documentation

```
## ⚙️ How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/eriklegramante-dev/banco-nester.git](https://github.com/eriklegramante-dev/banco-nester.git)
   cd banco-nester

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**:
   ```bash
   pip install streamlit

4. **Run the application**:
   ```bash
   streamlit run src/main.py


## 🛡️ Security Focus (Study Case)
This project was developed as a case study for logic applied to financial systems and information security. Key concepts explored include:

- **Input Sanitization: Methods used to clean data entries.**
- **State Management: Data persistence across page refreshes.**

- **Event Logging: Recording intrusion attempts and authentication failures for forensic analysis.**

-----------------------------------------
## Developed by Erik Legramante