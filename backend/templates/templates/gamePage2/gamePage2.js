document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const playerHealth = document.querySelector('.player-health');
    const monsterHealth = document.querySelector('.monster-health');
    const damageNumber = document.getElementById('damageNumber');
    const attackEffect = document.getElementById('attackEffect');
    const answerButtons = document.querySelectorAll('.answer-btn');
    const player = document.querySelector('.player img');
    const monster = document.querySelector('.monster img');
    const questionText = document.getElementById('questionText');

    // Game state variables
    let gameSession = null;
    let currentQuestion = null;
    let playerHealthValue = 0;
    let monsterHealthValue = 0;
    let playerMaxHealth = 0;
    let monsterMaxHealth = 0;

    // Timer variables
    let questionTimer = null;
    let timeLeft = 0;
    const QUESTION_TIME_LIMIT = 30; // 30 seconds per question

    // Game mechanics constants
    const PLAYER_DAMAGE = 10;
    const MONSTER_DAMAGE = 5;

    // Screen management functions
    function showLoadingScreen() {
        const elements = {
            loadingScreen: document.getElementById('loadingScreen'),
            battleScene: document.getElementById('battleScene'),
            questionArea: document.getElementById('questionArea'),
            gameInfo: document.getElementById('gameInfo'),
            errorMessage: document.getElementById('errorMessage'),
            timerDisplay: document.getElementById('timerDisplay')
        };

        if (elements.loadingScreen) elements.loadingScreen.style.display = 'block';
        if (elements.battleScene) elements.battleScene.style.display = 'none';
        if (elements.questionArea) elements.questionArea.style.display = 'none';
        if (elements.gameInfo) elements.gameInfo.style.display = 'none';
        if (elements.errorMessage) elements.errorMessage.style.display = 'none';
        if (elements.timerDisplay) elements.timerDisplay.style.display = 'none';
        
        console.log('Showing loading screen');
    }

    function showGameScreen() {
        const elements = {
            loadingScreen: document.getElementById('loadingScreen'),
            battleScene: document.getElementById('battleScene'),
            questionArea: document.getElementById('questionArea'),
            gameInfo: document.getElementById('gameInfo'),
            errorMessage: document.getElementById('errorMessage'),
            timerDisplay: document.getElementById('timerDisplay')
        };

        if (elements.loadingScreen) elements.loadingScreen.style.display = 'none';
        if (elements.battleScene) elements.battleScene.style.display = 'flex';
        if (elements.questionArea) elements.questionArea.style.display = 'block';
        if (elements.gameInfo) elements.gameInfo.style.display = 'block';
        if (elements.errorMessage) elements.errorMessage.style.display = 'none';
        if (elements.timerDisplay) elements.timerDisplay.style.display = 'block';
        
        console.log('Showing game screen');
    }

    function showErrorScreen() {
        const elements = {
            loadingScreen: document.getElementById('loadingScreen'),
            battleScene: document.getElementById('battleScene'),
            questionArea: document.getElementById('questionArea'),
            gameInfo: document.getElementById('gameInfo'),
            errorMessage: document.getElementById('errorMessage'),
            timerDisplay: document.getElementById('timerDisplay')
        };

        if (elements.loadingScreen) elements.loadingScreen.style.display = 'none';
        if (elements.battleScene) elements.battleScene.style.display = 'none';
        if (elements.questionArea) elements.questionArea.style.display = 'none';
        if (elements.gameInfo) elements.gameInfo.style.display = 'none';
        if (elements.errorMessage) elements.errorMessage.style.display = 'block';
        if (elements.timerDisplay) elements.timerDisplay.style.display = 'none';
        
        console.log('Showing error screen');
    }

    // Hide all question type containers
    function hideAllQuestionTypes() {
        const multipleChoiceElement = document.getElementById('multipleChoiceQuestion');
        const fillInBlankElement = document.getElementById('fillInBlankQuestion');
        
        if (multipleChoiceElement) multipleChoiceElement.style.display = 'none';
        if (fillInBlankElement) fillInBlankElement.style.display = 'none';
        
        // Clear the main question text when hiding
        const questionTextElement = document.getElementById('questionText');
        if (questionTextElement) {
            questionTextElement.textContent = 'Loading next question...';
        }
        
        console.log('All question types hidden and text cleared');
    }

    // JWT Token management with fallback for testing
    function getJWTToken() {
        const token = localStorage.getItem('jwtToken') || sessionStorage.getItem('jwtToken');
        
        // TEMPORARY: Fallback to test token if no token found
        if (!token) {
            console.log('No JWT token found, using test token');
            const testToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0ODk0MjIwNSwianRpIjoiZmI4MThjYTctNTIxZC00MjRkLWE3YTgtNDA5ZjkzZTU2NjJjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjkyNTVkZTliLWMxMDktNGE0NS1hMjAzLWJiNTNiYjM2ZWNiYyIsIm5iZiI6MTc0ODk0MjIwNSwiY3NyZiI6IjI5MDE1YjM4LWNhNTQtNGUwMy04MzgyLWM2ZmJjM2FkYTMyZiIsImV4cCI6MTc0ODk0OTQwNSwicm9sZSI6InN0dWRlbnQifQ.b-3Y_98pzjyJLsvPh50HBBrwEHbCnRS76EA8eTZ7-Ag';
            localStorage.setItem('jwtToken', testToken);
            return testToken;
        }
        
        return token;
    }

    // Timer functions
    function startQuestionTimer() {
        // Clear any existing timer
        if (questionTimer) {
            clearInterval(questionTimer);
        }
        
        timeLeft = QUESTION_TIME_LIMIT;
        updateTimerDisplay();
        
        questionTimer = setInterval(() => {
            timeLeft--;
            updateTimerDisplay();
            
            if (timeLeft <= 0) {
                handleTimeOut();
            }
        }, 1000);
        
        console.log('Question timer started');
    }
    
    function stopQuestionTimer() {
        if (questionTimer) {
            clearInterval(questionTimer);
            questionTimer = null;
            console.log('Question timer stopped');
        }
    }
    
    // Update timer display with visual feedback
    function updateTimerDisplay() {
        const timerElement = document.getElementById('timerDisplay');
        if (timerElement) {
            timerElement.textContent = `Time: ${timeLeft}`;
            
            // Change styling based on time left
            if (timeLeft <= 5) {
                timerElement.className = 'timer-display danger';
            } else if (timeLeft <= 10) {
                timerElement.className = 'timer-display warning';
            } else {
                timerElement.className = 'timer-display';
            }
        }
    }
    
    // REPLACE your handleTimeOut function:

