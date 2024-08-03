async function loginWithMetaMask() {
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
        } else {
            console.error('Login failed:', data.message);
        }
    } else {
        console.error('MetaMask is not installed');
    }
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
        } else {
            alert('Error saving nickname.');
        }
    });
});