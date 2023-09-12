# ShoutToLearn Telegram Bot

A Telegram bot to search for content on the `ShoutToLearn` website and display results.

## Features:

- Web scraping to fetch search results from `ShoutToLearn`.
- Command-based interactions.
- Provides information about ShoutToLearn's content for both ICSE and ISC.
- Contact details for the admin.
- Links to ShoutToLearn's social media handles.

## Commands:

- `/start` - Welcome message.
- `/help` - Display the help guide.
- `/contact` - Display contact details for the admin.
- `/isc` - Display content related to ISC Class 12.
- `/icse` - Display content related to ICSE Class 10.
- `/social` - Display links to official social media handles.

Any other text sent to the bot will be treated as a search query. The bot will help you determine if the content related to the sent text is available on the website.

## Requirements:

- Python libraries: `logging`, `httpx`, `selectolax`, `telegram`, `dotenv`
- A `.env` file containing the `BOT_TOKEN` for authentication.

## Setup:

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt` (You will need to create this file with the libraries mentioned).
3. Create a `.env` file in the root directory and add your `BOT_TOKEN`.
4. Run the bot using `python main.py`.

## Contributing:

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you'd like to change.

## License:

This project is licensed under the MIT License.

## Contact:

For any queries or feedback, please contact:
- Name: Andhi Toofan
- Telegram: @AndhiToofan
