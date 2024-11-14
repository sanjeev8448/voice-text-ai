# voice-text-ai

Code Structure
Imports and Setup:
Imports necessary libraries for voice processing (sounddevice, speech_recognition), translation (googletrans), and text-to-speech (gTTS).
Sets up sqlite3 for database management and bcrypt for password hashing.
Initializes Streamlit for the web interface.
Database Setup:
Creates an SQLite database (users.db) with a users table to store usernames and hashed passwords.
Utility Functions:
hash_password(password): Hashes passwords with bcrypt for secure storage.
check_password(password, hashed): Verifies the password by comparing it with the stored hash.
Signup and Login Functions:
signup(username, password): Registers a new user, storing the username and hashed password in the database. Returns True if successful, otherwise False.
login(username, password): Authenticates the user by checking credentials against stored data. Returns True if login is successful, otherwise False.
Translation and Voice Playback Functions:
translator_function(spoken_text, from_language, to_language): Translates the spoken text from one language to another using the Google Translate API.
text_to_voice(text_data, to_language): Converts translated text to speech using gTTS, plays it, and then deletes the audio file for cleanup.
Streamlit Interface:
Session State and Authentication: Checks and maintains the user’s login state with st.session_state.
Login/Signup Interface: Presents login or signup options based on authentication status.
Translator UI: Provides dropdowns for language selection, real-time text placeholders, and a start button to begin recording and translation.
Recording and Translating Loop: Starts a continuous recording loop upon button press, using sounddevice and speech_recognition to capture, process, and display translations. Includes error handling for audio recognition and API requests.
AI Tools and Libraries
Google Translate API (googletrans):
Provides language translation functionality by translating text from the source language to the target language.
Google Text-to-Speech (gTTS):
Converts translated text into spoken audio, enabling playback of translations in different languages.
Speech Recognition (speech_recognition):
Uses Google Speech Recognition to convert audio input into text, facilitating the voice-to-text functionality.
Streamlit:
Provides an interactive web interface for the app, allowing user inputs, dynamic updates, and session management.
Security Considerations
Password Hashing:
bcrypt is used to hash passwords before storing them in the database, making it more resistant to brute force attacks.
Authentication Management:
st.session_state is used to track the user’s authentication status, preventing unauthorized access to the app’s translation functionality.
Only authenticated users are allowed to access the translation interface; others must log in or sign up.
Database Security:
Prepared statements are used for database queries to avoid SQL injection vulnerabilities.
Temporary File Handling:
Temporary audio files created by gTTS are deleted immediately after playback to prevent unauthorized access or data leakage.
Error Handling:
The code includes error handling for common issues like unrecognized audio and API availability, which helps prevent app crashes and unauthorized access to error messages.






USER GUIDE --
Open the App: Launch the Streamlit app for voice-to-text translation with user authentication.
Create an Account or Log In:
New Users:
Select Signup from the sidebar.
Enter a unique username and password, then click Create Account.
A confirmation message will appear if the account creation is successful.
Existing Users:
Select Login from the sidebar.
Enter your username and password, then click Login.
If the credentials are correct, a success message appears, and you’re redirected to the main app.
Using the Translation Feature
Once logged in, you’ll see the main interface for real-time language translation:
Language Selection:
Use the Select Source Language dropdown to choose the language you’ll be speaking in.
Use the Select Target Language dropdown to choose the language you want the translation in.
Voice Input and Translation:
Click Start to begin the voice-to-text and translation process.
The app will start listening to your voice input, converting it to text, and then translating it to the target language.
The Original Transcript section displays your spoken words.
The Translated Transcript section shows the translated text in your chosen target language.
Audio Playback of Translations:
After each translation, the app will automatically generate and play an audio version of the translated text using text-to-speech.
This allows you to hear the translation in the selected target language.
Stop Condition:
Currently, there’s no explicit stop button, but you can manually exit or refresh the app page to stop the listening and translation loop.
Logging Out
To end your session, click Logout in the sidebar. This will return you to the authentication screen, ensuring your account remains secure.

