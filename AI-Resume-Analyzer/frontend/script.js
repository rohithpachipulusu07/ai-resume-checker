const form = document.getElementById('resume-form');
const result = document.getElementById('result');
const scoreEl = document.getElementById('score');
const summaryEl = document.getElementById('summary');
const overallMatchEl = document.getElementById('overall-match');
const keywordMatchEl = document.getElementById('keyword-match');
const semanticMatchEl = document.getElementById('semantic-match');
const skillMatchEl = document.getElementById('skill-match');
const atsSuggestionsEl = document.getElementById('ats-suggestions');
const interviewQuestionsEl = document.getElementById('interview-questions');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    try {
        const response = await fetch('http://127.0.0.1:8000/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || data.error || 'Something went wrong');
        }

        result.classList.remove('hidden');
        scoreEl.textContent = Math.round(data.overall_match || 0);
        overallMatchEl.textContent = `${Math.round(data.overall_match || 0)}%`;
        keywordMatchEl.textContent = `${Math.round(data.keyword_match || 0)}%`;
        semanticMatchEl.textContent = `${Math.round(data.semantic_match || 0)}%`;
        skillMatchEl.textContent = `${Math.round(data.skill_match || 0)}%`;
        summaryEl.textContent = `Overall Match ${Math.round(data.overall_match || 0)}% | Keyword Match ${Math.round(data.keyword_match || 0)}% | Semantic Match ${Math.round(data.semantic_match || 0)}% | Skill Match ${Math.round(data.skill_match || 0)}%`;

        atsSuggestionsEl.innerHTML = '';
        (data.ats_suggestions || []).forEach((suggestion) => {
            const item = document.createElement('li');
            item.textContent = suggestion;
            atsSuggestionsEl.appendChild(item);
        });

        interviewQuestionsEl.innerHTML = '';
        (data.interview_questions || []).forEach((question) => {
            const item = document.createElement('li');
            item.textContent = question;
            interviewQuestionsEl.appendChild(item);
        });
    } catch (error) {
        alert(error.message);
    }
});
