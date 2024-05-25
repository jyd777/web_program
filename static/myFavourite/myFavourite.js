
let c = 0;
function toggle() {
    c % 2 == 0 ? day() : night();
    c++;
}

function night() {
    document.querySelector(".cont_circle").className =
        "cont_circle cont_circle_noche";
    document.body.style.backgroundColor = "#f2edff";
    document.querySelector(".cont_text").className = "cont_text  cont_text_noche";
    document.querySelectorAll(".cont_text > p")[0].innerHTML = "NIGHT";
}

function day() {
    document.querySelector(".cont_circle").className =
        "cont_circle cont_circle_dia";
    document.body.style.backgroundColor = "#f7f7f7";
    document.querySelector(".cont_text").className = "cont_text  cont_text_dia";
    document.querySelectorAll(".cont_text > p")[0].innerHTML = " ";
}

function loadTableData() {
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = ''; // 清空现有内容

    fetch('/getUserStarredArticles')
    .then(response => response.json())
    .then(data => {
        data.forEach((item) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.title}</td>
                <td>${item.category}</td>
                <td>
                <a href="http://127.0.0.1:5000/articlesDetail.html?id=${item.article_id}" class="button">
                <span>Review</span>  →
            </a>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error loading user starred articles:', error);
    });
}
// 加载数据
loadTableData();


//  搜索栏
document.getElementById('search-input').addEventListener('input', function () {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('#table-body tr');

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const match = Array.from(cells).some(cell => cell.textContent.toLowerCase().includes(filter));
        if (match) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});


//  汉字云
function randomText() {
    const text = 'WORD TONGJI';
    const letter = text[Math.floor(Math.random() * text.length)];
    return letter;
}
function rain() {
    const cloud = document.querySelector('.cloud');
    const e = document.createElement('div');
    const left = Math.floor(Math.random() * 110);
    const size = Math.random() * 1.5;
    const duration = Math.random() * 1;
    const text = randomText();
    e.classList.add('text');
    e.innerText = text;
    e.style.left = 25 + left + 'px';
    e.style.fontSize = size + 'em';
    e.style.animationDuration = 2 + duration + 's';
    cloud.appendChild(e);
    setTimeout(() => {
        cloud.removeChild(e);
    }, 2000);
}
setInterval(rain, 40);
