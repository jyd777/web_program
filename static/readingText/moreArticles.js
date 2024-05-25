document.addEventListener('DOMContentLoaded', () => {
    const booksPerPage = 4; // 每页显示的书籍数量
    let currentPage = 1; // 当前页码
    let totalPages = 1; // 总页码
    let books = [];
    // let books = [
    //     { id: 1, title: 'THIS is TITLETHIS is TITLETHIS is TITLE', cover: '../TextImage/buildBetterLife.png', category: 'Economics' },
    //     { id: 2, title: 'THIS is TITLE', cover: '../TextImage/brand.png', category: 'Economics' },
    //     { id: 3, title: 'THIS is TITLE', cover: '../TextImage/brand.png', category: 'Others' },
    //     { id: 4, title: 'THIS is TITLE', cover: '../TextImage/brand.png', category: 'Others' },
    //     { id: 5, title: 'THIS is TITLE', cover: '../TextImage/brand.png', category: 'Science' },
    //     { id: 6, title: 'THIS is TITLE', cover: '../TextImage/brand.png', category: 'Science' },
    //     { id: 7, title: 'THIS is TITLE', cover: '../TextImage/brand.png', category: 'Others' },
    //     { id: 8, title: 'THIS is TITLE', cover: '../TextImage/brand.png', category: 'Psychology' },
    //     { id: 9, title: 'THIS is TITLE', cover: '../TextImage/AItennis.png', category: 'Psychology' }
    // ];

    // 获取DOM元素
    const gallery = document.getElementById('book-gallery');
    const searchInput = document.getElementById('search-input');
    const categorySelect = document.getElementById('category-select');
    const pagination = document.getElementById('pagination');
    // const loader = document.getElementById('loader');

    // 过滤书籍函数
    function filterBooks() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedCategory = categorySelect.value;
        return books.filter(book => {
            const matchesSearch= book.title.toLowerCase().includes(searchTerm);
            const matchesCategory= selectedCategory === 'all' || book.category === selectedCategory;
            return matchesSearch && matchesCategory;
        });
    }

    // 渲染书籍函数
    function renderBooks() {
        // loader.style.display = 'block'; // 显示加载动画
        gallery.classList.add('fade-out'); // 添加淡出动画效果

        setTimeout(() => {
            gallery.innerHTML = ''; // 清空当前书籍展示区
            // const filteredBooks = filterBooks();
            // const start = (currentPage - 1) * booksPerPage;
            // const end = start + booksPerPage;
            // const paginatedBooks = filteredBooks.slice(start, end);

            books.forEach(book => {
                const bookItem = document.createElement('div');
                bookItem.className = 'book-item';
                bookItem.innerHTML = `
                    <img src="${book.coverUrl}" alt="${book.title}">
                    <div class="book-title">${book.title}</div>
                `;
                bookItem.addEventListener('click', () => {
                    window.location.href = `articlesDetail.html?id=${book.id}`;
                });
                gallery.appendChild(bookItem);
            });

            // loader.style.display = 'none'; // 隐藏加载动画
            gallery.classList.remove('fade-out');
            gallery.classList.add('fade-in'); // 添加淡入动画效果

            renderPagination(); // 渲染分页按钮
            // renderPagination(filteredBooks.length); // 渲染分页按钮
        }, 10); // 模拟加载时间,不考虑加载动画后好像也没用了
    }

    // 渲染分页函数
    function renderPagination(totalBooks) {
        pagination.innerHTML = ''; // 清空当前分页按钮
        // const totalPages = Math.ceil(totalBooks / booksPerPage);
        console.log('totalPages', totalPages);
        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.textContent = i;
            if (i === currentPage) {
                button.disabled = true;
            }
            button.addEventListener('click', () => {
                currentPage = i;
                loadBooks();
                // renderBooks(); // 切换页码并渲染书籍
            });
            pagination.appendChild(button);
        }
    }

    // 加载书籍
    function loadBooks() {
        const keyword = searchInput.value.toLowerCase() || void 0;
        const category = categorySelect.value;
        $.ajax({
            async: true,
            url: 'http://127.0.0.1:5000/articles/page',
            type: 'GET',
            data: {
                pageNumber: currentPage,
                pageSize: booksPerPage,
                keyword: keyword,
                category: category !== 'all' ? category : void 0,
            },
            dataType: 'json',
            timeout: 30000,
            success: (json) => {
                console.log(json);
                if (json.code === 200) {
                    books = json?.data?.data || [];
                    totalPages = json?.data.pages || 1;
                    // 初次渲染书籍
                    renderBooks();
                } else {
                    alert(json.msg);
                }
            },
            error: (xhr, status) => {
                console.log('出问题了！', xhr, status);
            }
        });
    }

    // 搜索框输入事件监听
    searchInput.addEventListener('change', () => {
        currentPage = 1; // 重置到第一页
        // renderBooks();
        searchInput.blur();
        loadBooks();
    });

    // 类别选择事件监听
    categorySelect.addEventListener('change', () => {
        currentPage = 1; // 重置到第一页
        // renderBooks();
        loadBooks();
    });

    loadBooks();

    // 星空动画
    const body = document.querySelector("body");
    for (let i = 0; i < 100; i++) {
        const star = document.createElement("div");
        star.classList.add("stars");
        star.style.top = `${Math.random() * 100}%`;
        star.style.left = `${Math.random() * 100}%`;
        star.style.animationDuration = `${Math.random() * 2 + 1}s`;
        body.appendChild(star);
    }

});
