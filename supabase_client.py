import os
from supabase import create_client,Client
from dotenv import load_dotenv

load_dotenv()

# Read environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

# Safety check (helps catch mistakes early)
if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError("Supabase credentials missing. Check your .env file.")

# 3. Create supabase client only ONCE
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)