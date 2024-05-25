// 获取段落表单数据
function getParagraphFormData() {
  const paragraphsList = [];
  $('form.box').each(function () {
    const $paragraphForm = $(this);
    paragraphsList.push({
      id: $paragraphForm.find('input[name=paragraphId]').val(),
      contentEn: $paragraphForm.find('textarea[name=contentEn]').val(),
      contentZh: $paragraphForm.find('textarea[name=contentZh]').val(),
      wordEn: $paragraphForm.find('textarea[name=wordEn]').val(),
      wordZh: $paragraphForm.find('textarea[name=wordZh]').val(),
      wordSampleEn: $paragraphForm.find('textarea[name=wordSampleEn]').val(),
      wordSampleZh: $paragraphForm.find('textarea[name=wordSampleZh]').val(),
      picture: $paragraphForm.find('input[name=picture]').val(),
    });
  })
  return paragraphsList;
}

// 获取文章表单数据
function getArticleFormData() {
  const $articleForm = $('form.introduction');
  return {
    id: $articleForm.find('input[name=articleId]').val(),
    cover: $articleForm.find('input[name=cover]').val(),
    category: $articleForm.find('select[name=category]').val(),
    title: $articleForm.find('textarea[name=title]').val(),
    intro: $articleForm.find('textarea[name=intro]').val(),
    paragraphsList: getParagraphFormData(),
  }
}

// 生成随机字符串
function generateRandomCode(length) {
  var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
  var code = '';
  for (var i = 0; i < length; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return code;
}

// 渲染文章
function renderArticle(articleInfo) {
  const $articleForm = $('form.introduction');
  $articleForm.find('input[name=articleId]').val(articleInfo.id);
  $articleForm.find('input[name=cover]').val(articleInfo.cover);
  $articleForm.find('select[name=category]').val(articleInfo.category);
  $articleForm.find('textarea[name=title]').val(articleInfo.title);
  $articleForm.find('textarea[name=intro]').val(articleInfo.intro);
  $articleForm.find('.introduction-icon img').attr('src', articleInfo.coverUrl).css('display', 'block');

  // 渲染段落
  const $paragraphs = $('#paragraphs');
  articleInfo.paragraphsList.forEach(item => {
    addParagraph($paragraphs, item, true);
  });
  if (articleInfo.paragraphsList.length === 0) {
    // 初始化段落
    addParagraph($paragraphs, {}, true);
  }
}

// 添加段落
function addParagraph($node, item= {}, isAppend = true) {
  const boxHtmlId = `data-v="${generateRandomCode(6)}"`;
  const paragraphId = item.id || '';
  const nodeHtml = `
      <form class="box" data-id="${paragraphId}" ${boxHtmlId}>
        <input type="text" name="paragraphId" value="${paragraphId}" style="display: none;">
        <div class="left">
            <div class="text-english">
                <textarea class="file-content-en" name="contentEn" placeholder="请输入英文内容">${item.contentEn || ''}</textarea>
            </div>
            <div class="text-chinese">
                <textarea class="file-content-zh" name="contentZh" placeholder="请输入中文内容">${item.contentZh || ''}</textarea>
            </div>
            <div class="imageContainer">
                <img src="${item.pictureUrl || ''}" alt="" style="display: ${item.pictureUrl ? 'block' : 'none'}">
                <input type="text" name="picture" value="${item.picture || ''}" style="display: none">
            </div>
        </div>
        <div class="center"></div>
        <div class="right">
            <div class="paragraphs-toolbar">
                <button type="button" class="add" title="新增" ${boxHtmlId}><i class="fa-solid fa-plus"></i></button>
                <button type="button" class="remove" title="移除" ${boxHtmlId}><i class="fa-solid fa-minus"></i></button>
                <button type="button" class="up" title="上移" ${boxHtmlId}><i class="fa-solid fa-up-long"></i></button>
                <button type="button" class="down" title="下移" ${boxHtmlId}><i class="fa-solid fa-down-long"></i></button>
                <button type="button" class="upload" ${boxHtmlId} title="上传插图"><i class="fa-regular fa-image"></i></button>
            </div>
            <textarea class="file-content-word-en" name="wordEn" placeholder="请输入英文注释">${item.wordEn || ''}</textarea>
            <textarea class="file-content-word-zh" name="wordZh" placeholder="请输入中文解释">${item.wordZh || ''}</textarea>
            <textarea class="file-content-word-sample-en" name="wordSampleEn" placeholder="请输入英文例句">${item.wordSampleEn || ''}</textarea>
            <textarea class="file-content-word-sample-zh" name="wordSampleZh" placeholder="请输入中文例句">${item.wordSampleZh || ''}</textarea>
        </div>
      </form>
  `;
  if (isAppend) {
    $node.append(nodeHtml);
  } else {
    $node.after(nodeHtml);
  }
}

// 加载文章
function loadArticle() {
  const articleId = new URLSearchParams(location.search).get("id");
  if (!articleId) {
    // 初始化段落
    return addParagraph($('#paragraphs'), {}, true);
  }
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
        // 渲染文章
        renderArticle(json?.data || {});
      } else {
        alert(json.msg);
      }
    },
    error: (xhr, status) => {
      console.log('出问题了！', xhr, status);
    }
  });
}

