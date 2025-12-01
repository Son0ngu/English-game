document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const playerHealth = document.querySelector('.player-health');
    const monsterHealth = document.querySelector('.monster-health');
    const damageNumber = document.getElementById('damageNumber');
    const attackEffect = document.getElementById('attackEffect');
    const answerButtons = document.querySelectorAll('.answer-btn');
    const player = document.querySelector('.player img');
    const monster = document.querySelector('.monster img');
    const questionText = document.querySelector('.question-text');
    
    // Game questions
    const questions = [
        {
            question: "What is the past tense of \"go\"?",
            answers: [
                { text: "gone", correct: false },
                { text: "went", correct: true },
                { text: "going", correct: false },
                { text: "goes", correct: false }
            ]
        },
        {
            question: "Which word is a synonym for \"happy\"?",
            answers: [
                { text: "sad", correct: false },
                { text: "joyful", correct: true },
                { text: "angry", correct: false },
                { text: "tired", correct: false }
            ]
        },
        {
            question: "What is the plural form of \"child\"?",
            answers: [
                { text: "childs", correct: false },
                { text: "children", correct: true },
                { text: "childen", correct: false },
                { text: "childs", correct: false }
            ]
        }
    ];
    
    let currentQuestion = 0;
    let playerHealthValue = 76;
    let monsterHealthValue = 45;
    
    // Load a question
    function loadQuestion(questionIndex) {
        const question = questions[questionIndex];
        questionText.textContent = question.question;
        
        answerButtons.forEach((button, index) => {
            button.textContent = question.answers[index].text;
            button.dataset.correct = question.answers[index].correct;
        });
    }
    
    // Handle answer button click
    answerButtons.forEach(button => {
        button.addEventListener('click', () => {
            const isCorrect = button.dataset.correct === "true";
            
            if (isCorrect) {
                // Correct answer
                button.classList.add('correct');
                
                // Player attack animation
                player.style.transform = 'translateX(30px)';
                setTimeout(() => {
                    attackEffect.style.opacity = '1';
                    damageNumber.style.opacity = '1';
                    
                    // Reduce monster health
                    monsterHealthValue -= 10;
                    if (monsterHealthValue < 0) monsterHealthValue = 0;
                    monsterHealth.style.width = monsterHealthValue + '%';
                    document.querySelector('.monster-stats .health-text').textContent = monsterHealthValue;
                    
                    monster.style.transform = 'translateX(15px) rotate(5deg)';
                    
                    setTimeout(() => {
                        player.style.transform = '';
                        attackEffect.style.opacity = '0';
                        damageNumber.style.opacity = '0';
                        monster.style.transform = '';
                        
                        // Load next question
                        currentQuestion = (currentQuestion + 1) % questions.length;
                        loadQuestion(currentQuestion);
                        
                        // Reset button styling
                        answerButtons.forEach(btn => btn.classList.remove('correct', 'incorrect'));
                        
                        // Check win condition
                        if (monsterHealthValue <= 0) {
                            setTimeout(() => {
                                alert('You won! The monster has been defeated!');
                                resetGame();
                            }, 500);
                        }
                    }, 1000);
                }, 200);
            } else {
                // Incorrect answer
                button.classList.add('incorrect');
                
                // Monster attack
                monster.style.transform = 'translateX(-30px)';
                setTimeout(() => {
                    // Reduce player health
                    playerHealthValue -= 5;
                    if (playerHealthValue < 0) playerHealthValue = 0;
                    playerHealth.style.width = playerHealthValue + '%';
                    document.querySelector('.player-stats .health-text').textContent = playerHealthValue;
                    
                    player.style.transform = 'translateX(-15px) rotate(-5deg)';
                    
                    setTimeout(() => {
                        monster.style.transform = '';
                        player.style.transform = '';
                        
                        // Reset button styling
                        answerButtons.forEach(btn => btn.classList.remove('correct', 'incorrect'));
                        
                        // Check loss condition
                        if (playerHealthValue <= 0) {
                            setTimeout(() => {
                                alert('Game Over! You have been defeated!');
                                resetGame();
                            }, 500);
                        }
                    }, 1000);
                }, 200);
            }
        });
    });
    
    // Reset game
    function resetGame() {
        playerHealthValue = 76;
        monsterHealthValue = 45;
        playerHealth.style.width = playerHealthValue + '%';
        monsterHealth.style.width = monsterHealthValue + '%';
        document.querySelector('.player-stats .health-text').textContent = playerHealthValue;
        document.querySelector('.monster-stats .health-text').textContent = monsterHealthValue;
        currentQuestion = 0;
        loadQuestion(currentQuestion);
        answerButtons.forEach(btn => btn.classList.remove('correct', 'incorrect'));
    }
    
    // Initialize the game
    loadQuestion(currentQuestion);
});