# 🧦 Contributing to Sock Spy

🎉 Thank you for considering contributing to **Sock Spy**! Your support helps us maintain a valuable educational tool for OSINT training and awareness.

---

## 📚 Purpose & Scope

Sock Spy is designed **strictly for educational and research purposes**. Its primary goal is to demonstrate how easily fake profiles ("sock puppets") can be created, thereby raising awareness about security vulnerabilities on social media platforms. It's secondary goal is to create fake data profiles for made up study cases, "boxes" or "rooms" to practice OSINT in and for the community.

**Please ensure all contributions align with this mission.**

---

## 🧭 Code of Conduct

We are committed to fostering a welcoming and respectful community. By participating, you agree to uphold our [Code of Conduct](ethical_use_policy.txt).

---

## 🛠️ How to Contribute

Help us make Sock Spy more realistic and educational!

### 🌐 How to Contribute New Localizations

We use .json files for most of the data and .txt files for names and last names.
- for **names and last names** you have to separate them by gender and use only one column with every data key, no comas, no points just raw data in a column.
- for **interests, professions and locations** you have to make a hierarquical key list like this example:

```bash
{
  "Africa": {
    "Nigeria": {
      "Lagos": ["Ikeja", "Victoria Island", "Lekki", "Surulere", "Yaba"],
      "Abuja": ["Garki", "Wuse", "Maitama", "Gwarinpa", "Utako"]
    },
        "South Africa": {
      "Johannesburg": ["Sandton", "Soweto", "Rosebank", "Melville", "Maboneng"],
      "Cape Town": ["Waterfront", "Camps Bay", "Woodstock", "Khayelitsha", "Sea Point"]
    }
  }

```
- When you send the contribution to "PR" make sure it's clear what type of data is it and where belongs.

### 🐛 Reporting Bugs

- **Search existing issues** to avoid duplicates.
- **Provide detailed information**:
  - Steps to reproduce the issue.
  - Expected and actual behavior.
  - Screenshots or logs, if applicable.

### 💡 Suggesting Enhancements

- **Explain the motivation** behind the suggestion.
- **Describe the proposed solution** and its benefits.
- **Consider the educational scope** of the project.

### 📥 Submitting Pull Requests

1. **Fork the repository** and create a new branch.
2. **Implement your changes** with clear and concise code.
3. **Write descriptive commit messages**.
4. **Test your changes** thoroughly.
5. **Ensure compliance** with the project's license and ethical guidelines.
6. **Submit a pull request** with a detailed description of your changes.

---

## 📜 Licensing

By contributing, you agree that your contributions will be licensed under the [GNU General Public License v3.0](license.md), in line with the project's existing license.

---

## ⚖️ Ethical Considerations

Given the sensitive nature of simulation tools, any contribution that:

- Promotes unauthorized access or deceptive behavior outside of a controlled educational environment.
- Encourages bypassing security measures on live social media platforms.
- Enables misuse for invasive data collection.

**will be rejected**.

Contributions must be designed to educate, not to facilitate illegal or unethical actions.

---

## 🙏 Acknowledgment

Thank you for your interest in contributing to Sock Spy. Your efforts help improve the educational experience for users and reinforce the importance of cybersecurity awareness.

If you have any questions or need further clarification, please open an issue on the repository or contact the maintainers.

## 🧵 Become a Digital Weaver

Sock Spy needs your cultural expertise! Help us:
- 🔍 Enhance OSINT investigation realism
- 🎓 Create better educational resources
- 🌐 Preserve digital diversity

**Contributor Benefits:**

✅ **Tangible:**
- Permanent credit in [ESPIONAGE ELITE](ESPIONAGE_ELITE.md)
- GitHub contribution graph recognition

🎯 **Professional:**
- Referenceable work in infosec/OSINT field
- Demonstrable impact (Our user base: X monthly downloads)

🌱 **Learning:**
- Real-world experience
- Python/JSON validation practice