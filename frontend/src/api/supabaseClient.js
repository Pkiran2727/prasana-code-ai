import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://yclqwkrfdtiukilrviwy.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im52bGJpaGhxbWRkeGxkdnZtbXV3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0OTQ4OTgsImV4cCI6MjA4OTA3MDg5OH0.UUKMuWBS_lg9iMocpN0XIXGDx0vZcCcnQ7yl1UccJwU';

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
  }
});
