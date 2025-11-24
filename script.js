// Update time
function updateTime() {
    const timeElement = document.getElementById('currentTime');
    if (timeElement) {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        timeElement.textContent = `${hours}:${minutes}:${seconds}`;
    }
}

// Sidebar toggle
document.addEventListener('DOMContentLoaded', function() {
    // Update time every second
    updateTime();
    setInterval(updateTime, 1000);
    
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Tab switching
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });

    // Draw rating chart
    drawRatingChart();
});

// Close notification popup
function closeNotification() {
    const popup = document.getElementById('notificationPopup');
    if (popup) {
        popup.classList.add('hidden');
    }
}

// Draw rating chart
function drawRatingChart() {
    const canvas = document.getElementById('ratingChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    
    // Months
    const months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
                    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    
    // Sample data
    const y1Data = [8, 10, 12, 14, 16, 18, 20, 22, 19, 17, 15, 13];
    const y2Data = [5, 6, 8, 10, 12, 14, 15, 16, 14, 12, 10, 8];
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Draw background
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, width, height);
    
    // Draw grid lines
    ctx.strokeStyle = '#E0E0E0';
    ctx.lineWidth = 1;
    
    // Horizontal grid lines
    for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
        
        // Y-axis labels
        ctx.fillStyle = '#666';
        ctx.font = '12px Arial';
        ctx.textAlign = 'right';
        ctx.fillText((25 - i * 5).toString(), padding - 10, y + 4);
    }
    
    // Vertical grid lines
    for (let i = 0; i <= 12; i++) {
        const x = padding + (chartWidth / 12) * i;
        ctx.beginPath();
        ctx.moveTo(x, padding);
        ctx.lineTo(x, height - padding);
        ctx.stroke();
        
        // X-axis labels (every month)
        if (i < months.length) {
            ctx.fillStyle = '#666';
            ctx.font = '10px Arial';
            ctx.textAlign = 'center';
            ctx.save();
            ctx.translate(x, height - padding + 20);
            ctx.rotate(-Math.PI / 4);
            ctx.fillText(months[i], 0, 0);
            ctx.restore();
        }
    }
    
    // Draw axes
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    
    // X-axis
    ctx.beginPath();
    ctx.moveTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();
    
    // Y-axis
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.stroke();
    
    // Y-axis label
    ctx.fillStyle = '#333';
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.save();
    ctx.translate(15, height / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Значение', 0, 0);
    ctx.restore();
    
    // Draw Y1 line (blue)
    ctx.strokeStyle = '#2196F3';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    for (let i = 0; i < y1Data.length; i++) {
        const x = padding + (chartWidth / 12) * i;
        const y = height - padding - (y1Data[i] / 25) * chartHeight;
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    ctx.stroke();
    
    // Draw Y1 points
    ctx.fillStyle = '#2196F3';
    for (let i = 0; i < y1Data.length; i++) {
        const x = padding + (chartWidth / 12) * i;
        const y = height - padding - (y1Data[i] / 25) * chartHeight;
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Draw Y2 line (green)
    ctx.strokeStyle = '#4CAF50';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    for (let i = 0; i < y2Data.length; i++) {
        const x = padding + (chartWidth / 12) * i;
        const y = height - padding - (y2Data[i] / 25) * chartHeight;
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    ctx.stroke();
    
    // Draw Y2 points
    ctx.fillStyle = '#4CAF50';
    for (let i = 0; i < y2Data.length; i++) {
        const x = padding + (chartWidth / 12) * i;
        const y = height - padding - (y2Data[i] / 25) * chartHeight;
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Draw legend
    const legendY = padding + 20;
    
    // Y1 legend (blue)
    ctx.fillStyle = '#2196F3';
    ctx.fillRect(width - padding - 120, legendY, 15, 3);
    ctx.fillStyle = '#333';
    ctx.font = '12px Arial';
    ctx.textAlign = 'left';
    ctx.fillText('Значение Y1', width - padding - 100, legendY + 10);
    
    // Y2 legend (green)
    ctx.fillStyle = '#4CAF50';
    ctx.fillRect(width - padding - 120, legendY + 20, 15, 3);
    ctx.fillStyle = '#333';
    ctx.fillText('Значение Y2', width - padding - 100, legendY + 30);
    
    // Make canvas responsive
    if (canvas.parentElement) {
        const containerWidth = canvas.parentElement.offsetWidth;
        if (containerWidth < width) {
            canvas.style.width = '100%';
            canvas.style.height = 'auto';
        }
    }
}



const ok_btn_id = document.getElementById("ok-submit-btn");
const not_btn_id = document.getElementById("not-submit-btn");
const form_cont = document.querySelector(".message-form"); // изменил на querySelector
const pred_date = document.getElementById("pred_date"); // добавил получение элемента

pred_date.disabled = true;

ok_btn_id.addEventListener("click", function(event){ // добавил параметр event
    event.preventDefault();
    const work_value = document.getElementById("answer");
    const formData = new FormData();
    formData.append('id', '2');
    formData.append("answer", document.getElementById("answer"));
    fetch('http://localhost:8000/answerexecutor', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Успех:', data);
        alert('Данные отправлены!');
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка');
    });

    console.log("SUCCESS"); // исправил опечатку
});

// Добавьте обработчик для кнопки "Отложить решение"
const notSubmitBtn = document.getElementById("not-submit-btn");
notSubmitBtn.addEventListener("click", function(event) {
    event.preventDefault();
    
    const formData = new FormData(form_cont);
    formData.append('status', 'delayed');
    formData.append('id', '2');
    
    fetch('http://localhost:8000/answerexecutor', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Заявка отложена:', data);
        alert('Заявка отложена! Рейтинг снижен на 10 пунктов.');
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка');
    });
});

const new_ipol = document.getElementById("new_ipol");
new_ipol.addEventListener("click", function(event) {
    event.preventDefault();
    new_ipol.textContent = "В работе";
});



// document.addEventListener('DOMContentLoaded', function() {
//     // Код здесь выполнится когда DOM полностью загружен
//     const formData = new FormData();
//     formData.append('id', '2');
//     formData.append("answer", document.getElementById("answer"));
//     fetch('http://localhost:8000/answerexecutor', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Успех:', data);
//         alert('Данные отправлены!');
//     })
//     .catch(error => {
//         console.error('Ошибка:', error);
//         alert('Произошла ошибка');
//     });

//     const rank = document.getElementById("rating-value");
//     rank.textContent = "88%";
//     r
    
// });
