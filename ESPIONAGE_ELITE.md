# 🕵️♂️ Espionage Elite - Sock Spy Operatives Dossier

[![Active Operatives](https://img.shields.io/badge/AGENTS_IN_FIELD-12-blueviolet?logo=spy)](https://github.com/Kanarath/Sock_Spy)
[![Completed Missions](https://img.shields.io/badge/TOTAL_MISSIONS-42-success)](CONTRIBUTING.md)

## 🔍 Rank Hierarchy (2 Missions Per Promotion)
| Rank              | Missions Required | Badge                                                                 |
|--------------------|-------------------|-----------------------------------------------------------------------|
| **Recruit**        | 1-2               | ![](https://img.shields.io/badge/Recruit-🔍-lightgrey)               |
| **Field Agent**    | 3-4               | ![](https://img.shields.io/badge/Field_Agent-📡-9cf)                 |
| **Master Spy**     | 5-6               | ![](https://img.shields.io/badge/Master_Spy-📟-orange)               |
| **Chief Handler**  | 7+                | ![](https://img.shields.io/badge/Chief_Handler-💼-red)               |

## 🥇 Active Operatives Leaderboard

| Rank | Agent Profile | Missions | Current Badge                        |
|------|---------------|----------|--------------------------------------|
| 1    | [![@codeweaver](https://img.shields.io/badge/Agent-codeweaver-00FF00?logo=github)](https://github.com/codeweaver) | 8 | ![](https://img.shields.io/badge/Chief_Handler-💼-red) |
| 2    | [![@datasleuth](https://img.shields.io/badge/Agent-datasleuth-FFA500?logo=keybase)](https://keybase.io/datasleuth) | 5 | ![](https://img.shields.io/badge/Master_Spy-📟-orange) |
| 3    | [![@localizeit](https://img.shields.io/badge/Agent-localizeit-FF00FF?logo=globe)](https://github.com/localizeit) | 3 | ![](https://img.shields.io/badge/Field_Agent-📡-9cf) |

## 🧩 How to Join the Elite?
1. Complete missions (PR merges)
2. Earn badges based on mission count
3. Appear on this leaderboard
[See mission protocol](contributing.md)

---

## 🔄 Promotion Tracker
**Next Rank Requirements**
```python
def show_progress(missions):
    next_rank = "Chief Handler" if missions >=7 else "Master Spy" if missions >=5 else "Field Agent"
    needed = 2 - (missions % 2)
    return f"Agent needs {needed} more mission(s) to reach {next_rank} rank"

print(show_progress(3))  # Output: "Agent needs 1 more mission(s) to reach Field Agent rank"
```
---

## 🗂️ Operative Dossier Template

### [Your Code Name]
**Real Identity**: [Optional Name/Link]
**Specialization**: [Localization/Code/Intel]
**Active Since**: Month 2024

**Notable Missions**:
- Mission #23: Spanish localization patterns
- Mission #42: Validation system upgrade

**Contact Protocol**:
[![Preferred Contact](https://img.shields.io/badge/Contact_Me-Platform-COLOR?logo=PLATFORM)](LINK) 
