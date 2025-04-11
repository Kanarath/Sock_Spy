1. Portfolio Documentation (OSINT Focus)
Project Title: Sock Spy: Automated Sock Puppet Generation for OSINT
Project Overview:
Sock Spy is a command-line tool designed to streamline the creation of realistic "Sock Puppet" personas for Open Source Intelligence (OSINT) investigations. It automates the process of generating profiles with customizable attributes like name, nationality, age, interests, and platform presence. This allows OSINT researchers to quickly deploy multiple distinct personas for data collection, social network analysis, and online reconnaissance, enhancing their ability to gather valuable intelligence in a controlled and ethical manner.
Problem Addressed:
OSINT investigations often require interacting with online communities and social networks. Creating credible personas manually is a time-consuming and challenging task. Existing methods can be inconsistent, leading to detectable and potentially compromised operations. Sock Spy addresses this challenge by providing a repeatable, customizable, and efficient way to generate realistic personas that can be used ethically and responsibly in OSINT research.
Solution:
Sock Spy provides an interactive command-line interface (CLI) that guides the user through a step-by-step process of creating a "Sock Puppet" persona. Key features include:
Dynamic Data Population: Leverages external data files (names, locations, interests) to create diverse and credible profiles.
Customizable Attributes: Allows fine-grained control over persona characteristics, including gender, nationality, age, and platform presence.
Automated Username Generation: Suggests realistic usernames based on the persona's name and age, improving authenticity.
JSON Export: Exports the complete profile data in JSON format, making it easy to integrate with other OSINT tools and workflows.
Secure Credential Management: While explicitly acknowledging the ethical and legal implications, it allows the user to document created passwords/usernames.
Platform Tracking: Track the usage of the Sock Puppet per each platform so you are able to keep up with the usage of this one.
OSINT Applications:
Social Media Reconnaissance: Gathering data from social media platforms without revealing your true identity.
Forum and Community Monitoring: Infiltrating and monitoring online communities relevant to an investigation.
Data Collection Automation: Creating multiple personas to scrape and collect data from websites and APIs.
Counter-Intelligence: Creating decoy profiles to detect and disrupt malicious actors.
Vulnerability Testing: Simulating user behavior to test the security and privacy of online services.
Technical Details:
Programming Language: Python 3.x
Libraries Used: json, os, random (all built-in, minimizing dependencies)
Data Storage: Data files organized for easy modification and expansion.
data/names/{gender}/{nationality}.txt: Names organized by gender and nationality.
data/last_names/{nationality}.txt: Last names organized by nationality.
data/interests/general.txt: General interests.
data/locations.json: Hierarchical location data.
data/profile_pictures.txt: URLs of generic profile pictures.
Key Learnings and Skills Demonstrated:
Python Programming: Proficiency in Python syntax, data structures, and file I/O.
Command-Line Interface (CLI) Design: Experience in creating user-friendly and interactive CLIs.
Data Management: Skills in organizing and managing data in external files.
Randomization and Simulation: Understanding of techniques for generating realistic and diverse data.
OSINT Methodology: Knowledge of OSINT principles and techniques, including persona creation, social media reconnaissance, and data collection.
Ethical Considerations: Awareness of the ethical and legal implications of using "Sock Puppets" in OSINT investigations.
Future Enhancements:
More Advanced Name Generation: Generate name suggestions that account for cultural naming conventions and frequency.
Automated Profile Picture Integration: Integrate with image APIs to automatically download and assign profile pictures.
Social Media API Integration: Automate the creation of social media accounts using the generated profile data (with extreme caution and respect for terms of service).
Enhanced Realism: Incorporate natural language processing (NLP) to generate more realistic biographies and posts.
GUI Interface: Develop a graphical user interface (GUI) for easier use and accessibility.
Project URL (GitHub): [\[Link to your GitHub repository\]](https://github.com/Kanarath/Sock_Spy)

2. Security Considerations
Credential Storage: Sock Spy asks the user to create the password, document it and store it as a field. Consider a secure way to store these passwords instead of exposing them in plain text:
Never Stored in Code: Never hardcode passwords directly in the Python script.
Hashing (If Stored): If you need to store passwords at all (which is generally not recommended), use a strong hashing algorithm (e.g., bcrypt, Argon2) with a unique salt for each password. Python's hashlib and bcrypt libraries can be used for this purpose. Be aware this will mean you can't just use the raw password, you'll have to verify future passwords against this.
Encryption: Encrypt the entire output JSON to protect the credentials. Use a strong encryption algorithm like AES with a randomly generated key.
Key Management: Store the encryption key separately from the encrypted data (e.g., in a secure configuration file). Use environment variables.
Input Validation: Implement robust input validation to prevent command injection vulnerabilities. Sanitize all user input before using it in system calls or file operations.
Data File Security:
Permissions: Set appropriate file permissions on the data files to prevent unauthorized access.
Integrity: Implement checksums or digital signatures to verify the integrity of the data files and detect tampering.
Code Injection: Sanitize every input that it's used for code injection (like the name of the output JSON) so nothing goes haywire.
Dependency Management: Use a requirements.txt file to manage Python dependencies and ensure that all libraries are up-to-date and free from vulnerabilities. Use tools like pip and virtualenv to create isolated Python environments.
Shell Script Security: Ensure that the sock_spy.sh script is properly secured to prevent unauthorized access and execution.

"It is important to note that the program is designed to create a persona exclusively from data created on the spot, not to gather, store, or process any sort of real personal information for anyone to be used in a malicious way, just created data to be useful in an OSINT scope within legal terms."