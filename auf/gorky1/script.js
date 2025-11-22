// Функция для проверки прокрутки до конца
function checkScroll() {
  const footer = document.getElementById("footer");
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  const scrollHeight = document.documentElement.scrollHeight;
  const clientHeight = document.documentElement.clientHeight;

  // Проверяем, достигли ли конца страницы (с небольшим запасом в 50px)
  if (scrollTop + clientHeight >= scrollHeight - 50) {
    footer.classList.add("show");
  } else {
    footer.classList.remove("show");
  }
}

// Слушаем событие прокрутки
window.addEventListener("scroll", checkScroll);

// Также проверяем при загрузке страницы
window.addEventListener("load", checkScroll);