async function handleTimeOut() {
    stopQuestionTimer();
    
    console.log('Time is up! Auto-submitting answer "sai"');
    
    // Disable all interactions
    answerButtons.forEach(btn => btn.disabled = true);
    const blankInput = document.getElementById('blankInput');
    const submitBtn = document.getElementById('submitAnswerBtn');
    if (blankInput) blankInput.disabled = true;
    if (submitBtn) submitBtn.disabled = true;
    
    // Submit answer "sai" to backend
    const result = await submitAnswer("sai");
    
    // Determine which question type we're handling
    const fillInBlankElement = document.getElementById('fillInBlankQuestion');
    const isFillinBlank = fillInBlankElement && fillInBlankElement.style.display !== 'none';
    
    if (isFillinBlank) {
        // Handle as fill-in-blank timeout with auto-advance
        await handleFillInBlankTimeout(result);
    } else {
        // Handle as multiple choice timeout with auto-advance
        await handleMultipleChoiceTimeout(result);
    }
}

// REPLACE your handleMultipleChoiceTimeout function:
async function handleMultipleChoiceTimeout(result) {
    // Show timeout styling
    answerButtons.forEach(btn => {
        btn.classList.add('timeout');
    });
    
    // Show timeout indicator
    const questionTextElement = document.getElementById('questionText');
    if (questionTextElement) {
        const originalText = questionTextElement.textContent;
        questionTextElement.textContent = `⏰ TIMEOUT: ${originalText}`;
        questionTextElement.style.color = '#ff6b35';
    }
    
    // Treat timeout as incorrect answer
    try {
        if (typeof playHitSFX === 'function') playHitSFX();
    } catch (error) {
        console.log('Hit SFX failed:', error);
    }
    
    // Monster attack animation
    if (monster) monster.style.transform = 'translateX(-30px)';
    setTimeout(() => {
        // Update player health locally
        playerHealthValue = Math.max(0, playerHealthValue - MONSTER_DAMAGE);
        updateHealthBars();
        
        if (player) player.style.transform = 'translateX(-15px) rotate(-5deg)';
        
        setTimeout(async () => {
            if (monster) monster.style.transform = '';
            if (player) player.style.transform = '';
            
            // Reset button styling
            answerButtons.forEach(btn => {
                btn.classList.remove('timeout');
                btn.disabled = false;
            });
            
            // Reset question text color
            if (questionTextElement) {
                questionTextElement.style.color = '';
            }
            
            // Check lose condition locally
            if (playerHealthValue <= 0) {
                handleGameEnd(false);
            } else {
                // AUTO-ADVANCE: Get next question (same as incorrect answer flow)
                console.log('Timeout - auto-advancing to next question');
                await getQuestion();
            }
        }, 1000);
    }, 200);
}
// REPLACE your handleFillInBlankTimeout function:
async function handleFillInBlankTimeout(result) {
    const blankInput = document.getElementById('blankInput');
    
    if (blankInput) {
        blankInput.value = 'TIMEOUT';
        blankInput.classList.add('timeout');
        blankInput.style.backgroundColor = '#fff3cd';
        blankInput.style.borderColor = '#ffc107';
    }
    
    // Show timeout message in question text
    const questionTextElement = document.getElementById('questionText');
    if (questionTextElement) {
        const originalText = questionTextElement.textContent;
        questionTextElement.textContent = `⏰ TIMEOUT: ${originalText}`;
        questionTextElement.style.color = '#ff6b35';
    }
    
    try {
        if (typeof playHitSFX === 'function') playHitSFX();
    } catch (error) {
        console.log('Hit SFX failed:', error);
    }
    
    // Monster attack animation
    if (monster) monster.style.transform = 'translateX(-30px)';
    setTimeout(() => {
        // Update player health locally
        playerHealthValue = Math.max(0, playerHealthValue - MONSTER_DAMAGE);
        updateHealthBars();
        
        if (player) player.style.transform = 'translateX(-15px) rotate(-5deg)';
        
        setTimeout(async () => {
            if (monster) monster.style.transform = '';
            if (player) player.style.transform = '';
            
            // Reset question text color
            if (questionTextElement) {
                questionTextElement.style.color = '';
            }
            
            // Check game status
            if (playerHealthValue <= 0) {
                handleGameEnd(false);
            } else {
                // AUTO-ADVANCE: Get next question (same as incorrect answer flow)
                console.log('Timeout - auto-advancing to next question');
                resetFillInBlankUI();
                await getQuestion();
            }
        }, 1000);
    }, 200);
}
    
    async function handleMultipleChoiceTimeout(result) {
        // Show timeout message
        answerButtons.forEach(btn => {
            btn.classList.add('timeout');
            btn.textContent = btn.textContent + ' (TIMEOUT)';
        });
        
        // Treat timeout as incorrect answer
        try {
            if (typeof playHitSFX === 'function') playHitSFX();
        } catch (error) {
            console.log('Hit SFX failed:', error);
        }
        
        // Monster attack animation
        if (monster) monster.style.transform = 'translateX(-30px)';
        setTimeout(() => {
            // Update player health locally
            playerHealthValue = Math.max(0, playerHealthValue - MONSTER_DAMAGE);
            updateHealthBars();
            
            if (player) player.style.transform = 'translateX(-15px) rotate(-5deg)';
            
            setTimeout(async () => {
                if (monster) monster.style.transform = '';
                if (player) player.style.transform = '';
                
                // Reset button styling
                answerButtons.forEach(btn => {
                    btn.classList.remove('timeout');
                    btn.disabled = false;
                });
                
                // Check lose condition locally
                if (playerHealthValue <= 0) {
                    handleGameEnd(false);
                } else {
                    // Get next question
                    await getQuestion();
                }
            }, 1000);
        }, 200);
    }
    
    

    // Update game info display
    function updateGameInfo(sessionData) {
        const gameDifficultyElement = document.getElementById('gameDifficulty');
        const sessionIdElement = document.getElementById('sessionId');
        const playerLevelElement = document.getElementById('playerLevel');
        const monsterLevelElement = document.getElementById('monsterLevel');
        
        if (gameDifficultyElement) gameDifficultyElement.textContent = sessionData.difficulty || '-';
        if (sessionIdElement) sessionIdElement.textContent = sessionData.session_id || '-';
        if (playerLevelElement) playerLevelElement.textContent = sessionData.player_level || sessionData.player_stats?.level || '1';
        if (monsterLevelElement) monsterLevelElement.textContent = sessionData.monster_level || sessionData.monster_stats?.level || '1';
        
        console.log('Game info updated:', sessionData);
    }

    // Create game room with enhanced error handling
    async function createGameRoom(difficulty = "easy", classId = "class1") {
        try {
            console.log('Creating game room...', { difficulty, classId });
            showLoadingScreen();
            
            // FIXED: Use exact same format as your successful Postman request
            const response = await fetch('http://127.0.0.1:5000/game/newroom', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getJWTToken()}`
                },
                body: JSON.stringify({
                    difficulty: difficulty,
                    class_id: "class1"
                })
            });
            console.log(`API Response status: ${response.status}`);
            
            if (!response.ok) {
                if (response.status === 401) {
                    console.log('Unauthorized, removing tokens and redirecting');
                    localStorage.removeItem('jwtToken');
                    sessionStorage.removeItem('jwtToken');
                    window.location.href = '/login';
                    return;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log("Game room created:", data);

            // Handle the response exactly like in your example
            const sessionId = data.session_id;
            const monsterHP = data.monster_stats.hp;
            const playerHP = data.player_stats.hp;
            const playerATK = data.player_stats.atk;
            
            console.log('Session data:', { sessionId, monsterHP, playerHP, playerATK });
            
            // Store the session data
            gameSession = data;
            
            // Update game state with backend data
            playerHealthValue = playerHP;
            playerMaxHealth = playerHP;
            
            monsterHealthValue = monsterHP;
            monsterMaxHealth = monsterHP;
            
            // Update UI with backend data
            updateGameInfo(data);
            updateHealthBars();
            
            // Get first question
            await getQuestion();
            
            // Show game screen
            showGameScreen();
            
            return data;
        } catch (error) {
            console.error('Failed to create game room:', error);
            showErrorScreen();
            throw error;
        }
    }

    // Get question from backend with correct response handling
    async function getQuestion() {
        if (!gameSession) {
            console.error('No game session available');
            return;
        }
        
        try {
            console.log('Getting question for session:', gameSession.session_id);
            
            const response = await fetch('http://127.0.0.1:5000/game/get_question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getJWTToken()}`
                },
                body: JSON.stringify({
                    session_id: gameSession.session_id,
                    class_id: gameSession.class_id || "class1"
                })
            });
            
            console.log(`API Response status: ${response.status}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            console.log('Question received:', result);
            
            // FIXED: Handle array response from backend
            let questionData = null;
            
            if (Array.isArray(result)) {
                console.log('Backend returned array with length:', result.length);
                if (result.length > 0) {
                    // Take the first question from array
                    questionData = result[0];
                    console.log('Using first question from array:', questionData);
                } else {
                    // Empty array - no questions available
                    console.error('No questions available for this session');
                    if (questionText) {
                        questionText.textContent = 'No more questions available for this difficulty level.';
                    }
                    setTimeout(() => {
                        alert('No more questions available! Game completed.');
                        handleGameEnd(true, gameSession?.monster_stats?.money_win || 0);
                    }, 1000);
                    return;
                }
            } else if (result && result.question && result.choices) {
                // Single object response (your previous working format)
                questionData = result;
                console.log('Using single question object:', questionData);
            } else {
                console.error('Invalid question response format:', result);
                if (questionText) {
                    questionText.textContent = 'Invalid question format received.';
                }
                return;
            }
            
            // Validate question data before loading
            if (questionData && questionData.question && questionData.choices) {
                currentQuestion = questionData;
                loadQuestion(questionData);
                
                // Start timer for new question
                startQuestionTimer();
            } else {
                console.error('Question data missing required fields:', questionData);
                if (questionText) {
                    questionText.textContent = 'Question data is incomplete.';
                }
            }
            
        } catch (error) {
            console.error('Failed to get question:', error);
            if (questionText) {
                questionText.textContent = 'Failed to load question. Please try again.';
            }
        }
    }

    // Submit answer to backend
   // REPLACE your submitAnswer function with this DEBUG version:

async function submitAnswer(answer) {
    if (!gameSession || !currentQuestion) {
        console.error('Cannot submit answer: missing session or question');
        return null;
    }
    
    // Stop timer when answer is submitted
    stopQuestionTimer();
    
    try {
        console.log('=== DEBUG SUBMIT ANSWER ===');
        console.log('User answer:', answer);
        console.log('Current question:', currentQuestion);
        console.log('Session ID:', gameSession.session_id);
        console.log('Question ID:', currentQuestion.id);
        console.log('Question type:', currentQuestion.type);
        console.log('Question choices:', currentQuestion.choices);
        
        const payload = {
            session_id: gameSession.session_id,
            question_id: currentQuestion.id,
            answer: answer
        };
        console.log('Sending payload:', JSON.stringify(payload, null, 2));
        
        const response = await fetch('http://127.0.0.1:5000/game/check_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getJWTToken()}`
            },
            body: JSON.stringify(payload)
        });
        
        console.log(`API Response status: ${response.status}`);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Response error:', errorText);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('=== BACKEND RESPONSE ===');
        console.log('Full result:', JSON.stringify(result, null, 2));
        console.log('Status:', result.status);
        console.log('Expected answer might be:', result.correct_answer || result.expected_answer);
        console.log('========================');
        
        return result;
    } catch (error) {
        console.error('Failed to submit answer:', error);
        return null;
    }
}

    // Update health bars with smooth animation
    function updateHealthBars() {
        const playerHealthPercent = playerMaxHealth > 0 ? (playerHealthValue / playerMaxHealth) * 100 : 0;
        const monsterHealthPercent = monsterMaxHealth > 0 ? (monsterHealthValue / monsterMaxHealth) * 100 : 0;
        
        if (playerHealth) {
            playerHealth.style.width = Math.max(0, playerHealthPercent) + '%';
            playerHealth.style.transition = 'width 0.5s ease-in-out';
        }
        if (monsterHealth) {
            monsterHealth.style.width = Math.max(0, monsterHealthPercent) + '%';
            monsterHealth.style.transition = 'width 0.5s ease-in-out';
        }
        
        const playerHealthText = document.querySelector('.player-stats .health-text');
        const monsterHealthText = document.querySelector('.monster-stats .health-text');
        
        if (playerHealthText) playerHealthText.textContent = Math.max(0, playerHealthValue);
        if (monsterHealthText) monsterHealthText.textContent = Math.max(0, monsterHealthValue);
        
        console.log('Health updated:', { player: playerHealthValue, monster: monsterHealthValue });
    }
    
    // Load a question from backend data
    // REPLACE your loadQuestion function with this UPDATED version:

