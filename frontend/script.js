const userInput = document.getElementById('user-input')
const sendButton = document.getElementById('send-button')
const chatBox = document.getElementById('chat-box')
const clearButton = document.getElementById('clear-button')
async function sendMessage() {
  const message = userInput.value

  if (message.trim() === '') {
    return
  }
  sendButton.disabled = true
  chatBox.innerHTML += `
    <div class="user-message">
        ${message}
    </div>
`
  chatBox.scrollTop = chatBox.scrollHeight
  chatBox.innerHTML += `<p id="loading"><strong>AI:</strong> Thinking...</p>`

  try {
    const response = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: message }),
    })
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`)
    }

    console.log('Response received:', response)

    const data = await response.json()

    console.log('AI response:', data)
    chatBox.innerHTML += `
    <div class="ai-message">
        ${marked.parse(data.response)}
    </div>
`
    chatBox.innerHTML += marked.parse(data.response)
    chatBox.scrollTop = chatBox.scrollHeight
  } catch (error) {
    console.log('Error:', error)
    chatBox.innerHTML += `<p><strong>AI:</strong> Sorry, something went wrong.</p>`
  } finally {
    document.getElementById('loading').remove()
    sendButton.disabled = false
  }
  userInput.value = ''
}

async function clearChat() {
  const response = await fetch('http://127.0.0.1:8000/clear', {
    method: 'POST',
  })

  if (!response.ok) {
    console.log('Failed to clear chat')
    return
  }

  chatBox.innerHTML = ''
}

sendButton.addEventListener('click', sendMessage)
userInput.addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    sendMessage()
  }
})
clearButton.addEventListener('click', clearChat)
