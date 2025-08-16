import asyncio
from pyrogram import Client
import os
import sys

class SessionGenerator:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        
    def get_credentials(self):
        print("🎵 VCPlay Music Bot - Session Generator")
        print("=" * 50)
        print("📖 Instructions:")
        print("1. Go to https://my.telegram.org")
        print("2. Login with your phone number")
        print("3. Go to 'API Development Tools'")
        print("4. Create a new application")
        print("5. Copy API_ID and API_HASH")
        print("=" * 50)
        
        while True:
            try:
                self.api_id = int(input("\n📝 Enter your API_ID: "))
                break
            except ValueError:
                print("❌ Invalid API_ID. Please enter numbers only.")
        
        self.api_hash = input("📝 Enter your API_HASH: ")
        
        if not self.api_hash.strip():
            print("❌ API_HASH cannot be empty!")
            sys.exit(1)
    
    async def generate_session(self):
        print("\n🔄 Starting session generation...")
        print("📱 Please check your Telegram for verification code...")
        
        try:
            async with Client("session_generator", self.api_id, self.api_hash) as app:
                session_string = await app.export_session_string()
                
                # Get user info
                me = await app.get_me()
                
                print("\n" + "=" * 60)
                print("✅ SESSION STRING GENERATED SUCCESSFULLY!")
                print("=" * 60)
                print(f"👤 Account: {me.first_name} (@{me.username or 'No username'})")
                print(f"📱 Phone: +{me.phone_number}")
                print(f"🆔 User ID: {me.id}")
                print("=" * 60)
                print("🔑 Your SESSION_STRING:")
                print(f"{session_string}")
                print("=" * 60)
                
                # Save to file with user info
                filename = f"session_{me.id}.txt"
                with open(filename, "w") as f:
                    f.write(f"Account: {me.first_name} (@{me.username or 'No username'})\n")
                    f.write(f"Phone: +{me.phone_number}\n")
                    f.write(f"User ID: {me.id}\n")
                    f.write(f"Generated: {asyncio.get_event_loop().time()}\n")
                    f.write(f"\nSESSION_STRING = '{session_string}'\n")
                
                print(f"💾 Session details saved to: {filename}")
                print("\n🔐 SECURITY REMINDERS:")
                print("• This session string gives FULL access to your account")
                print("• Never share it with anyone")
                print("• Don't post it online or in groups")
                print("• Use it only for your own bots")
                print("• Keep it secure like a password")
                print("\n✅ You can now use this SESSION_STRING in your music bot!")
                
        except Exception as e:
            print(f"\n❌ Error generating session: {e}")
            print("\n🛠️ Troubleshooting:")
            print("• Check your API_ID and API_HASH are correct")
            print("• Ensure you have stable internet connection")
            print("• Verify your phone number is correct")
            print("• Check if 2FA code is entered correctly")

def main():
    generator = SessionGenerator()
    generator.get_credentials()
    
    try:
        asyncio.run(generator.generate_session())
    except KeyboardInterrupt:
        print("\n❌ Process cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