function loadQuestion(questionData) {
    if (!questionData || !questionData.question) {
        console.error('Invalid question data:', questionData);
        if (questionText) {
            questionText.textContent = 'No question available.';
        }
        return;
    }
    
    console.log('Loading question:', questionData);
    
    // FIXED: Handle different question type formats from backend
    let questionType = questionData.type || 'single_choice';
    
    // Normalize question type names to match your frontend
    const typeMapping = {
        'fill_in_the_blank': 'fill_in_blank',  // Backend format -> Frontend format
        'fill_in_blank': 'fill_in_blank',      // Already correct
        'single_choice': 'single_choice',      // Already correct
        'multiple_choice': 'multiple_choice',   // Already correct
        'true_false': 'true_false'             // NEW: Add true/false support
    };
    
    // Map backend type to frontend type
    if (typeMapping[questionType]) {
        questionType = typeMapping[questionType];
    }
    
    console.log('Normalized question type:', questionType);
    
    // Update question type display if element exists
    const questionTypeElement = document.getElementById('questionTypeDisplay');
    if (questionTypeElement) {
        questionTypeElement.textContent = questionType.replace('_', ' ').toUpperCase();
    }
    
    // Hide all question types first
    hideAllQuestionTypes();
    
    if (questionType === 'single_choice' || questionType === 'multiple_choice') {
        loadMultipleChoiceQuestion(questionData);
        setupAnswerButtonListeners();
    } else if (questionType === 'fill_in_blank') {
        loadFillInBlankQuestion(questionData);
        setupFillInBlankListeners();
    } else if (questionType === 'true_false') {  // NEW: Handle true/false questions
        loadTrueFalseQuestion(questionData);
        setupTrueFalseListeners();
    } else {
        console.error('Unknown question type after mapping:', questionType);
        // Default to multiple choice as fallback
        console.log('Falling back to multiple choice format');
        loadMultipleChoiceQuestion(questionData);
        setupAnswerButtonListeners();
    }
}

