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

    // JWT Token management
    function getJWTToken() {
        return localStorage.getItem('jwtToken') || sessionStorage.getItem('jwtToken');
    }
    
    // API call function
    async function makeAPIRequest(endpoint, data, method = 'POST') {
        const token = getJWTToken();
        
        try {
            const response = await fetch(`/api/${endpoint}`, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: method !== 'GET' ? JSON.stringify(data) : undefined
            });
            
            if (!response.ok) {
                if (response.status === 401) {
                    localStorage.removeItem('jwtToken');
                    sessionStorage.removeItem('jwtToken');
                    window.location.href = '/login';
                    return;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
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
    }
    
    function stopQuestionTimer() {
        if (questionTimer) {
            clearInterval(questionTimer);
            questionTimer = null;
        }
    }
    
   // Update the updateTimerDisplay function
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
            // Handle as fill-in-blank timeout
            await handleFillInBlankTimeout(result);
        } else {
            // Handle as multiple choice timeout
            await handleMultipleChoiceTimeout(result);
        }
    }
    
    async function handleMultipleChoiceTimeout(result) {
        // Show timeout message
        answerButtons.forEach(btn => {
            btn.classList.add('timeout');
            btn.textContent = btn.textContent + ' (TIMEOUT)';
        });
        
        // Treat timeout as incorrect answer
        if (typeof playHitSFX === 'function') playHitSFX();
        
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
    
    async function handleFillInBlankTimeout(result) {
        const blankInput = document.getElementById('blankInput');
        const feedbackArea = document.getElementById('feedbackArea');
        const feedbackText = document.getElementById('feedbackText');
        const nextQuestionBtn = document.getElementById('nextQuestionBtn');
        
        if (blankInput) {
            blankInput.value = 'TIMEOUT';
            blankInput.classList.add('timeout');
        }
        
        // Show timeout feedback
        if (feedbackArea) {
            feedbackArea.className = 'feedback-area incorrect';
            feedbackArea.style.display = 'block';
        }
        if (feedbackText) {
            feedbackText.className = 'feedback-text incorrect';
            feedbackText.textContent = 'Time is up! You took too long to answer.';
        }
        
        if (typeof playHitSFX === 'function') playHitSFX();
        
        // Monster attack animation
        if (monster) monster.style.transform = 'translateX(-30px)';
        setTimeout(() => {
            // Update player health locally
            playerHealthValue = Math.max(0, playerHealthValue - MONSTER_DAMAGE);
            updateHealthBars();
            
            if (player) player.style.transform = 'translateX(-15px) rotate(-5deg)';
            
            setTimeout(() => {
                if (monster) monster.style.transform = '';
                if (player) player.style.transform = '';
                
                // Check game status
                if (playerHealthValue <= 0) {
                    handleGameEnd(false);
                } else {
                    if (nextQuestionBtn) nextQuestionBtn.style.display = 'inline-block';
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
        if (playerLevelElement) playerLevelElement.textContent = sessionData.player_level || '1';
        if (monsterLevelElement) monsterLevelElement.textContent = sessionData.monster_level || '1';
    }

    // Create game room
    async function createGameRoom(difficulty = 'easy', classId = 1) {
        try {
            showLoadingScreen();
            
            const response = await makeAPIRequest('game/create-room', {
                difficulty: difficulty,
                class_id: classId
            });
            
            gameSession = response;
            
            // Update game state with backend data
            playerHealthValue = response.player_stats.hp;
            playerMaxHealth = response.player_stats.hp;
            
            monsterHealthValue = response.monster_stats.hp;
            monsterMaxHealth = response.monster_stats.hp;
            
            // Update UI with backend data
            updateGameInfo(response);
            updateHealthBars();
            
            // Get first question
            await getQuestion();
            
            // Show game screen
            showGameScreen();
            
            return response;
        } catch (error) {
            console.error('Failed to create game room:', error);
            showErrorScreen();
        }
    }

    // Get question from backend
    async function getQuestion() {
        if (!gameSession) return;
        
        try {
            const response = await makeAPIRequest('game/get-question', {
                session_id: gameSession.session_id
            });
            
            if (response && response.question) {
                currentQuestion = response;
                loadQuestion(response);
                
                // Start timer for new question
                startQuestionTimer();
            }
        } catch (error) {
            console.error('Failed to get question:', error);
            if (questionText) {
                questionText.textContent = 'Failed to load question. Please try again.';
            }
        }
    }

    // Submit answer to backend
    async function submitAnswer(answer) {
        if (!gameSession || !currentQuestion) return;
        
        // Stop timer when answer is submitted
        stopQuestionTimer();
        
        try {
            const response = await makeAPIRequest('game/check-answer', {
                session_id: gameSession.session_id,
                answer: answer
            });
            
            return response;
        } catch (error) {
            console.error('Failed to submit answer:', error);
            return null;
        }
    }

    // Update health bars
    function updateHealthBars() {
        const playerHealthPercent = playerMaxHealth > 0 ? (playerHealthValue / playerMaxHealth) * 100 : 0;
        const monsterHealthPercent = monsterMaxHealth > 0 ? (monsterHealthValue / monsterMaxHealth) * 100 : 0;
        
        if (playerHealth) playerHealth.style.width = Math.max(0, playerHealthPercent) + '%';
        if (monsterHealth) monsterHealth.style.width = Math.max(0, monsterHealthPercent) + '%';
        
        const playerHealthText = document.querySelector('.player-stats .health-text');
        const monsterHealthText = document.querySelector('.monster-stats .health-text');
        
        if (playerHealthText) playerHealthText.textContent = Math.max(0, playerHealthValue);
        if (monsterHealthText) monsterHealthText.textContent = Math.max(0, monsterHealthValue);
    }
    
    // Load a question from backend data
    function loadQuestion(questionData) {
        if (!questionData || !questionData.question) {
            if (questionText) {
                questionText.textContent = 'No question available.';
            }
            return;
        }
        
        const questionType = questionData.question.type || questionData.type || 'multiple_choice';
        
        // Update question type display if element exists
        const questionTypeElement = document.getElementById('questionType');
        if (questionTypeElement) {
            questionTypeElement.textContent = questionType.replace('_', ' ').toUpperCase();
        }
        
        // Hide all question types first
        hideAllQuestionTypes();
        
        if (questionType === 'multiple_choice') {
            loadMultipleChoiceQuestion(questionData);
        } else if (questionType === 'fill_in_blank') {
            loadFillInBlankQuestion(questionData);
        }
    }
    
    // Hide all question type containers
    function hideAllQuestionTypes() {
        const multipleChoiceElement = document.getElementById('multipleChoiceQuestion');
        const fillInBlankElement = document.getElementById('fillInBlankQuestion');
        
        if (multipleChoiceElement) multipleChoiceElement.style.display = 'none';
        if (fillInBlankElement) fillInBlankElement.style.display = 'none';
    }
    
    // Load multiple choice question
    function loadMultipleChoiceQuestion(questionData) {
        const multipleChoiceElement = document.getElementById('multipleChoiceQuestion');
        if (multipleChoiceElement) {
            multipleChoiceElement.style.display = 'block';
        }
        
        // Update question text
        if (questionText) {
            questionText.textContent = questionData.question.text || questionData.question;
        }
        
        // Update answer buttons
        const choices = questionData.question.choices || questionData.choices || [];
        answerButtons.forEach((button, index) => {
            if (choices[index]) {
                button.textContent = choices[index];
                button.style.display = 'block';
                button.disabled = false;
            } else {
                button.style.display = 'none';
            }
            button.classList.remove('correct', 'incorrect', 'timeout');
        });
    }
    
    // Load fill in the blank question
    function loadFillInBlankQuestion(questionData) {
        const fillInBlankElement = document.getElementById('fillInBlankQuestion');
        if (!fillInBlankElement) return;
        
        fillInBlankElement.style.display = 'block';
        
        const question = questionData.question;
        
        // Update question components
        const fillInBlankText = document.getElementById('fillInBlankText');
        const sentenceBefore = document.getElementById('sentenceBefore');
        const sentenceAfter = document.getElementById('sentenceAfter');
        const hintText = document.getElementById('hintText');
        const showHintBtn = document.getElementById('showHintBtn');
        const blankInput = document.getElementById('blankInput');
        const feedbackArea = document.getElementById('feedbackArea');
        const submitBtn = document.getElementById('submitAnswerBtn');
        
        if (fillInBlankText) {
            fillInBlankText.textContent = question.instruction || 'Complete the sentence:';
        }
        if (sentenceBefore) {
            sentenceBefore.textContent = question.sentence_before || '';
        }
        if (sentenceAfter) {
            sentenceAfter.textContent = question.sentence_after || '';
        }
        
        // Setup hint
        if (hintText && showHintBtn) {
            if (question.hint) {
                hintText.textContent = question.hint;
                showHintBtn.style.display = 'inline-block';
            } else {
                showHintBtn.style.display = 'none';
            }
        }
        
        // Reset input and feedback
        if (blankInput) {
            blankInput.value = '';
            blankInput.disabled = false;
            blankInput.classList.remove('correct', 'incorrect', 'timeout');
        }
        
        if (feedbackArea) {
            feedbackArea.style.display = 'none';
        }
        
        if (hintText) {
            hintText.style.display = 'none';
        }
        
        if (submitBtn) {
            submitBtn.disabled = false;
        }
    }
    
    // Handle multiple choice answer button clicks
    answerButtons.forEach((button, index) => {
        button.addEventListener('click', async () => {
            if (!currentQuestion || button.disabled) return;
            
            // Disable all buttons during processing
            answerButtons.forEach(btn => btn.disabled = true);
            
            const selectedAnswer = button.textContent;
            const result = await submitAnswer(selectedAnswer);
            
            if (!result) {
                // Re-enable buttons if request failed
                answerButtons.forEach(btn => btn.disabled = false);
                return;
            }
            
            await handleAnswerResult(result, button, 'multiple_choice');
        });
    });
    
    // Handle fill in the blank interactions
    const submitAnswerBtn = document.getElementById('submitAnswerBtn');
    if (submitAnswerBtn) {
        submitAnswerBtn.addEventListener('click', async () => {
            const blankInput = document.getElementById('blankInput');
            if (!blankInput) return;
            
            const userAnswer = blankInput.value.trim();
            
            if (!userAnswer) {
                alert('Please enter an answer!');
                return;
            }
            
            const result = await submitAnswer(userAnswer);
            await handleFillInBlankResult(result, userAnswer);
        });
    }
    
    const showHintBtn = document.getElementById('showHintBtn');
    if (showHintBtn) {
        showHintBtn.addEventListener('click', () => {
            const hintText = document.getElementById('hintText');
            if (!hintText) return;
            
            if (hintText.style.display === 'none' || !hintText.style.display) {
                hintText.style.display = 'block';
                showHintBtn.textContent = 'Hide Hint';
            } else {
                hintText.style.display = 'none';
                showHintBtn.textContent = 'Show Hint';
            }
        });
    }
    
    const clearBtn = document.getElementById('clearBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            const blankInput = document.getElementById('blankInput');
            if (blankInput) {
                blankInput.value = '';
                blankInput.focus();
            }
        });
    }
    
    const nextQuestionBtn = document.getElementById('nextQuestionBtn');
    if (nextQuestionBtn) {
        nextQuestionBtn.addEventListener('click', async () => {
            // Reset fill-in-blank UI elements
            resetFillInBlankUI();
            // Get next question
            await getQuestion();
        });
    }
    
    // Enter key support for fill in blank
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
    
    // Handle answer result for multiple choice
    async function handleAnswerResult(result, buttonElement, questionType) {
        // Backend trả về true/false hoặc object với correct property
        const isCorrect = result === true || result.correct === true;
        
        if (isCorrect) {
            buttonElement.classList.add('correct');
            if (typeof playAttackSFX === 'function') playAttackSFX();
            
            // Player attack animation
            if (player) player.style.transform = 'translateX(30px)';
            setTimeout(() => {
                if (attackEffect) attackEffect.style.opacity = '1';
                
                // Show damage number
                if (damageNumber) {
                    damageNumber.textContent = PLAYER_DAMAGE;
                    damageNumber.style.opacity = '1';
                }
                
                // Update health locally (vì backend chỉ trả về true/false)
                monsterHealthValue = Math.max(0, monsterHealthValue - PLAYER_DAMAGE);
                updateHealthBars();
                
                if (monster) monster.style.transform = 'translateX(15px) rotate(5deg)';
                
                setTimeout(async () => {
                    if (player) player.style.transform = '';
                    if (attackEffect) attackEffect.style.opacity = '0';
                    if (damageNumber) damageNumber.style.opacity = '0';
                    if (monster) monster.style.transform = '';
                    
                    // Reset button styling
                    answerButtons.forEach(btn => {
                        btn.classList.remove('correct', 'incorrect');
                        btn.disabled = false;
                    });
                    
                    // Check win condition locally
                    if (monsterHealthValue <= 0) {
                        handleGameEnd(true, gameSession?.monster_stats?.money_win || 0);
                    } else {
                        // Get next question
                        await getQuestion();
                    }
                }, 1000);
            }, 200);
        } else {
            buttonElement.classList.add('incorrect');
            if (typeof playHitSFX === 'function') playHitSFX();
            
            // Monster attack
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
                        btn.classList.remove('correct', 'incorrect');
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
    }
    
    // Handle fill in the blank result
    async function handleFillInBlankResult(result, userAnswer) {
        const blankInput = document.getElementById('blankInput');
        const feedbackArea = document.getElementById('feedbackArea');
        const feedbackText = document.getElementById('feedbackText');
        const nextQuestionBtn = document.getElementById('nextQuestionBtn');
        const submitBtn = document.getElementById('submitAnswerBtn');
        
        if (!blankInput || result === null || result === undefined) return;
        
        blankInput.disabled = true;
        if (submitBtn) submitBtn.disabled = true;
        
        // Backend trả về true/false hoặc object với correct property
        const isCorrect = result === true || result.correct === true;
        
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
            
            if (typeof playAttackSFX === 'function') playAttackSFX();
            
            // Player attack animation
            if (player) player.style.transform = 'translateX(30px)';
            setTimeout(() => {
                if (attackEffect) attackEffect.style.opacity = '1';
                
                if (damageNumber) {
                    damageNumber.textContent = PLAYER_DAMAGE;
                    damageNumber.style.opacity = '1';
                }
                
                // Update health locally
                monsterHealthValue = Math.max(0, monsterHealthValue - PLAYER_DAMAGE);
                updateHealthBars();
                
                if (monster) monster.style.transform = 'translateX(15px) rotate(5deg)';
                
                setTimeout(() => {
                    if (player) player.style.transform = '';
                    if (attackEffect) attackEffect.style.opacity = '0';
                    if (damageNumber) damageNumber.style.opacity = '0';
                    if (monster) monster.style.transform = '';
                    
                    // Check game status
                    if (monsterHealthValue <= 0) {
                        handleGameEnd(true, gameSession?.monster_stats?.money_win || 0);
                    } else {
                        if (nextQuestionBtn) nextQuestionBtn.style.display = 'inline-block';
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
            
            if (typeof playHitSFX === 'function') playHitSFX();
            
            // Monster attack
            if (monster) monster.style.transform = 'translateX(-30px)';
            setTimeout(() => {
                // Update player health locally
                playerHealthValue = Math.max(0, playerHealthValue - MONSTER_DAMAGE);
                updateHealthBars();
                
                if (player) player.style.transform = 'translateX(-15px) rotate(-5deg)';
                
                setTimeout(() => {
                    if (monster) monster.style.transform = '';
                    if (player) player.style.transform = '';
                    
                    // Check game status
                    if (playerHealthValue <= 0) {
                        handleGameEnd(false);
                    } else {
                        if (nextQuestionBtn) nextQuestionBtn.style.display = 'inline-block';
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
        
        if (isWin) {
            // Show win dialog and navigate
            setTimeout(() => {
                alert(`You won! The monster has been defeated! You earned ${reward} coins!`);
                // Navigate to results or menu
                window.location.href = `/game-results?result=win&reward=${reward}`;
                // Or back to menu
                // window.location.href = '/menu';
            }, 500);
        } else {
            // Show lose dialog and navigate  
            setTimeout(() => {
                alert('Game Over! You have been defeated!');
                // Navigate to results or menu
                window.location.href = `/game-results?result=lose`;
                // Or back to menu
                // window.location.href = '/menu';
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
    
    // Initialize the game
    async function initializeGame() {
        const difficulty = getGameDifficulty();
        const classId = getClassId();
        await createGameRoom(difficulty, classId);
    }

    // Start the game
    initializeGame();
});