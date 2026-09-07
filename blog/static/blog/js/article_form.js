const titleInput = document.getElementById("id_title");
const titleCount = document.getElementById("title-count");

function updateTitleCount() {
    const count = titleInput.value.length;

    titleCount.textContent = `${count} / 50文字`;

    if (count > 50) {
        titleCount.textContent += " ※50文字以内で入力してください";
    }
}

titleInput.addEventListener("input", updateTitleCount);

updateTitleCount();