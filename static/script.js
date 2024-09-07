document.getElementById('download-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('url-input').value;
    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `url=${encodeURIComponent(url)}`
        });
        const result = await response.json();
        if (result.status === 'success') {
            displayMessages();
        } else {
            console.error('Error details:', result);
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert(`An error occurred: ${error.message}`);
    }
});

document.getElementById('search-button').addEventListener('click', () => {
    const query = document.getElementById('search-input').value;
    displayMessages(query);
});

function replaceEmojiPlaceholders(message) {
    return message.replace(/<emoji-img src='([^']+)' alt='([^']+)'>/g, (match, src, alt) => {
        return `<img src="${src}" alt="${alt}" class="inline-block align-text-bottom" style="width: 24px; height: 24px;" onerror="this.onerror=null; this.alt='${alt}'; this.style.display='inline';">`;
    });
}

async function displayMessages(query = '') {
    const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
    const messages = await response.json();
    const chatContainer = document.getElementById('chat-container');
    chatContainer.innerHTML = '';
    messages.forEach(msg => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', 'mb-4', 'p-3', 'bg-gray-700', 'rounded-lg', 'border', 'border-gray-600');
        messageDiv.innerHTML = `
            <div class="flex items-baseline mb-1">
                <span class="text-neon-blue mr-2">${formatTimestamp(msg.timestamp)}</span>
                <span class="font-bold text-neon-green mr-2">${msg.username}:</span>
                <p class="text-gray-200 break-words">${replaceEmojiPlaceholders(msg.message)}</p>
            </div>
        `;
        chatContainer.appendChild(messageDiv);
    });
}

function formatTimestamp(timestamp) {
    const totalSeconds = Math.floor(parseInt(timestamp) / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}