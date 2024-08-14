let request = false;

async function loginWithMetaMask() {
    
    if (request) {
        console.log('Already processing login request. Please wait.');
        return;
    }
    
    request = true;

    try {
        if (typeof window.ethereum !== 'undefined') {
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0];

            const message = 'Sign this message to login';
            const signature = await ethereum.request({
                method: 'personal_sign',
                params: [message, account],
            });

            const response = await fetch('/api/MetaMaskUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}',  // Ensure CSRF token is included if using Django
                },
                body: JSON.stringify({ address: account, signature: signature, message: message }),
            });

            const data = await response.json();
            if (data.status === 'success') {
                console.log('User logged in:', data.username);
                document.getElementById('metaMaskAddress').textContent = account;
                document.getElementById('authPopup').classList.add('show');
            } else if (data.status === "user_exist") {
                const url = data.redirect_url;
                const user_nickname = data.username;
                const user_id = data.user_id;

                sessionStorage.setItem('user_id', user_id);
                window.location.href = url + "/" + user_nickname;
            } else {
                console.error('Login failed:', data.message);
            }
        } else {
            document.getElementById('metaMaskAlertPopup').style.display = 'block';
        }
    } catch (error) {
        console.error('Error during MetaMask login:', error);
    } finally {
        request = false;
    }
}

function closeMetaMaskAlert() {
    document.getElementById('metaMaskAlertPopup').style.display = 'none';
    window.open('https://metamask.io/download.html', '_blank');
}

document.getElementById('nicknameForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const nickname = document.getElementById('nickname').value;
    const address = document.getElementById('metaMaskAddress').textContent;

    fetch('/api/saveUserdata', {  // Update the URL to your endpoint for saving the nickname
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',  // Ensure CSRF token is included if using Django
        },
        body: JSON.stringify({ nickname, address }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Nickname saved successfully!');
            document.getElementById('authPopup').classList.remove('show');
        } else if (data.status === "Exist") {
            const error_nickname = document.getElementById('nickname-error-tag');
            error_nickname.innerHTML = "Username already exists!";
            error_nickname.style.display = "block";
        } else {
            alert('Error saving nickname.');
        }
    })
    .catch(error => console.error('Error during nickname saving:', error));
});
