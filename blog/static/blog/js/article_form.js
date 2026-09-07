const titleInput = document.getElementById("id_title");
const titleCount = document.getElementById("title-count");
const tagSelect = document.getElementById("id_tags");
const tagButtons = document.getElementById("tag-buttons");
const tagOptions = tagSelect.querySelectorAll("option");

function updateTitleCount() {
    const count = titleInput.value.length;

    titleCount.textContent = `${count} / 50文字`;

    if (count > 50) {
        titleCount.textContent += " ※50文字以内で入力してください";
    }
}

titleInput.addEventListener("input", updateTitleCount);

updateTitleCount();


tagOptions.forEach(function (option) {
    const button = document.createElement("button");

    button.type = "button";
    button.textContent = option.textContent;

    // ★ 編集画面を開いた時点ですでに選択済みなら ✓ をつける
    if (option.selected) {
        button.textContent = `✓ ${option.textContent}`;
    }

    button.addEventListener("click", function () {
        option.selected = !option.selected;

        if (option.selected) {
            button.textContent = `✓ ${option.textContent}`;
        } else {
            button.textContent = option.textContent;
        }
    });

    tagButtons.appendChild(button);
});

tagSelect.style.display = "none";