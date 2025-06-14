jQuery("button.upload").click(function(){
    jQuery("#first-popup").show("fast");
    jQuery("#first-popup .dialog").show();
})

jQuery("#first-popup #close").click(function(){
    jQuery("#first-popup").hide("fast");
})
jQuery("button.menu-icon").click(function(){
    jQuery("#main-header").addClass("animate");
    jQuery("#main-header").addClass("open");
})
jQuery("#main-header .menu-close-icon").click(function(){
    jQuery("#main-header").removeClass("open animate");
})
jQuery(".dropzone-blue.dropzone").click(function(){
  jQuery(this).prev().find("input").click();
})

let collectedThumbnails = [];


$('#file-input').on('change', function () {
    jQuery("#close").click();
    const files = this.files;
    if (files.length === 0) return;

    $('#uploadPopup').fadeIn();
    $('#popupOverlay').fadeIn();
    $('#thumbnailPreview').empty();
    $('#currentIndex').text(1);
    $('#totalCount').text(files.length);
    updateProgress(0);

    for (let i = 0; i < files.length; i++) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const dataUrl = e.target.result;
        collectedThumbnails.push({
            dataUrl: e.target.result,
            filename: files[i].name
        });
        jQuery('#thumbnailPreview').append(`<img src="${dataUrl}" alt="img${i}"/>`);
      };
      reader.readAsDataURL(files[i]);
    }

    let index = 0;

    function uploadNext() {
      if (index >= files.length) {
        updateProgress(100);
        $('#uploadStatus').text('Готово!');
        setTimeout(() => {
            $('#uploadPopup').fadeOut();
            // передаем массив миниатюр
            showFaceSelectionPopup(collectedThumbnails);
        }, 1000);
        return;
      }

      const formData = new FormData();
      formData.append('file', files[index]);

      $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function () {
          index++;
          const percent = Math.round((index / files.length) * 100);
          $('#currentIndex').text(index);
          updateProgress(percent);
          setTimeout(() => {
            uploadNext();
          }, 500);
        }
      });
    }
    function updateProgress(percent) {
      const circle = document.getElementById('progressCircle');
      const dashArray = 2 * Math.PI * 40; // длина окружности (r = 40)
      const offset = dashArray - (percent / 100) * dashArray;

      circle.style.strokeDashoffset = offset;
      let current = parseInt($('#progressText').text()) || 0;
        jQuery({ count: current }).animate({ count: percent }, {
        duration: 600,
        easing: 'swing',
        step: function (val) {
            jQuery('#progressText').text(Math.floor(val) + '%');
        }
        });
    }
    uploadNext();
  });


function showFaceSelectionPopup(thumbnails) {
  // Скрыть старый popup и показать overlay + новый
  $('#uploadPopup').fadeOut();
  $('#popupOverlay').fadeIn();
  $('#selectFacePopup').fadeIn();

  const $grid = $('#faceGrid');
  $grid.empty();

  thumbnails.forEach((src, index) => {
    const $img = $('<img>').attr('src', src.dataUrl).attr('data-filename', src.filename).attr('data-index', index);
    $grid.append($img);
  });

  // Клик по лицу
  $('#faceGrid img').on('click', function () {
    $('#faceGrid img').removeClass('selected');
    $(this).addClass('selected');
    $('#goToSearchBtn').addClass('active').prop('disabled', false);
  });

  // Кнопка поиска
  $('#goToSearchBtn').on('click', function () {
    const selected = $('#faceGrid img.selected');
    if (!selected.length) return;

    const selectedSrc = selected.attr('src');
    const selectedFilename = selected.attr('data-filename');

    // Закрываем выбор лица, открываем анализ
    $('#selectFacePopup').fadeOut();
    $('#analyzeFacePopup').fadeIn();
    $('#popupOverlay').fadeIn();
     // Отображение миниатюры + СОХРАНЕНИЕ имени в DOM
    $('#analyzePreview')
        .attr('src', selectedSrc)
        .attr('data-filename', selectedFilename);
    });
}


$('#startAnalysisBtn').on('click', function () {
  const filename = $('#analyzePreview').attr('data-filename');
  if (!filename) {
    alert("Не удалось получить имя файла");
    return;
  }
  window.location.href = `/results?chosen=${filename}`;
});

$('.toggle-option').on('click', function () {
  $(this).toggleClass('active');
});