// ADD these NEW functions after your existing load functions:

// Load true/false question
function loadTrueFalseQuestion(questionData) {
    console.log('Loading true/false question:', questionData);
    
    // Hide other question types
    const multipleChoiceElement = document.getElementById('multipleChoiceQuestion');
    const fillInBlankElement = document.getElementById('fillInBlankQuestion');
    if (multipleChoiceElement) multipleChoiceElement.style.display = 'none';
    if (fillInBlankElement) fillInBlankElement.style.display = 'none';
    
    // Show multiple choice container (reuse for True/False)
    if (multipleChoiceElement) {
        multipleChoiceElement.style.display = 'block';
    }
    
    // Update question text
    const questionTextElement = document.getElementById('questionText');
    if (questionTextElement) {
        questionTextElement.textContent = questionData.question || 'No question available';
        console.log('Updated question text to:', questionData.question);
    }
    
    // Get answer buttons and set them to True/False
    const currentAnswerButtons = document.querySelectorAll('.answer-btn');
    
    // Set first two buttons to True/False
    const trueFalseOptions = ['True', 'False'];
    
    currentAnswerButtons.forEach((button, index) => {
        if (index < 2) {
            button.textContent = trueFalseOptions[index];
            button.style.display = 'block';
            button.disabled = false;
        } else {
            // Hide extra buttons
            button.style.display = 'none';
        }
        
        // Clear previous styling
        button.classList.remove('correct', 'incorrect', 'timeout');
        button.style.backgroundColor = '';
        button.style.color = '';
    });
    
    console.log('True/False question loaded successfully');
}

