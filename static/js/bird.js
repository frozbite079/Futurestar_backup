document.addEventListener('DOMContentLoaded', function() {
    let gameArea = document.getElementById('game-area');
    let startGameButton = document.getElementById('start-game-button');
    let user_id = document.getElementById('user-id-for-gem-update')
    let timerDisplay = document.createElement('h2');
    let healthDisplay = document.createElement('h2'); 
    let scoreDisplay = document.createElement('h2');
    scoreDisplay.id = 'score';
    let gem_update = document.getElementById('gem-update')
    let coin_update = document.getElementById('coin-update')


    let user_id_is = user_id.innerText
    console.log(user_id_is)
    scoreDisplay.textContent = 'Score: 0'; // Initial score

    timerDisplay.id = 'timer';
    timerDisplay.textContent = 'Time: 0s'; // Default text
    
    healthDisplay.id = 'health';
    healthDisplay.textContent = 'Health: 0'; // Default text

    function setupGame() {
        gameArea.appendChild(scoreDisplay); // Append to the game area
        gameArea.appendChild(timerDisplay); // Append to game area
        gameArea.appendChild(healthDisplay); // Append to game area

        let score = 0;
        let gems = 0;
        let birdsShot = 0;
        let totalBirds;
        let levelTime;
        let healthPoints;
        let currentLevel = 1; 
        let birdSpeed; 
        let birdInterval; 
        let timerInterval; 

        function getBirdType() {
            if (currentLevel === 3 || currentLevel === 5) {
                return Math.random() < 0.2 ? 'silver' : 'normal';
            } else if (currentLevel === 4 || currentLevel === 6) {
                return Math.random() < 0.2 ? 'golden' : 'normal';
            } else {
                return 'normal'; 
            }
        }

        function showNotification(message) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.classList.add('show-notification');
        
            setTimeout(() => {
                notification.classList.remove('show-notification');
            }, 3000);
        }

        function earnGems() {
            gemInterval = setInterval(() => {
                gems++;
                //window.location.href = ""
                sendGemstoServer(gems)
                //sendGemstoServer(gems)
                //gemDisplay.textContent = 'Gems: ' + gems;
                
            }, 60000); 
            
        }

        function sendGemstoServer(gems){
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            console.log(csrfToken)
            fetch('/api/gemUpdate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                
                body: JSON.stringify({ gems: gems,user_id:user_id_is})
            })
            .then(response => response.json())
            .then(data => {
                console.log('Gems successfully sent to server:', data);
                showNotification(`Congratulation you get a Gem 💎`);
                gem_update.innerText = data.message

            })
            .catch(error => {
                console.error('Error sending gems:', error);
            });

        }


        function createBird() {
            if (birdsShot >= totalBirds || healthPoints <= 0) return; 
        
            let bird = document.createElement('div');
            let birdType = getBirdType();
            
            bird.className = 'bird ' + birdType;
            gameArea.appendChild(bird);
        
            let fromLeft = Math.random() < 0.5;
        
            let gameAreaHeight = gameArea.clientHeight;
            let minY = timerDisplay.offsetHeight + 20; 
            let maxY = gameAreaHeight - 200; 
        
            let randomY = Math.floor(Math.random() * (maxY - minY)) + minY;
        
            bird.style.top = randomY + 'px';
            if (fromLeft) {
                bird.style.left = '0';
                bird.style.transition = `left ${birdSpeed}s linear`; 
                bird.style.left = gameArea.clientWidth + 'px';
            } else {
                bird.style.right = '0';
                bird.classList.add('flip'); 
                bird.style.transition = `right ${birdSpeed}s linear`; 
                bird.style.right = gameArea.clientWidth + 'px';
            }
        
            bird.addEventListener('transitionend', () => {
                bird.remove();
                decreaseHealth();
            });
        
            bird.addEventListener('click', function () {
                let birdValue;
                switch (birdType) {
                    case 'silver':
                        birdValue = 2;
                        coinadd(birdValue)
                        break;
                    case 'golden':
                        birdValue = 5;
                        coinadd(birdValue)
                        break;
                    default:
                        birdValue = 1;
                        coinadd(birdValue)
                }

                function coinadd(birdvalue){

                    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
                    console.log(csrfToken)
                    fetch('/api/coinupdate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        
                        body: JSON.stringify({ coin: birdvalue,user_id:user_id_is})
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('coin successfully sent to server:', data);
                        //showNotification(`Congratulation you get a Gem 💎`);
                        coin_update.innerText = data.message

                    })
                    .catch(error => {
                        console.error('Error sending gems:', error);
                    });

                }
                    
                
                score += birdValue;
                birdsShot++;
                scoreDisplay.textContent = 'Score: ' + score;
                bird.remove();
        
                if (birdsShot >= totalBirds) {
                    if (currentLevel === 7) {
                        showNotification('Congratulations! You completed Level 7!');
                        clearInterval(birdInterval);
                        clearInterval(timerInterval);
                    } else {
                        showNotification(`Congratulations! You completed Level ${currentLevel}!`);
                        clearInterval(birdInterval);
                        clearInterval(timerInterval);
                        startNextLevel(); 
                    }
                }
            });
        }

        function decreaseHealth() {
            healthPoints--;
            healthDisplay.textContent = 'Health: ' + healthPoints;
            if (healthPoints <= 0) {
                showNotification('You ran out of health! Game Over.');
                clearInterval(birdInterval);
                clearInterval(timerInterval);
                showStartButton();
            }
        }


        function startTimer() {
            let timeLeft = levelTime;
            timerDisplay.textContent = 'Time: ' + timeLeft + 's';

            timerInterval = setInterval(() => {
                timeLeft--;
                timerDisplay.textContent = 'Time: ' + timeLeft + 's';

                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    showNotification('Time\'s up! Game Over.');
                    clearInterval(birdInterval);
                    showStartButton();
                }
            }, 1000);
        }

        function startLevel(level) {
            currentLevel = level;
            birdsShot = 0;
            
            switch (level) {
                case 1:
                    totalBirds = 7;
                    levelTime = 30;
                    healthPoints = 5;
                    birdSpeed = 8; 
                    break;
                case 2:
                    totalBirds = 12;
                    levelTime = 30;
                    healthPoints = 7;
                    birdSpeed = 6; 
                    break;
                case 3:
                    totalBirds = 17;
                    levelTime = 30;
                    healthPoints = 9;
                    birdSpeed = 5.5; 
                    break;
                case 4:
                    totalBirds = 22;
                    levelTime = 30;
                    healthPoints = 11;
                    birdSpeed = 5; 
                    break;
                case 5:
                    totalBirds = 27;
                    levelTime = 40;
                    healthPoints = 13;
                    birdSpeed = 4.5; 
                    break;
                case 6:
                    totalBirds = 32;
                    levelTime = 40;
                    healthPoints = 15;
                    birdSpeed = 4; 
                    break;
                case 7:
                    totalBirds = 37;
                    levelTime = 40;
                    healthPoints = 17;
                    birdSpeed = 3.5; 
                    break;
                case 8:
                    totalBirds = 42;
                    levelTime = 40;
                    healthPoints = 19;
                    birdSpeed = 3; 
                    break;
                case 9:
                    totalBirds = 50;
                    levelTime = 40;
                    healthPoints = 21;
                    birdSpeed = 2.5; 
                    break;
                case 10:
                    totalBirds = 52;
                    levelTime = 40;
                    healthPoints = 21;
                    birdSpeed = 2; 
                    break;
            }

            healthDisplay.textContent = 'Health: ' + healthPoints;

            birdInterval = setInterval(createBird, 2500 - (level * 50));
            earnGems(); 
            startTimer();
        }

        function startNextLevel() {
            let nextLevel = currentLevel + 1;
            if (nextLevel <= 10) {
                showNotification(`Congratulations! Starting Level ${nextLevel}!`);
                startLevel(nextLevel);
            } else {
                showNotification('Congratulations! You completed all levels!');
                showStartButton();
            }
        }

        function showStartButton() {
            startGameButton.style.display = 'block'; // Show the start button
        }

        function startGame() {
            startGameButton.style.display = 'none'; // Hide the start button
            startGameButton.style.zIndex = '0'
            setupGame(); // Set up the game
            startLevel(1); // Start the first level
        }

        startGameButton.addEventListener('click', startGame);
        showStartButton(); // Ensure the button is shown initially
    }

    setupGame();
});
