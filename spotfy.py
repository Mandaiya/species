import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
SPOTIFY_CLIENT_ID = '566027c77614413ea026aecc9ae66431'
SPOTIFY_CLIENT_SECRET = '8ff250d41eeb4199b10eb12b96d79f18'

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = '6369515689:AAGToA4VTFWYBiGdo4MLSXylzLkTijspqRI'

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set up Spotify client
spotify_client = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

def search_song(update: Update, context: CallbackContext) -> None:
    """Search for a song on Spotify and send the track preview link."""
    if not context.args:
        update.message.reply_text("Please provide a song name. Usage: /search <song name>")
        return
    
    song_name = " ".join(context.args)
    results = spotify_client.search(q=song_name, type='track', limit=1)

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        preview_url = track.get('preview_url')  # Note: Not all tracks have previews

        if preview_url:
            update.message.reply_text(f"🎵 {track_name} by {artist_name}\nListen: {preview_url}")
        else:
            update.message.reply_text(f"🎵 {track_name} by {artist_name}\nSorry, no preview available.")
    else:
        update.message.reply_text("No results found for your query.")

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message."""
    update.message.reply_text("Welcome! Use /search <song name> to find a song on Spotify.")

def main() -> None:
    """Run the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search_song))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
