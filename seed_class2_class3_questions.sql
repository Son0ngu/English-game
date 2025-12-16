-- Add complete question sets for class2 and class3
-- This ensures all difficulty levels and question types are covered

-- CLASS 2 (Grammar Basic) - Complete Question Set
-- EASY level
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('c2_easy_mc1', 'class2', 'What is a noun?', 'multiple_choice', 'easy', '["person, place, or thing","action word","describing word","connecting word"]', 0),
  ('c2_easy_mc2', 'class2', 'Which is a verb?', 'multiple_choice', 'easy', '["house","jump","blue","happy"]', 1),
  ('c2_easy_tf1', 'class2', 'A sentence must have a subject and a verb.', 'true_false', 'easy', '["True","False"]', 0),
  ('c2_easy_tf2', 'class2', 'Adjectives describe verbs.', 'true_false', 'easy', '["True","False"]', 1),
  ('c2_easy_fib1', 'class2', 'I ___ a student.', 'fill_in_the_blank', 'easy', '["am"]', 0),
  ('c2_easy_fib2', 'class2', 'She ___ to school.', 'fill_in_the_blank', 'easy', '["goes"]', 0),
  ('c2_easy_sc1', 'class2', 'Choose the correct verb form: He ___ every day.', 'single_choice', 'easy', '["run","runs","running","ran"]', 1),
  ('c2_easy_sc2', 'class2', 'Which is a complete sentence?', 'single_choice', 'easy', '["Running fast","The dog","I am happy","Very good"]', 2);

-- MEDIUM level
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('c2_med_mc1', 'class2', 'Which are articles?', 'multiple_choice', 'medium', '["a","the","an","is"]', 0),
  ('c2_med_mc2', 'class2', 'Which words are conjunctions?', 'multiple_choice', 'medium', '["and","but","or","very"]', 0),
  ('c2_med_tf1', 'class2', 'A pronoun replaces a noun.', 'true_false', 'medium', '["True","False"]', 0),
  ('c2_med_tf2', 'class2', 'An adverb modifies a noun.', 'true_false', 'medium', '["True","False"]', 1),
  ('c2_med_fib1', 'class2', 'They ___ playing football.', 'fill_in_the_blank', 'medium', '["are"]', 0),
  ('c2_med_fib2', 'class2', 'She has ___ the book.', 'fill_in_the_blank', 'medium', '["read"]', 0),
  ('c2_med_sc1', 'class2', 'Choose the correct pronoun: ___ is my friend.', 'single_choice', 'medium', '["Him","Her","He","His"]', 2),
  ('c2_med_sc2', 'class2', 'Which sentence uses the correct past tense?', 'single_choice', 'medium', '["I goed home","I go home","I went home","I going home"]', 2);

-- HARD level
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('c2_hard_mc1', 'class2', 'Which are subordinating conjunctions?', 'multiple_choice', 'hard', '["because","although","while","very"]', 0),
  ('c2_hard_mc2', 'class2', 'Which sentences use the subjunctive mood?', 'multiple_choice', 'hard', '["If I were rich","I wish I were there","He acts as if he were king","I am here"]', 0),
  ('c2_hard_tf1', 'class2', 'A gerund functions as a noun.', 'true_false', 'hard', '["True","False"]', 0),
  ('c2_hard_tf2', 'class2', 'An infinitive can only be used as a verb.', 'true_false', 'hard', '["True","False"]', 1),
  ('c2_hard_fib1', 'class2', 'By this time tomorrow, I will ___ finished.', 'fill_in_the_blank', 'hard', '["have"]', 0),
  ('c2_hard_fib2', 'class2', 'The book ___ by millions.', 'fill_in_the_blank', 'hard', '["was read"]', 0),
  ('c2_hard_sc1', 'class2', 'Identify the participial phrase: The girl, running quickly, won the race.', 'single_choice', 'hard', '["The girl","running quickly","won the race","None"]', 1),
  ('c2_hard_sc2', 'class2', 'Which is an example of passive voice?', 'single_choice', 'hard', '["She writes letters","Letters are written by her","She is writing","She wrote"]', 1);

-- VERY HARD level
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('c2_vh_mc1', 'class2', 'Which are examples of anaphora?', 'multiple_choice', 'very hard', '["repetition at start","repetition at end","use of pronouns","backward reference"]', 0),
  ('c2_vh_mc2', 'class2', 'In transformational grammar, what are deep structures?', 'multiple_choice', 'very hard', '["surface forms","underlying meanings","phonetic representations","written forms"]', 1),
  ('c2_vh_tf1', 'class2', 'The extended projection principle requires sentences to have subjects.', 'true_false', 'very hard', '["True","False"]', 0),
  ('c2_vh_tf2', 'class2', 'Chomsky hierarchy classifies grammars by generative power.', 'true_false', 'very hard', '["True","False"]', 0),
  ('c2_vh_fib1', 'class2', 'A sentence with multiple embeddings tests ___ memory.', 'fill_in_the_blank', 'very hard', '["working"]', 0),
  ('c2_vh_fib2', 'class2', 'In X-bar theory, every phrase has a ___ position.', 'fill_in_the_blank', 'very hard', '["specifier"]', 0),
  ('c2_vh_sc1', 'class2', 'What is the theta criterion in government and binding theory?', 'single_choice', 'very hard', '["word order","argument structure","tense marking","negation"]', 1),
  ('c2_vh_sc2', 'class2', 'Which principle explains wh-movement?', 'single_choice', 'very hard', '["locality","economy","projection","move alpha"]', 3);