// 上传图片
function uploadImage(file, callback) {
  const formData = new FormData();
  formData.append('file', file);
  $.ajax({
    async: true,
    url: 'http://127.0.0.1:5000/upload/image',
    type: 'POST',
    processData: false,  // 告诉jQuery不要处理发送的数据
    contentType: false,  // 告诉jQuery不要设置内容类型头
    data: formData,
    dataType: 'json',
    timeout: 30000,
    success: (json) => {
      console.log(json);
      if (json.code === 200) {
        callback && callback(json?.data);
      } else {
        alert(json.msg);
      }
    },
    error: (xhr, status) => {
      console.log('出问题了！', xhr, status);
    }
  });
}

// 提交表单
function submitForm(data) {
  $.ajax({
    async: true,
    url: `http://127.0.0.1:5000/articles/${data.id ? 'edit/' + data.id : 'add'}`,
    type: 'POST',
    data: JSON.stringify(data),
    dataType: 'json',
    contentType:'application/json; charset=utf-8',
    timeout: 30000,
    success: (json) => {
      console.log(json);
      if (json.code === 200) {
        alert('保存成功');
        window.location.href = `./moreArticles`;
      } else {
        alert(json.msg);
      }
    },
    error: (xhr, status) => {
      console.log('出问题了！', xhr, status);
    }
  });
}

$(() => {
  const $paragraphs = $('#paragraphs');
  $paragraphs.empty();
  // 加载文章
  loadArticle();
  // 添加段落-全局
  $('.floating-toolbar .fa-plus').on('click', function() {
    addParagraph($paragraphs, {}, true);
  });

  // 上传封面
  $('#uploadButton').on('click', function() {
    const fileInput= document.createElement('input');
    fileInput.setAttribute('type', 'file');
    fileInput.setAttribute('accept', 'image/png, image/jpg, image/jpeg');
    fileInput.addEventListener('change', function(e) {
      uploadImage(e.target.files[0], (res) => {
        const $target = $(`#introductionLeft`);
        $target.find('.introduction-icon img').attr({src: res.imageUrl}).css('display', 'block');
        $target.find('.introduction-icon input[name=cover]').val(res.imagePath);
      })
    })
    fileInput.click();
  });

  // 移除段落-局部
  $paragraphs.on('click', 'form.box .paragraphs-toolbar button.remove', function(e) {
    const count = $('#paragraphs form.box').length;
    if (count > 1) {
      const flag = $(this).data('v');
      const $target = $(`#paragraphs form.box[data-v=${flag}]`);
      $target.remove();
      console.log($target);
    } else {
      alert('至少需要保留一组wrap，无法删除！');
    }
  });

  // 上传插图-局部
  $paragraphs.on('click', 'form.box .paragraphs-toolbar button.upload', function(e) {
    const flag = $(this).data('v');
    const fileInput= document.createElement('input');
    fileInput.setAttribute('type', 'file');
    fileInput.setAttribute('accept', 'image/png, image/jpg, image/jpeg');
    fileInput.addEventListener('change', function(e) {
      uploadImage(e.target.files[0], (res) => {
        const $target = $(`#paragraphs form.box[data-v=${flag}]`);
        $target.find('.imageContainer img').attr({src: res.imageUrl}).css('display', 'block');
        $target.find('.imageContainer input[name=picture]').val(res.imagePath);
      })
    })
    fileInput.click();
  });

  // 上移段落
  $paragraphs.on('click', 'form.box .paragraphs-toolbar button.up', function(e) {
    const flag = $(this).data('v');
    const $target = $(`#paragraphs form.box[data-v=${flag}]`);
    const $prev = $target.prev();
    if ($prev.length) {
      $prev.before($target);
    }
  });

  // 下移段落
  $paragraphs.on('click', 'form.box .paragraphs-toolbar button.down', function(e) {
    const flag = $(this).data('v');
    const $target = $(`#paragraphs form.box[data-v=${flag}]`);
    const $next = $target.next();
    if ($next.length) {
      $next.after($target);
    }
  });

  // 插入段落
  $paragraphs.on('click', 'form.box .paragraphs-toolbar button.add', function(e) {
    const flag = $(this).data('v');
    const $target = $(`#paragraphs form.box[data-v=${flag}]`);
    addParagraph($target, {}, false);
  });

  // 提交表单
  $('.save-box button').on('click', function() {
    const articleForm = getArticleFormData();
    if (!articleForm.title || !articleForm.intro) {
      return alert('文章标题或简介未填写');
    }
    let flag = true
    articleForm.paragraphsList.every(item => {
      if (!item.contentEn || !item.contentZh || !item.wordEn || !item.wordZh || !item.wordSampleEn || !item.wordSampleZh) {
        flag = false
        alert('段落内容未填写完整');
        return false
      }
      return true
    })
    if (flag) {
      // 表单填写完整，可以提交
      console.log('表单填写完整，可以提交', articleForm);
      submitForm(articleForm);
    }
  })
});
