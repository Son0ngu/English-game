# Database Seeding Guide

## Quick Start

To seed all databases with complete data:

```bash
./seed_all.sh
```

This will seed both `database.db` and `userprofile.db` with full test data.

## What Gets Seeded

### database.db
- **7 users** (1 admin, 2 teachers, 4 students)
- **3 classes** (English A1, Grammar Basic, Vocabulary Advanced)
- **113 questions** across all classes
  - Class 1: 41 questions
  - Class 2: 36 questions
  - Class 3: 36 questions
- **43 permissions** (role-based access control)

### userprofile.db
- **7 user profiles** (matching auth users)
- **4 student profiles** with default stats (HP: 100, ATK: 10, Money: 100)
- **2 teacher profiles**
- **4 personal swords** (one for each student)

## Question Coverage

All classes have complete question coverage:
- **4 difficulty levels**: easy, medium, hard, very hard
- **4 question types per level**:
  - Multiple Choice
  - True/False
  - Fill in the Blank
  - Single Choice

This ensures the game is playable at all difficulty levels in all classes.

## Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin01 | admin123 |
| Teacher | teacher1 | teach123 |
| Teacher | teacher2 | teach234 |
| Student | student1 | stud123 |
| Student | student2 | stud123 |
| Student | student3 | stud234 |
| Student | student4 | stud345 |

## Manual Seeding

If you need to seed databases individually:

### Seed database.db
```bash
sqlite3 database.db < seed_fixed.sql
sqlite3 database.db < seed_class2_class3_questions.sql
```

### Seed userprofile.db
```bash
# Recreate schema
sqlite3 userprofile.db "DROP TABLE IF EXISTS items;"
sqlite3 userprofile.db "DROP TABLE IF EXISTS student_profiles;"
sqlite3 userprofile.db "DROP TABLE IF EXISTS teacher_profiles;"
sqlite3 userprofile.db "DROP TABLE IF EXISTS user_profiles;"
sqlite3 userprofile.db < user_profile_service/DBTable.sql

# Add data
sqlite3 userprofile.db < seed_userprofile.sql
```

## Seed Files

- `seed_fixed.sql` - Main seed for auth, classes, class1 questions, and permissions
- `seed_class2_class3_questions.sql` - Complete questions for class2 and class3
- `seed_userprofile.sql` - User profiles and items
- `seed_all.sh` - Master script that runs all seeds

## Verifying Seed Data

Check question distribution:
```bash
sqlite3 database.db "SELECT class_id, difficulty, COUNT(*) FROM questions GROUP BY class_id, difficulty;"
```

Check user profiles:
```bash
sqlite3 userprofile.db "SELECT id, role FROM user_profiles;"
```

## Issues Fixed

The original `seed.sql` had issues:
1. ❌ Permission table schema mismatch (used `role` column instead of boolean columns)
2. ❌ Class 2 and Class 3 had incomplete question sets
3. ❌ Missing questions prevented gameplay at certain difficulty levels

All issues have been resolved in the new seed files.
