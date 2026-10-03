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
      const errorData = await response.json()

      console.log('Backend error:', errorData)

      throw new Error(`Server error: ${response.status}`)
    }

    // Convert response to JSON

    const data = await response.json()

    console.log(data)

    // Display AI response

    resultBox.innerHTML = `


        <!-- Overall Score -->

        <div class="score-card">

            <h2>Overall Resume Score</h2>

            <div class="score">
                ${data.overall_score}
            </div>

            <p>out of 100</p>

        </div>



        <!-- Score Breakdown -->

        <div class="breakdown-card">

            <h2>Score Breakdown</h2>


            <div class="score-row">

                <span>Projects</span>

                <strong>
                    ${data.score_breakdown.projects}
                </strong>

            </div>


            <div class="score-row">

                <span>Skills</span>

                <strong>
                    ${data.score_breakdown.skills}
                </strong>

            </div>


            <div class="score-row">

                <span>Job Match</span>

                <strong>
                    ${data.score_breakdown.job_match ?? 'N/A'}
                </strong>

            </div>


            <div class="score-row">

                <span>Experience</span>

                <strong>
                    ${data.score_breakdown.experience ?? 'N/A'}
                </strong>

            </div>


            <div class="score-row">

                <span>Achievements</span>

                <strong>
                    ${data.score_breakdown.achievements ?? 'N/A'}
                </strong>

            </div>

        </div>



        <!-- Strengths and Weaknesses -->

        <div class="analysis-grid">


            <!-- Strengths -->

            <div class="analysis-card">

                <h2>Strengths</h2>

                <ul>

                    ${data.strengths
                      .map(
                        (strength) => `
                            <li>${strength}</li>
                        `,
                      )
                      .join('')}

                </ul>

            </div>



            <!-- Weaknesses -->

            <div class="analysis-card">

                <h2>Weaknesses</h2>

                ${data.weaknesses
                  .map(
                    (item) => `

                        <div class="weakness-item">

                            <h3>
                                ${item.weakness}
                            </h3>

                            <p>
                                <strong>Why:</strong>
                                ${item.why}
                            </p>

                            <p>
                                <strong>Improvement:</strong>
                                ${item.improvement}
                            </p>

                        </div>

                    `,
                  )
                  .join('')}

            </div>


        </div>



        <!-- Job Match -->

        ${
          data.job_match
            ? `

            <div class="job-match-card">

                <h2>Job Match</h2>


                <div class="job-score">

                    ${data.job_match.score} / 100

                </div>



                <!-- Demonstrated -->

                <div class="job-match-section">

                    <h3>
                        ✓ Demonstrated
                    </h3>

                    <ul>

                        ${data.job_match.demonstrated
                          .map(
                            (skill) => `
                                <li>${skill}</li>
                            `,
                          )
                          .join('')}

                    </ul>

                </div>



                <!-- Listed but not demonstrated -->

                <div class="job-match-section">

                    <h3>
                        ⚠ Listed but not demonstrated
                    </h3>

                    <ul>

                        ${data.job_match.listed_but_not_demonstrated
                          .map(
                            (skill) => `
                                <li>${skill}</li>
                            `,
                          )
                          .join('')}

                    </ul>

                </div>



                <!-- Missing -->

                <div class="job-match-section">

                    <h3>
                        ✗ Missing
                    </h3>

                    <ul>

                        ${data.job_match.missing
                          .map(
                            (skill) => `
                                <li>${skill}</li>
                            `,
                          )
                          .join('')}

                    </ul>

                </div>


            </div>

        `
            : ''
        }



        <!-- Project Analysis -->

        <div class="project-analysis-card">

            <h2>Project Analysis</h2>


            ${data.project_analysis
              .map(
                (project) => `

                    <div class="project-card">


                        <h3>
                            ${project.project}
                        </h3>



                        <!-- Project Strengths -->

                        <div class="project-section">

                            <h4>
                                Strengths
                            </h4>

                            <ul>

                                ${project.strengths
                                  .map(
                                    (strength) => `
                                        <li>${strength}</li>
                                    `,
                                  )
                                  .join('')}

                            </ul>

                        </div>



                        <!-- Project Weaknesses -->

                        <div class="project-section">

                            <h4>
                                Weaknesses
                            </h4>

                            <ul>

                                ${project.weaknesses
                                  .map(
                                    (weakness) => `
                                        <li>${weakness}</li>
                                    `,
                                  )
                                  .join('')}

                            </ul>

                        </div>



                        <!-- Project Improvements -->

                        <div class="project-section">

                            <h4>
                                Improvements
                            </h4>

                            <ul>

                                ${project.improvements
                                  .map(
                                    (improvement) => `
                                        <li>${improvement}</li>
                                    `,
                                  )
                                  .join('')}

                            </ul>

                        </div>


                    </div>

                `,
              )
              .join('')}
              <!-- Bullet Improvements -->

<div class="bullet-improvements-card">

    <h2>Bullet Improvements</h2>

    ${data.bullet_improvements
      .map(
        (bullet) => `

            <div class="bullet-card">

                <div class="bullet-section">

                    <h4>Original</h4>

                    <p>
                        ${bullet.original}
                    </p>

                </div>


                <div class="bullet-section">

                    <h4>Problem</h4>

                    <p>
                        ${bullet.problem}
                    </p>

                </div>


                <div class="bullet-section">

                    <h4>Improved</h4>

                    <p>
                        ${bullet.improved}
                    </p>

                </div>

            </div>

        `,
      )
      .join('')}

</div>
<!-- Action Items -->

<div class="action-items-card">

    <h2>Action Items</h2>

    <ul>

        ${data.action_items
          .map(
            (item) => `
                    <li>${item}</li>
                `,
          )
          .join('')}

    </ul>

</div>
<!-- ATS Analysis -->

<div class="ats-analysis-card">

    <h2>ATS Analysis</h2>

    <ul>

        ${data.ats_analysis
          .map(
            (item) => `
                    <li>${item}</li>
                `,
          )
          .join('')}

    </ul>

</div>

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
