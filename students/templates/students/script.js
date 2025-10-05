let quizTimer=null;
let timeLeft=0;
let timerRunning=false;

function toggleTopic(el){
  const parent = el.closest('.topic');
  const sub = parent.querySelector('.sublist');
  const chev = el.querySelector('.chev');
  const isOpen = sub.classList.contains('show');
  if(isOpen){ sub.classList.remove('show'); chev.classList.remove('open'); }
  else{ sub.classList.add('show'); chev.classList.add('open'); }
}

function selectAll(topicKey, all=true){
  const list = document.getElementById(topicKey + '-list');
  if(!list) return;
  list.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = all);
  updateSelectedInfo();
}

function getSelectedSubtopics(){
  const checked = Array.from(document.querySelectorAll('.sidebar input[type="checkbox"]:checked'));
  return checked.map(cb => cb.value);
}

function updateSelectedInfo(){
  const sel = getSelectedSubtopics();
  document.getElementById('selList').textContent = sel.length ? sel.join(', ') : 'none';
}

document.querySelectorAll('.sidebar input[type="checkbox"]').forEach(cb => {
  cb.addEventListener('change', updateSelectedInfo);
});

function onLevelChange(){
  const level = document.getElementById('level').value;
  document.querySelectorAll('#geometric-optics-list .subitem').forEach(item => {
    const levelsAttr = item.getAttribute('data-level') || '';
    const allowed = levelsAttr.split(/\s+/).filter(Boolean);
    if(allowed.includes(level)){
      item.style.display = 'flex';
    } else {
      item.style.display = 'none';
      const cb = item.querySelector('input[type="checkbox"]');
      if(cb) cb.checked = false;
    }
  });
  updateSelectedInfo();
}

function generateQuiz(){
  const selected = getSelectedSubtopics();
  if(selected.length === 0){
    alert('Select at least one subtopic before generating.');
    return;
  }
  simulate(); // generate questions
  const startBtn = document.getElementById('startQuizBtn');
  startBtn.style.display = document.getElementById('enableTimer').checked ? 'inline-block' : 'none';
}

function startQuiz(){
  if(timerRunning) return;
  const numQ = parseInt(document.getElementById('num_q').value || 5);
  timeLeft = numQ * 60; // 1 min per question
  const timerDisplay = document.getElementById('timer-display');
  timerRunning = true;

  // disable all Show Answer buttons
  document.querySelectorAll('.qcard button').forEach(b=>b.disabled=true);

  quizTimer = setInterval(()=>{
    let minutes = Math.floor(timeLeft/60);
    let seconds = timeLeft%60;
    timerDisplay.textContent = `${minutes}:${seconds.toString().padStart(2,'0')}`;
    timeLeft--;
    if(timeLeft<0){
      clearInterval(quizTimer);
      timerRunning=false;
      timerDisplay.textContent="Time's up!";
      alert("Time's up!");
      // re-enable Show Answer buttons
      document.querySelectorAll('.qcard button').forEach(b=>b.disabled=false);
    }
  },1000);
}

// SIMULATION LOGIC (Non-Objective as before)
function renderQuiz(questions){
  const area = document.getElementById('quiz-area');
  if(!questions || questions.length === 0){
    area.innerHTML = '<div class="muted">No questions available.</div>';
    MathJax.typesetPromise && MathJax.typesetPromise();
    return;
  }
  area.innerHTML = '';
  questions.forEach((q, i) => {
    const card = document.createElement('div');
    card.className = 'qcard';
    const title = document.createElement('div');
    title.className = 'q-title';
    title.textContent = 'Question ' + (i+1);
    const body = document.createElement('div');
    body.className = 'q-body';
    body.innerHTML = q.question;
    card.appendChild(title);
    card.appendChild(body);
    const ansToggle = document.createElement('button');
    ansToggle.className = 'secondary';
    ansToggle.style.marginTop = '6px';
    ansToggle.textContent = 'Show Answer';
    const ansDiv = document.createElement('div');
    ansDiv.className = 'muted';
    ansDiv.style.display = 'none';
    ansDiv.style.marginTop = '8px';
    ansDiv.innerHTML = q.answer || 'No answer provided';
    ansToggle.onclick = () => {
      if(ansDiv.style.display==='none'){ ansDiv.style.display='block'; ansToggle.textContent='Hide Answer'; }
      else{ ansDiv.style.display='none'; ansToggle.textContent='Show Answer'; }
    };
    card.appendChild(ansToggle);
    card.appendChild(ansDiv);
    area.appendChild(card);
  });
  if(window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();
}

function simulate(){
  const subs = getSelectedSubtopics();
  const sample = [];
  const n = Math.min(12, Math.max(1, parseInt(document.getElementById('num_q').value || 5)));
  const diff = document.getElementById('difficulty').value;
  const chosen = subs.length ? subs : ['reflection'];

  for(let i=0;i<n;i++){
    const s = chosen[i % chosen.length];
    let qtex, ans;
    switch(s){
      case 'reflection':
        qtex = `A light ray strikes a plane mirror at an angle of incidence $\\theta_i=30^\\circ$. What is the angle of reflection?`;
        ans = 'Angle of reflection equals angle of incidence → 30°';
        break;
      case 'refraction':
        qtex = `A ray of light passes from air into glass with index $n=1.5$ at incidence $\\theta_i=45^\\circ$. Use Snell\\'s law to find $\\theta_t$.`;
        ans = 'Use $n_1\\sin\\theta_1=n_2\\sin\\theta_2$. Solve: θ₂ ≈ 28°';
        break;
      case 'snell':
        qtex = `Derive Snell\\'s law using Fermat\\'s principle of least time.`;
        ans = 'Show that path of least time requires $n_1\\sin\\theta_1 = n_2\\sin\\theta_2$.';
        break;
      case 'aberration':
        qtex = `Describe spherical aberration in a convex lens. How can it be reduced?`;
        ans = 'Different rays focus at different points. Reduced by using aspheric lenses or stopping down aperture.';
        break;
      case 'lenses':
        qtex = `A converging lens has focal length $f=10\\,cm$. An object is placed $u=15\\,cm$ away. Find the image distance $v$.`;
        ans = 'Lens formula: $1/f=1/v+1/u$. Solve: $v=30$ cm.';
        break;
      case 'mirrors':
        qtex = `A concave mirror forms a real image twice the size of the object. If the object distance is 30 cm, find the focal length.`;
        ans = 'Magnification = -v/u = -2. Solve: v=60 cm. Mirror formula → f=20 cm.';
        break;
      case 'tir':
        qtex = `Critical angle at a glass–air interface when $n=1.5$.`;
        ans = '$\\theta_c = \\arcsin(1/1.5) ≈ 41.8°$.';
        break;
      default:
        qtex = 'Sample LaTeX question placeholder';
        ans = 'Sample answer placeholder';
    }
    sample.push({question:qtex, answer:ans});
  }
  renderQuiz(sample);
}

async function downloadPDF(){
  const area = document.getElementById('quiz-area');
  if(!area || !area.firstChild){ alert('No quiz to download.'); return; }
  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF({unit:'pt', format:'a4'});
  const canvas = await html2canvas(area);
  const imgData = canvas.toDataURL('image/png');
  const pageWidth = pdf.internal.pageSize.getWidth();
  const ratio = pageWidth / canvas.width;
  const pageHeight = canvas.height * ratio;
  pdf.addImage(imgData, 'PNG', 20, 20, pageWidth-40, pageHeight-40);
  pdf.save('quiz.pdf');
}

onLevelChange();
