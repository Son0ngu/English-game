#!/bin/bash
# Master seed script for English Game databases
# This script seeds both database.db and userprofile.db with complete data

set -e  # Exit on error

echo "🌱 Starting database seeding..."

# Seed main database (auth, classes, questions, permissions)
echo "📚 Seeding database.db (auth, classes, questions, permissions)..."
sqlite3 database.db < seed_fixed.sql
sqlite3 database.db < seed_class2_class3_questions.sql

# Recreate userprofile.db schema and seed
echo "👤 Seeding userprofile.db (user profiles, items)..."
sqlite3 userprofile.db "DROP TABLE IF EXISTS items;"
sqlite3 userprofile.db "DROP TABLE IF EXISTS student_profiles;"
sqlite3 userprofile.db "DROP TABLE IF EXISTS teacher_profiles;"
sqlite3 userprofile.db "DROP TABLE IF EXISTS user_profiles;"
sqlite3 userprofile.db < user_profile_service/DBTable.sql
sqlite3 userprofile.db < seed_userprofile.sql

# Verify seeding
echo ""
echo "✅ Seeding complete! Verification:"
echo ""
echo "📊 database.db statistics:"
sqlite3 database.db "SELECT 'Users: ' || COUNT(*) FROM auth_service;"
sqlite3 database.db "SELECT 'Classes: ' || COUNT(*) FROM classes;"
sqlite3 database.db "SELECT 'Questions: ' || COUNT(*) FROM questions;"
sqlite3 database.db "SELECT 'Permissions: ' || COUNT(*) FROM permission;"

echo ""
echo "📊 userprofile.db statistics:"
sqlite3 userprofile.db "SELECT 'User Profiles: ' || COUNT(*) FROM user_profiles;"
sqlite3 userprofile.db "SELECT 'Student Profiles: ' || COUNT(*) FROM student_profiles;"
sqlite3 userprofile.db "SELECT 'Teacher Profiles: ' || COUNT(*) FROM teacher_profiles;"
sqlite3 userprofile.db "SELECT 'Items: ' || COUNT(*) FROM items;"

echo ""
echo "📊 Question coverage by class:"
sqlite3 database.db "SELECT class_id || ' - ' || difficulty || ': ' || COUNT(*) || ' questions' FROM questions GROUP BY class_id, difficulty ORDER BY class_id, difficulty;"

echo ""
echo "🎉 All databases seeded successfully!"
echo ""
echo "Test credentials:"
echo "  Admin:    admin01 / admin123"
echo "  Teacher:  teacher1 / teach123"
echo "  Student:  student1 / stud123"
