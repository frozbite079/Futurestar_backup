let gameArea = document.getElementById('game-area');
let scoreDisplay = document.getElementById('score');
let timerDisplay = document.createElement('h2');
let healthDisplay = document.createElement('h2');
let score = 0;
let birdsShot = 0;
let totalBirds;
let levelTime;
let healthPoints;
let currentLevel = 1; 
let birdSpeed; 
let birdInterval; 
let timerInterval; 

timerDisplay.id = 'timer';
timerDisplay.textContent = 'Time: ' + levelTime + 's';
document.body.insertBefore(timerDisplay, gameArea);

healthDisplay.id = 'health';
healthDisplay.textContent = 'Health: ' + healthPoints;
document.body.insertBefore(healthDisplay, gameArea.nextSibling);

function getBirdType() {
    if (currentLevel === 3 || currentLevel === 5) {
        return Math.random() < 0.2 ? 'silver' : 'normal'; // 20% chance for Silver Birds in levels 3 and 5
    } else if (currentLevel === 4 || currentLevel === 6) {
        return Math.random() < 0.2 ? 'golden' : 'normal'; // 20% chance for Golden Birds in levels 4 and 6
    } else {
        return 'normal'; 
    }
}

function createBird() {
    if (birdsShot >= totalBirds || healthPoints <= 0) return; 

    let bird = document.createElement('div');
    let birdType = getBirdType();
    
    bird.className = 'bird ' + birdType;
    gameArea.appendChild(bird);

    let fromLeft = Math.random() < 0.5;

    let gameAreaHeight = gameArea.clientHeight;
    let randomY = Math.floor(Math.random() * (gameAreaHeight - 50));

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
                break;
            case 'golden':
                birdValue = 5;
                break;
            default:
                birdValue = 1;
        }
        score += birdValue;
        birdsShot++;
        scoreDisplay.textContent = 'Score: ' + score;
        bird.remove();

        if (birdsShot >= totalBirds) {
            if (currentLevel === 7) {
                alert('Congratulations! You completed Level 7!');
                clearInterval(birdInterval);
                clearInterval(timerInterval);
            } else {
                alert(`Congratulations! You completed Level ${currentLevel}!`);
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
        alert('You ran out of health! Game Over.');
        clearInterval(birdInterval);
        clearInterval(timerInterval);
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
            alert('Time\'s up! Game Over.');
            clearInterval(birdInterval);
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

    scoreDisplay.textContent = 'Score: ' + score;
    healthDisplay.textContent = 'Health: ' + healthPoints;

    birdInterval = setInterval(createBird, 2500 - (level * 50)); // Decrease interval to increase difficulty
    startTimer();
}

function startNextLevel() {
    let nextLevel = currentLevel + 1;
    if (nextLevel <= 10) {
        startLevel(nextLevel);
    } else {
        alert('Congratulations! You completed all levels!');
    }
}

startLevel(1);

