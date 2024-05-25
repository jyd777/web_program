$(() => {
  let articleInfo = {};
  // 加载文章
  function loadArticle() {
    const articleId = new URLSearchParams(location.search).get("id");
    if (!articleId) return;
    $.ajax({
      async: true,
      url: 'http://127.0.0.1:5000/articles/' + articleId,
      type: 'GET',
      data: {},
      dataType: 'json',
      timeout: 30000,
      success: (json) => {
        console.log(json);
        if (json.code === 200) {
          articleInfo = json?.data || {}
          // 初次渲染文章
          renderArticle();
        } else {
          alert(json.msg);
        }
      },
      error: (xhr, status) => {
        console.log('出问题了！', xhr, status);
      }
    });
  }

  // 渲染文章
  function renderArticle() {
    $('#title').html(articleInfo.title);
    $('#intro').html(articleInfo.intro);
    $('#cover').attr('src', articleInfo.coverUrl || "../static/TextImage/globalwarming.png");
    const $paragraphs = $('#paragraphs');
    // 清空
    $paragraphs.empty();
    articleInfo.paragraphsList.forEach(paragraph => {
      renderParagraph($paragraphs, paragraph);
    })
  }

  // 渲染段落
  function renderParagraph($node, item) {
    // 插图
    let illustration = '';
    if (item.picture) {
      illustration = `<div class="image-inserted">
          <img src="${item.pictureUrl}" alt="插图">
      </div>`;
    }
    const contentEnHtmlMark = item.contentEn.replace(item.wordEn, `<span class="mark">${item.wordEn}</span>`);
    const wordSampleEnHtmlMark = item.wordSampleEn.replace(item.wordEn, `<span class="highlight ">${item.wordEn}</span>`);
    $node.append(`
      <div class="box">
          <div class="left">
              <div class="text-english">${contentEnHtmlMark}</div>
              <div class="text-chinese">${item.contentZh}</div>
          </div>
          <div class="center"></div>
          <div class="right">
              <div class="phrase">${item.wordEn}</div>
              <div class="explain">${item.wordZh}</div>
              <div class="example">
                  <span>e.g.</span>
                  <p>${wordSampleEnHtmlMark}</p>
                  <p>${item.wordSampleZh}</p>
              </div>
          </div>
      </div>
      ${illustration}
    `)
  }

  loadArticle();
})
