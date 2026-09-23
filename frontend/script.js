const resumeInput = document.getElementById('resume-input')
const jobInput = document.getElementById('job-input')
const instructionsInput = document.getElementById('instructions-input')

const reviewButton = document.getElementById('review-button')
const resultBox = document.getElementById('result-box')

async function reviewResume() {
  const resume = resumeInput.value
  const jobDescription = jobInput.value
  const userInstructions = instructionsInput.value

  // Check if resume is empty

  if (resume.trim() === '') {
    alert('Please paste your resume first.')

    return
  }

  // Disable button while AI is working

  reviewButton.disabled = true

  // Show loading message

  resultBox.innerHTML = `
        <div class="loading">
            Analyzing your resume...
        </div>
    `

  try {
    const response = await fetch('http://127.0.0.1:8000/review', {
      method: 'POST',

      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify({
        resume: resume,

        job_description: jobDescription,

        user_instructions: userInstructions,
      }),
    })

    // Check for server errors

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`)
    }

    // Convert response to JSON

    const data = await response.json()
    console.log(data.response)
    // Display AI response

    resultBox.innerHTML = `
            <div class="ai-message">
                ${marked.parse(data.response)}
            </div>
        `
  } catch (error) {
    console.log('Error:', error)

    resultBox.innerHTML = `
            <div class="error">
                Something went wrong.
                Please check that the backend is running.
            </div>
        `
  } finally {
    // Enable button again

    reviewButton.disabled = false
  }
}

// When user clicks Review Resume

reviewButton.addEventListener('click', reviewResume)