// Setup event listeners for true/false questions
function setupTrueFalseListeners() {
    // Get fresh button references
    const trueFalseButtons = document.querySelectorAll('.answer-btn');
    
    // Remove existing listeners by cloning
    trueFalseButtons.forEach((button, index) => {
        if (index < 2) { // Only first 2 buttons for True/False
            button.replaceWith(button.cloneNode(true));
        }
    });
    
    // Get fresh references after cloning
    const freshButtons = document.querySelectorAll('.answer-btn');
    
    freshButtons.forEach((button, index) => {
        if (index < 2) { // Only handle True/False buttons
            button.addEventListener('click', async () => {
                if (!currentQuestion || button.disabled) return;
                
                console.log('True/False button clicked:', button.textContent);
                
                // Disable all buttons during processing
                freshButtons.forEach(btn => btn.disabled = true);
                
                const selectedAnswer = button.textContent;
                const result = await submitAnswer(selectedAnswer);
                
                if (!result) {
                    // Re-enable buttons if request failed
                    freshButtons.forEach(btn => btn.disabled = false);
                    return;
                }
                
                await handleAnswerResult(result, button, 'true_false');
            });
        }
    });
    
    console.log('True/False listeners setup complete');
}
    
    // Load multiple choice question with proper data mapping
    function loadMultipleChoiceQuestion(questionData) {
        console.log('Loading multiple choice question:', questionData);
        
        const multipleChoiceElement = document.getElementById('multipleChoiceQuestion');
        if (multipleChoiceElement) {
            multipleChoiceElement.style.display = 'block';
        }
        
        // CRITICAL FIX: Update the correct question text element
        const questionTextElement = document.getElementById('questionText');
        if (questionTextElement) {
            // Clear any previous content first
            questionTextElement.textContent = '';
            
            // Set the new question text
            const newQuestionText = questionData.question || 'No question available';
            questionTextElement.textContent = newQuestionText;
            
            console.log('Updated question text to:', newQuestionText);
        } else {
            console.error('questionText element not found!');
        }
        
        // Update answer buttons - handle backend format
        const choices = questionData.choices || [];
        console.log('Question choices:', choices);
        
        // Get fresh button references
        const currentAnswerButtons = document.querySelectorAll('.answer-btn');
        
        currentAnswerButtons.forEach((button, index) => {
            if (choices[index]) {
                button.textContent = choices[index];
                button.style.display = 'block';
                button.disabled = false;
            } else {
                button.style.display = 'none';
            }
            
            // IMPORTANT: Clear all previous styling
            button.classList.remove('correct', 'incorrect', 'timeout');
            button.style.backgroundColor = '';
            button.style.color = '';
        });
        
        console.log('Multiple choice question loaded successfully');
    }

    // FIXED: Load fill in the blank question (COMPLETE VERSION)
    function loadFillInBlankQuestion(questionData) {
        console.log('Loading fill in blank question:', questionData);
        
        // Hide multiple choice first
        const multipleChoiceElement = document.getElementById('multipleChoiceQuestion');
        if (multipleChoiceElement) {
            multipleChoiceElement.style.display = 'none';
        }
        
        // Show fill in blank container
        const fillInBlankElement = document.getElementById('fillInBlankQuestion');
        if (!fillInBlankElement) {
            console.error('Fill in blank element not found');
            return;
        }
        
        fillInBlankElement.style.display = 'block';
        
        // Get the question text
        const questionTextContent = questionData.question || '';
        console.log('Question text:', questionTextContent);
        
        // CRITICAL FIX: Update BOTH question text elements
        const questionTextElement = document.getElementById('questionText');
        const fillInBlankTextElement = document.getElementById('fillInBlankText');
        
        if (questionTextElement) {
            questionTextElement.textContent = questionTextContent;
            console.log('Updated main question text to:', questionTextContent);
        }
        
        if (fillInBlankTextElement) {
            fillInBlankTextElement.textContent = 'Complete the sentence:';
        }
        
        // Find and setup sentence parts
        const sentenceBefore = document.getElementById('sentenceBefore');
        const sentenceAfter = document.getElementById('sentenceAfter');
        const blankInput = document.getElementById('blankInput');
        
        // Parse question for blanks
        const parts = questionTextContent.split('____');
        if (parts.length >= 2) {
            // Question has explicit blanks
            if (sentenceBefore) sentenceBefore.textContent = parts[0].trim();
            if (sentenceAfter) sentenceAfter.textContent = parts[1].trim();
        } else {
            // No explicit blanks - look for common patterns
            const commonPatterns = [
                /(.+)\s+_+\s+(.+)/,  // "He ___ a teacher"
                /(.+)\s+\(\s*\)\s+(.+)/,  // "He ( ) a teacher"
                /(.+)\s+\[\s*\]\s+(.+)/   // "He [ ] a teacher"
            ];
            
            let patternMatched = false;
            for (const pattern of commonPatterns) {
                const match = questionTextContent.match(pattern);
                if (match) {
                    if (sentenceBefore) sentenceBefore.textContent = match[1].trim();
                    if (sentenceAfter) sentenceAfter.textContent = match[2].trim();
                    patternMatched = true;
                    break;
                }
            }
            
            if (!patternMatched) {
                // Default: put whole question before blank
                if (sentenceBefore) sentenceBefore.textContent = questionTextContent;
                if (sentenceAfter) sentenceAfter.textContent = '';
            }
        }
        
        // CRITICAL: Setup input field properly
        if (blankInput) {
            console.log('Setting up input field...');
            
            // Clear all restrictions and reset
            blankInput.value = '';
            blankInput.disabled = false;
            blankInput.readOnly = false;
            blankInput.style.display = 'inline-block';
            blankInput.style.visibility = 'visible';
            blankInput.style.pointerEvents = 'auto';
            blankInput.tabIndex = 0;
            
            // Remove any problematic attributes
            blankInput.removeAttribute('disabled');
            blankInput.removeAttribute('readonly');
            
            // Clear CSS classes that might interfere
            blankInput.classList.remove('correct', 'incorrect', 'timeout', 'disabled');
            
            // ENHANCED: Multiple focus attempts with better timing
            setTimeout(() => {
                blankInput.focus();
                console.log('First focus attempt');
            }, 100);
            
            setTimeout(() => {
                blankInput.focus();
                blankInput.click();
                console.log('Second focus with click');
            }, 300);
            
            setTimeout(() => {
                // Test if input is working
                const testFocus = document.activeElement === blankInput;
                console.log('Input focus test:', testFocus);
                
                if (!testFocus) {
                    blankInput.focus();
                    console.log('Final focus attempt');
                }
            }, 500);
        } else {
            console.error('blankInput element not found!');
        }
        
        // Setup submit button
        const submitBtn = document.getElementById('submitAnswerBtn');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.style.display = 'inline-block';
        }
        
        // Setup hint if available
        const hintText = document.getElementById('hintText');
        const showHintBtn = document.getElementById('showHintBtn');
        if (hintText && showHintBtn) {
            if (questionData.hint) {
                hintText.textContent = questionData.hint;
                showHintBtn.style.display = 'inline-block';
            } else {
                showHintBtn.style.display = 'none';
            }
            hintText.style.display = 'none';
        }
        
        // Hide feedback area
        const feedbackArea = document.getElementById('feedbackArea');
        if (feedbackArea) feedbackArea.style.display = 'none';
        
        // Hide next question button
        const nextQuestionBtn = document.getElementById('nextQuestionBtn');
        if (nextQuestionBtn) nextQuestionBtn.style.display = 'none';
        
        console.log('Fill in blank question loaded successfully');
    }

    // Setup event listeners for multiple choice buttons
    function setupAnswerButtonListeners() {
        answerButtons.forEach((button, index) => {
            // Remove any existing listeners first
            button.replaceWith(button.cloneNode(true));
        });
        
        // Get fresh button references after cloning
        const freshButtons = document.querySelectorAll('.answer-btn');
        
        freshButtons.forEach((button, index) => {
            button.addEventListener('click', async () => {
                if (!currentQuestion || button.disabled) return;
                
                console.log('Answer button clicked:', button.textContent);
                
                // Disable all buttons during processing
                freshButtons.forEach(btn => btn.disabled = true);
                
                const selectedAnswer = button.textContent;
                const result = await submitAnswer(selectedAnswer);
                
                if (!result) {
                    // Re-enable buttons if request failed
                    freshButtons.forEach(btn => btn.disabled = false);
                    return;
                }
                
                await handleAnswerResult(result, button, 'multiple_choice');
            });
        });
    }

    // Setup event listeners for fill-in-blank
    function setupFillInBlankListeners() {
        // Handle submit button
        const submitAnswerBtn = document.getElementById('submitAnswerBtn');
        if (submitAnswerBtn) {
            // Remove any existing listeners
            submitAnswerBtn.replaceWith(submitAnswerBtn.cloneNode(true));
            const newSubmitBtn = document.getElementById('submitAnswerBtn');
            
            newSubmitBtn.addEventListener('click', async () => {
                console.log('Submit button clicked');
                const blankInput = document.getElementById('blankInput');
                if (!blankInput) {
                    console.log('Blank input not found');
                    return;
                }
                
                const userAnswer = blankInput.value.trim();
                console.log('User answer:', userAnswer);
                
                if (!userAnswer) {
                    alert('Please enter an answer!');
                    blankInput.focus();
                    return;
                }
                
                console.log('Fill in blank answer submitted:', userAnswer);
                
                // Disable submit button to prevent double submission
                newSubmitBtn.disabled = true;
                blankInput.disabled = true;
                
                const result = await submitAnswer(userAnswer);
                await handleFillInBlankResult(result, userAnswer);
            });
        }

        // Handle hint button
        const showHintBtn = document.getElementById('showHintBtn');
        if (showHintBtn) {
            showHintBtn.replaceWith(showHintBtn.cloneNode(true));
            const newHintBtn = document.getElementById('showHintBtn');
            
            newHintBtn.addEventListener('click', () => {
                const hintText = document.getElementById('hintText');
                if (!hintText) return;
                
                if (hintText.style.display === 'none' || !hintText.style.display) {
                    hintText.style.display = 'block';
                    newHintBtn.textContent = 'Hide Hint';
                } else {
                    hintText.style.display = 'none';
                    newHintBtn.textContent = 'Show Hint';
                }
            });
        }

        // Handle clear button
        const clearBtn = document.getElementById('clearBtn');
        if (clearBtn) {
            clearBtn.replaceWith(clearBtn.cloneNode(true));
            const newClearBtn = document.getElementById('clearBtn');
            
            newClearBtn.addEventListener('click', () => {
                const blankInput = document.getElementById('blankInput');
                if (blankInput) {
                    blankInput.value = '';
                    blankInput.focus();
                }
            });
        }

        // Handle Enter key for input
        const blankInput = document.getElementById('blankInput');
        if (blankInput) {
            blankInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const submitBtn = document.getElementById('submitAnswerBtn');
                    if (submitBtn && !submitBtn.disabled) {
                        submitBtn.click();
                    }
                }
            });
        }
    }

    // Handle answer result for multiple choice with enhanced animations
    async function handleAnswerResult(result, buttonElement, questionType) {
        // Backend returns status: "correct" or other values
        const isCorrect = result.status === "correct";
        
        console.log('Handling answer result:', { result, isCorrect });
        
        if (isCorrect) {
            buttonElement.classList.add('correct');
            
            try {
                if (typeof playAttackSFX === 'function') playAttackSFX();
            } catch (error) {
                console.log('Attack SFX failed:', error);
            }
            
            // Player attack animation
            if (player) {
                player.style.transform = 'translateX(30px)';
                player.style.transition = 'transform 0.3s ease-in-out';
            }
            
            setTimeout(() => {
                if (attackEffect) {
                    attackEffect.style.opacity = '1';
                    attackEffect.style.transform = 'scale(1.2)';
                }
                
                // Show damage number
                if (damageNumber) {
                    damageNumber.textContent = PLAYER_DAMAGE;
                    damageNumber.style.opacity = '1';
                    damageNumber.style.transform = 'translate(-50%, -50%) scale(1.2)';
                }
                
                // Update health from backend response or locally
                if (result.monster_hp !== undefined) {
                    monsterHealthValue = result.monster_hp;
                } else {
                    monsterHealthValue = Math.max(0, monsterHealthValue - PLAYER_DAMAGE);
                }
                updateHealthBars();
                
                if (monster) {
                    monster.style.transform = 'translateX(15px) rotate(5deg)';
                    monster.style.filter = 'brightness(0.7) hue-rotate(0deg)';
                }
                
                setTimeout(async () => {
                    if (player) player.style.transform = '';
                    if (attackEffect) {
                        attackEffect.style.opacity = '0';
                        attackEffect.style.transform = '';
                    }
                    if (damageNumber) {
                        damageNumber.style.opacity = '0';
                        damageNumber.style.transform = 'translate(-50%, -50%) scale(1)';
                    }
                    if (monster) {
                        monster.style.transform = '';
                        monster.style.filter = '';
                    }
                    
                    // Reset button styling
                    answerButtons.forEach(btn => {
                        btn.classList.remove('correct', 'incorrect');
                        btn.disabled = false;
                    });
                    
                    // FIXED: Check win condition and auto-advance
                    if (monsterHealthValue <= 0) {
                        handleGameEnd(true, gameSession?.monster_stats?.money_win || 0);
                    } else {
                        // AUTO-ADVANCE: Get next question automatically for correct answers
                        console.log('Correct answer - auto-advancing to next question');
                        await getQuestion();
                    }
                }, 1500);
            }, 300);
        } else {
            buttonElement.classList.add('incorrect');
            
            try {
                if (typeof playHitSFX === 'function') playHitSFX();
            } catch (error) {
                console.log('Hit SFX failed:', error);
            }
            
            // Monster attack
            if (monster) {
                monster.style.transform = 'translateX(-30px)';
                monster.style.transition = 'transform 0.3s ease-in-out';
            }
            
            setTimeout(() => {
                // Update player health from backend response or locally
                if (result.player_hp !== undefined) {
                    playerHealthValue = result.player_hp;
                } else {
                    playerHealthValue = Math.max(0, playerHealthValue - MONSTER_DAMAGE);
                }
                updateHealthBars();
                
                if (player) {
                    player.style.transform = 'translateX(-15px) rotate(-5deg)';
                    player.style.filter = 'brightness(0.7) sepia(1) hue-rotate(0deg)';
                }
                
                setTimeout(async () => {
                    if (monster) monster.style.transform = '';
                    if (player) {
                        player.style.transform = '';
                        player.style.filter = '';
                    }
                    
                    // Reset button styling
                    answerButtons.forEach(btn => {
                        btn.classList.remove('correct', 'incorrect');
                        btn.disabled = false;
                    });
                    
                    // FIXED: Check lose condition and auto-advance
                    if (playerHealthValue <= 0) {
                        handleGameEnd(false);
                    } else {
                        // AUTO-ADVANCE: Get next question automatically even for wrong answers
                        console.log('Incorrect answer - auto-advancing to next question');
                        await getQuestion();
                    }
                }, 1500);
            }, 300);
        }
    }
    
    async function handleFillInBlankResult(result, userAnswer) {
        const blankInput = document.getElementById('blankInput');
        const feedbackArea = document.getElementById('feedbackArea');
        const feedbackText = document.getElementById('feedbackText');
        const submitBtn = document.getElementById('submitAnswerBtn');
        
        if (!blankInput || result === null || result === undefined) return;
        
        blankInput.disabled = true;
        if (submitBtn) submitBtn.disabled = true;
        
        // Backend returns status: "correct" or other values
        const isCorrect = result.status === "correct";
        
        console.log('Handling fill in blank result:', { result, isCorrect });
        
        if (isCorrect) {
            // Correct answer
            blankInput.classList.add('correct');
            if (feedbackArea) {
                feedbackArea.className = 'feedback-area correct';
                feedbackArea.style.display = 'block';
            }
            if (feedbackText) {
                feedbackText.className = 'feedback-text correct';
                feedbackText.textContent = result.feedback || 'Correct! Well done!';
            }
            
            try {
                if (typeof playAttackSFX === 'function') playAttackSFX();
            } catch (error) {
                console.log('Attack SFX failed:', error);
            }
            
            // Player attack animation
            if (player) player.style.transform = 'translateX(30px)';
            setTimeout(() => {
                if (attackEffect) attackEffect.style.opacity = '1';
                
                if (damageNumber) {
                    damageNumber.textContent = PLAYER_DAMAGE;
                    damageNumber.style.opacity = '1';
                }
                
                // Update health from backend response or locally
                if (result.monster_hp !== undefined) {
                    monsterHealthValue = result.monster_hp;
                } else {
                    monsterHealthValue = Math.max(0, monsterHealthValue - PLAYER_DAMAGE);
                }
                updateHealthBars();
                
                if (monster) monster.style.transform = 'translateX(15px) rotate(5deg)';
                
                setTimeout(async () => {
                    if (player) player.style.transform = '';
                    if (attackEffect) attackEffect.style.opacity = '0';
                    if (damageNumber) damageNumber.style.opacity = '0';
                    if (monster) monster.style.transform = '';
                    
                    // FIXED: Check game status and auto-advance
                    if (monsterHealthValue <= 0) {
                        handleGameEnd(true, gameSession?.monster_stats?.money_win || 0);
                    } else {
                        // AUTO-ADVANCE: Get next question automatically for correct answers
                        console.log('Correct answer - auto-advancing to next question');
                        resetFillInBlankUI();
                        await getQuestion();
                    }
                }, 1000);
            }, 200);
        } else {
            // Incorrect answer
            blankInput.classList.add('incorrect');
            if (feedbackArea) {
                feedbackArea.className = 'feedback-area incorrect';
                feedbackArea.style.display = 'block';
            }
            if (feedbackText) {
                feedbackText.className = 'feedback-text incorrect';
                feedbackText.textContent = result.feedback || 'Incorrect. Please try again!';
            }
            
            try {
                if (typeof playHitSFX === 'function') playHitSFX();
            } catch (error) {
                console.log('Hit SFX failed:', error);
            }
            
            // Monster attack
            if (monster) monster.style.transform = 'translateX(-30px)';
            setTimeout(() => {
                // Update player health from backend response or locally
                if (result.player_hp !== undefined) {
                    playerHealthValue = result.player_hp;
                } else {
                    playerHealthValue = Math.max(0, playerHealthValue - MONSTER_DAMAGE);
                }
                updateHealthBars();
                
                if (player) player.style.transform = 'translateX(-15px) rotate(-5deg)';
                
                setTimeout(async () => {
                    if (monster) monster.style.transform = '';
                    if (player) player.style.transform = '';
                    
                    // FIXED: Check game status and auto-advance
                    if (playerHealthValue <= 0) {
                        handleGameEnd(false);
                    } else {
                        // AUTO-ADVANCE: Get next question automatically for wrong answers too
                        console.log('Incorrect answer - auto-advancing to next question');
                        resetFillInBlankUI();
                        await getQuestion();
                    }
                }, 1000);
            }, 200);
        }
    }
    
    // Reset fill in blank UI elements
    function resetFillInBlankUI() {
        const blankInput = document.getElementById('blankInput');
        const feedbackArea = document.getElementById('feedbackArea');
        const nextQuestionBtn = document.getElementById('nextQuestionBtn');
        const submitBtn = document.getElementById('submitAnswerBtn');
        const hintText = document.getElementById('hintText');
        const showHintBtn = document.getElementById('showHintBtn');
        
        if (blankInput) {
            blankInput.value = '';
            blankInput.disabled = false;
            blankInput.readOnly = false;
            blankInput.classList.remove('correct', 'incorrect', 'timeout');
        }
        if (feedbackArea) feedbackArea.style.display = 'none';
        if (nextQuestionBtn) nextQuestionBtn.style.display = 'none';
        if (submitBtn) submitBtn.disabled = false;
        if (hintText) hintText.style.display = 'none';
        if (showHintBtn) showHintBtn.textContent = 'Show Hint';
    }
    
    // Handle game end - navigate instead of reset
    function handleGameEnd(isWin, reward = 0) {
        // Stop timer when game ends
        stopQuestionTimer();
        
        console.log('Game ended:', { isWin, reward });
        
        if (isWin) {
            // Show win dialog and navigate
            setTimeout(() => {
                window.location.href = `/client/gameResult.html?result=win&reward=${reward}`;
            }, 500);
        } else {
            // Show lose dialog and navigate  
            setTimeout(() => {
                window.location.href = '/client/gameResult.html?result=lose';
            }, 500);
        }
    }

    // Get game parameters from URL
    function getGameDifficulty() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('difficulty') || 'easy';
    }

    function getClassId() {
        const urlParams = new URLSearchParams(window.location.search);
        return parseInt(urlParams.get('classId')) || 1;
    }
    
    // Initialize the game with comprehensive error handling
    async function initializeGame() {
        try {
            console.log('Starting game initialization...');
            
            const difficulty = getGameDifficulty();
            const classId = getClassId();
            
            console.log('Game parameters:', { difficulty, classId });
            
            await createGameRoom(difficulty, classId);
            
            console.log('Game initialized successfully');

            // FIXED: Use correct element IDs from your HTML
            const battleScene = document.getElementById('battleScene');
            const questionArea = document.getElementById('questionArea');
            const loadingScreen = document.getElementById('loadingScreen');
            
            if (battleScene && questionArea) {
                // Show game screen using your HTML structure
                showGameScreen();
                console.log('Game screen displayed successfully');
            } else {
                console.error('Required game elements not found in HTML!');
                console.log('battleScene found:', !!battleScene);
                console.log('questionArea found:', !!questionArea);
                showErrorScreen();
            }
            
        } catch (error) {
            console.error('Failed to initialize game:', error);
            showErrorScreen();
        }
    }

    // Global event handlers
    function setupGlobalEventHandlers() {
        // Enhanced click handler for input focus
        document.addEventListener('click', (e) => {
            const blankInput = document.getElementById('blankInput');
            if (e.target === blankInput && blankInput) {
                setTimeout(() => {
                    blankInput.focus();
                }, 10);
            }
        });
    }

    // Initialize event listeners and start game
    setupGlobalEventHandlers();
    
    // Start the game
    console.log('DOM loaded, initializing game...');
    initializeGame();
});