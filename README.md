# Fragrance Recommend Website
#### Video Demo:  <https://youtu.be/mCVmk8w1pcc>
#### Description:

Overview
The Perfume Recommendation Webpage is a Flask-based application designed to help users discover perfumes tailored to their scent preferences, personality traits, and optional gender. By leveraging a SQLite database (fragrance_Internal.db) populated with data scraped from Nosetime (https://www.nosetime.com/), a professional perfume review community, the application matches user inputs to a curated selection of perfumes. It uses a scoring algorithm to rank perfumes based on scent notes, personality attributes, and fragrance types, displaying the top five recommendations with details like brand, name, notes, comments, and images. The project aims to provide an intuitive, user-friendly experience for perfume enthusiasts, combining a robust backend with a clean front-end interface.

Project Structure and File Descriptions
The project consists of several key files, each serving a specific purpose:
•	app.py: The core Python script that defines the Flask application. It handles routing, database interactions, and recommendation logic. The script:
o	Initializes the Flask app and sets paths for the SQLite database (fragrance_Internal.db) and image folder (static/fragrance_internal_fig).
o	Defines helper functions: load_fragrances() to query the database into a Pandas DataFrame, parse_notes() to extract scent notes and percentages, and find_image_for_perfume() to match perfume names to images.
o	Implements the recommendation logic in recommend_fragrances(), which scores perfumes based on user-selected scents, personality, and gender, returning the top five matches.
o	Defines the main route (/) to handle GET (display form) and POST (process inputs and show results) requests.
•	templates/index.html: The homepage template, rendered for GET requests. It contains a form where users select scent preferences (e.g., Citrus, Floral), a personality trait (e.g., Confident, Romantic), and optional gender. The form uses multi-select dropdowns for scents and single-select for personality and gender, styled with basic CSS for usability.
•	templates/results.html: The results template, displayed after form submission. It shows the top five recommended perfumes in a clean layout, including brand, name, fragrance type, signature notes, matched notes, user comments, and images (if available). A timestamp is included to indicate when recommendations were generated.
•	fragrance_Internal.db: A SQLite database containing a fragrance table with columns for brand, name, fragrance type (frag_type), signature notes (sig_note), attributes (e.g., male, female, unisex), and comments (itemcomment1). The data is scraped from Nosetime, ensuring a rich dataset of perfumes and reviews.
•	static/fragrance_internal_fig/: A folder within the static/ directory storing perfume images. Filenames are matched to perfume names for display in the results page.

Functionality
The application works as follows:
1.	Users access the homepage (http://localhost:5000) and select their preferences.
2.	Upon form submission, the app validates inputs, ensuring at least one scent and personality are chosen.
3.	The recommend_fragrances() function processes inputs, querying the database and scoring perfumes based on:
o	Matching scent notes (weighted by percentage in sig_note).
o	Alignment with personality attributes and fragrance types (defined in personality_mapping and scent_categories).
o	Optional gender filtering to exclude non-matching perfumes.
4.	Results are sorted by score, and the top five are displayed with images and details.
5.	Users can return to the homepage to try different combinations.

Design Choices
Several design decisions shaped the project, with the scoring algorithm being a critical component:
•	Scoring Algorithm: The recommend_fragrances() function employs a straightforward additive scoring system to rank perfumes. For each perfume in the database, the algorithm:
o	Matches Scent Notes: It compares user-selected scent categories (e.g., Citrus, Floral) to the perfume’s signature notes (stored in sig_note as, e.g., "Orange(30%)"). The parse_notes() function extracts notes and their percentages using regex (e.g., (\w+|\w+\s\w+)\((\d+)%\)). Each matched note adds its percentage (e.g., 30 for Orange) to the perfume’s score. This ensures that perfumes with stronger concentrations of preferred notes rank higher, reflecting their prominence in the fragrance.
o	Personality Attributes: If the perfume’s attribute (e.g., male, female, unisex) matches the user’s selected personality (via personality_mapping), it receives a fixed +20 points. This boosts perfumes aligned with the user’s chosen personality (e.g., “Confident” maps to male/unisex perfumes).
o	Fragrance Types: If the perfume’s type (e.g., “花香调”) matches the personality’s associated types, it gains another +20 points. This reinforces relevance to the user’s style.
o	Gender Filtering: If a gender is selected, perfumes not matching that gender (or unisex) are excluded, ensuring targeted recommendations.
o	Ranking: Perfumes with a score greater than 0 are sorted in descending order, and the top five are returned with details like matched notes and images.
o
Why This Approach? The additive scoring system was chosen for its simplicity and interpretability, making it easy to implement and maintain within the project’s scope. Assigning percentage-based points for notes ensures that dominant scent components have more weight, while fixed bonuses for attributes and types provide a balanced influence of personality. The +20-point bonuses were selected after testing to avoid overwhelming the note-based scores (which range from 0 to 100 per note) while still prioritizing personality alignment. Gender filtering was included to refine results for users with specific preferences, though it’s optional to maintain flexibility.

Setup and Usage
1.	Requirements: Install flask, pandas, and sqlite3.
2.	Database: Place fragrance_Internal.db in the project root, populated with Nosetime data.
3.	Images: Add perfume images to static/fragrance_internal_fig/.
4.	Run: Execute python app.py and visit http://localhost:5000.
5.	Demo: Select scents (e.g., Citrus), a personality (e.g., Romantic), and optional gender. Submit to view results, then try different inputs.

Future Improvements
•	Add user authentication for saving preferences.
•	Implement machine learning for advanced recommendation logic.
•	Support real-time Nosetime data via an API (if available).

This project delivers a practical, engaging tool for perfume discovery, blending simplicity with a user-focused experience.

