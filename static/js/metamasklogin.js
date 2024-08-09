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
        }
        
        else if(data.status ==="user_exist"){

            
            var url = data.redirect_url
            
            var user_nickname = data.username

            var user_id = data.user_id
            
            //return handleMetaMaskResponse(url)
            sessionStorage.setItem('user_id', user_id);

            window.location.href =  url+"/"+user_nickname;
 

        }
        else {
            console.error('Login failed:', data.message);
        }
    } else {
        document.getElementById('metaMaskAlertPopup').style.display = 'block';
        

    }
}

function closeMetaMaskAlert() {
    document.getElementById('metaMaskAlertPopup').style.display = 'none';
    window.open('https://metamask.io/download.html', '_blank');

}


function handleMetaMaskResponse(url) {
    
    console.log("hello")
    
    
    
   
    
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
        console.log("hello")
        if (data.status === 'success') {
            alert('Nickname saved successfully!');
            document.getElementById('authPopup').classList.remove('show');
        } 
        else if(data.status === "Exist"){

            var error_nickname =    document.getElementById('nickname-error-tag').innerHTML = "Username is already exist!"
            error_nickname.style.display = "block"

        }
        else {
            alert('Error saving nickname.');
        }
    });
});