-- CLASS 3 (Vocabulary Advanced) - Complete Question Set
-- EASY level
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('c3_easy_mc1', 'class3', 'What does "happy" mean?', 'multiple_choice', 'easy', '["joyful","sad","angry","tired"]', 0),
  ('c3_easy_mc2', 'class3', 'Which word means "large"?', 'multiple_choice', 'easy', '["big","small","tiny","little"]', 0),
  ('c3_easy_tf1', 'class3', '"Hot" and "cold" are antonyms.', 'true_false', 'easy', '["True","False"]', 0),
  ('c3_easy_tf2', 'class3', '"Fast" and "quick" are synonyms.', 'true_false', 'easy', '["True","False"]', 0),
  ('c3_easy_fib1', 'class3', 'A ___ is a large body of water.', 'fill_in_the_blank', 'easy', '["ocean"]', 0),
  ('c3_easy_fib2', 'class3', 'The opposite of day is ___.', 'fill_in_the_blank', 'easy', '["night"]', 0),
  ('c3_easy_sc1', 'class3', 'Which word means the same as "smart"?', 'single_choice', 'easy', '["stupid","intelligent","dumb","slow"]', 1),
  ('c3_easy_sc2', 'class3', 'A synonym for "begin" is:', 'single_choice', 'easy', '["end","start","finish","stop"]', 1);

-- MEDIUM level
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('c3_med_mc1', 'class3', 'Which words mean "to make better"?', 'multiple_choice', 'medium', '["improve","enhance","worsen","deteriorate"]', 0),
  ('c3_med_mc2', 'class3', 'Which are synonyms for "difficult"?', 'multiple_choice', 'medium', '["hard","challenging","easy","simple"]', 0),
  ('c3_med_tf1', 'class3', '"Benevolent" means kind and generous.', 'true_false', 'medium', '["True","False"]', 0),
  ('c3_med_tf2', 'class3', '"Verbose" means using few words.', 'true_false', 'medium', '["True","False"]', 1),
  ('c3_med_fib1', 'class3', 'To ___ means to make something less severe.', 'fill_in_the_blank', 'medium', '["mitigate"]', 0),
  ('c3_med_fib2', 'class3', 'An ___ person is outgoing and sociable.', 'fill_in_the_blank', 'medium', '["extroverted"]', 0),
  ('c3_med_sc1', 'class3', 'What does "ambiguous" mean?', 'single_choice', 'medium', '["clear","unclear","bright","dark"]', 1),
  ('c3_med_sc2', 'class3', 'A "novice" is:', 'single_choice', 'medium', '["expert","beginner","teacher","master"]', 1);

-- HARD level
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('c3_hard_mc1', 'class3', 'Which words mean to make worse?', 'multiple_choice', 'hard', '["exacerbate","aggravate","ameliorate","improve"]', 0),
  ('c3_hard_mc2', 'class3', 'Which are antonyms of "ephemeral"?', 'multiple_choice', 'hard', '["permanent","lasting","temporary","fleeting"]', 0),
  ('c3_hard_tf1', 'class3', '"Obfuscate" means to make something clearer.', 'true_false', 'hard', '["True","False"]', 1),
  ('c3_hard_tf2', 'class3', '"Mendacious" means truthful and honest.', 'true_false', 'hard', '["True","False"]', 1),
  ('c3_hard_fib1', 'class3', 'To ___ means to speak or write at length.', 'fill_in_the_blank', 'hard', '["expatiate"]', 0),
  ('c3_hard_fib2', 'class3', 'A ___ argument is convincing and well-reasoned.', 'fill_in_the_blank', 'hard', '["cogent"]', 0),
  ('c3_hard_sc1', 'class3', 'What does "perspicacious" mean?', 'single_choice', 'hard', '["confused","insightful","slow","dull"]', 1),
  ('c3_hard_sc2', 'class3', '"Recalcitrant" means:', 'single_choice', 'hard', '["obedient","stubborn","flexible","agreeable"]', 1);

-- VERY HARD level
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('c3_vh_mc1', 'class3', 'Which words relate to excessive pride?', 'multiple_choice', 'very hard', '["hubris","arrogance","humility","modesty"]', 0),
  ('c3_vh_mc2', 'class3', 'Which are examples of malapropism?', 'multiple_choice', 'very hard', '["wrong word","correct usage","proper grammar","exact meaning"]', 0),
  ('c3_vh_tf1', 'class3', '"Sesquipedalian" refers to using long words.', 'true_false', 'very hard', '["True","False"]', 0),
  ('c3_vh_tf2', 'class3', '"Pleonasm" means economical use of words.', 'true_false', 'very hard', '["True","False"]', 1),
  ('c3_vh_fib1', 'class3', 'The quality of being ___ involves using unnecessarily complex language.', 'fill_in_the_blank', 'very hard', '["abstruse"]', 0),
  ('c3_vh_fib2', 'class3', 'A ___ is a figure of speech comparing unlike things without using like or as.', 'fill_in_the_blank', 'very hard', '["metaphor"]', 0),
  ('c3_vh_sc1', 'class3', 'What is the meaning of "synecdoche"?', 'single_choice', 'very hard', '["repetition","part for whole","exaggeration","understatement"]', 1),
  ('c3_vh_sc2', 'class3', '"Tmesis" refers to:', 'single_choice', 'very hard', '["word ending","splitting compound","joining words","plural form"]', 1);
